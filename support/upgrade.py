#!/usr/bin/env python
# encoding: utf-8
# Copyright 2016 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager
from AccessControl.SecurityManager import setSecurityPolicy
from plone.app.linkintegrity.handlers import modifiedContent
from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy, OmnipotentUser
from Products.CMFCore.utils import getToolByName
from Testing import makerequest
from zExceptions import NotFound
from zope.component.hooks import setSite
import sys, argparse, logging, transaction


logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
app = globals().get('app', None)  # ``app`` comes from ``instance run`` magic.
_argParser = argparse.ArgumentParser(prog='upgrade.py', description=u'Upgrades an MCL site from a previous version')
_argParser.add_argument('username', help=u'Zope admin user')
_argParser.add_argument('password', help=u"Zope admin password")


def _setupLogging():
    channel = logging.StreamHandler()
    channel.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
    logger = logging.getLogger('jpl')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(channel)


def _setupZopeSecurity(app):
    logging.info(u'Setting up Zope security')
    acl_users = app.acl_users
    setSecurityPolicy(PermissiveSecurityPolicy())
    newSecurityManager(None, OmnipotentUser().__of__(acl_users))


def _setupPortal(app):
    logging.info(u'Setting up the portal')
    portal = app.unrestrictedTraverse('mcl')
    portal.setupCurrentSkin(app.REQUEST)
    setSite(portal)
    return portal


# This doesn't work anymore. Instead, the calling script will do::
#     curl -v 'http://localhost:6478/mcl/@@plone-upgrade' --user 'admin:admin' -H 'Content-Type: application/x-www-form-urlencoded' --data 'form.submitted%3Aboolean=True&submit=Upgrade'
# Good bye seirdly nonfunctional migrationTool upgrade!
# def _upgradePlone(portal):
#     logging.info(u'Upgrading Plone')
#     migrationTool = getToolByName(portal, 'portal_migration')
#     migrationTool.upgrade(dry_run=False)


def _upgradeScience(portal):
    logging.info(u'Upgrading Science Package')
    qi = getToolByName(portal, 'portal_quickinstaller')
    qi.upgradeProduct('jpl.mcl.site.sciencedata')


def _updateLinkIntegrity(portal):
    logging.info(u'Updating link integrity information')
    catalog = getToolByName(portal, 'portal_catalog')
    count = 0
    for brain in catalog({}):
        try:
            obj = brain.getObject()
        except (AttributeError, NotFound, KeyError):
            msg = "Catalog inconsistency: {} not found!"
            logging.error(msg.format(brain.getPath()), exc_info=1)
            continue
        try:
            modifiedContent(obj, 'dummy event parameter')
            count += 1
        except Exception:
            msg = "Error updating linkintegrity-info for {}."
            logging.error(msg.format(obj.absolute_url()), exc_info=1)
        if count % 1000 == 0:
            transaction.savepoint(optimistic=True)
    logging.info(u'Updated %d objects', count)


def _upgradeMCL(portal):
    logging.info(u'Upgrading MCL Site')
    qi = getToolByName(portal, 'portal_quickinstaller')
    qi.upgradeProduct('jpl.mcl.site.policy')


def _upgrade(app, username, password):
    app = makerequest.makerequest(app)
    _setupZopeSecurity(app)
    portal = _setupPortal(app)
    _updateLinkIntegrity(portal)
    _upgradeMCL(portal)
    _upgradeScience(portal)
    transaction.commit()
    noSecurityManager()


def main(argv):
    _setupLogging()
    try:
        global app
        args = _argParser.parse_args(argv[1:])
        _upgrade(app, args.username, args.password)
    except Exception as ex:
        logging.exception(u'Cannot upgrade: %s', unicode(ex))
        return False
    return True


if __name__ == '__main__':
    # The [2:] works around plone.recipe.zope2instance-4.2.6's lame bin/interpreter script issue
    sys.exit(0 if main(sys.argv[2:]) is True else -1)
