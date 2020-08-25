#!/usr/bin/env python
# encoding: utf-8
# Copyright 2020 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManager import setSecurityPolicy
# from plone.app.viewletmanager.interfaces import IViewletSettingsStorage  # not ready
from plone.registry.interfaces import IRegistry
from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy, OmnipotentUser
from zope.component import getUtility
import sys, logging, transaction


logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
app = globals().get('app', None)  # ``app`` comes from ``instance run`` magic.


NO_ROBOTS = u'''User-agent: *
Disallow: /
'''


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


# When we upgrade to pas.plugins.ldap, we'll need this:
# def setLDAPcacheParams(portal):
#     logging.info('Setting memcached server for LDAP to localhost:11211')
#     registry = getUtility(IRegistry)
#     registry['pas.plugins.ldap.memcached'] = u'localhost:11211'


def disableSearchEngines(portal):
    logging.info('Disabling search engines')
    registry = getUtility(IRegistry)
    registry['plone.webstats_js'] = u''
    registry['plone.robots_txt'] = NO_ROBOTS


def disableEmail(portal):
    logging.info('Setting SMTP server to bogus value')
    registry = getUtility(IRegistry)
    registry['plone.smtp_host'] = u'non.exist.int'  # Ths misspelling is intentional; get it?


# This is a nice feature; we're not ready for it, though:
# def showDevWarning(portal):
#     storage = getUtility(IViewletSettingsStorage)
#     skinName = portal.getCurrentSkinName() if portal.getCurrentSkinName() else 'Plone Default'
#     hidden = list(storage.getHidden('plone.portaltop', skinName))
#     try:
#         hidden.remove('mcl.dev_warning')
#         storage.setHidden('plone.portaltop', skinName, hidden)
#     except ValueError:
#         pass


def _main(app):
    # Apparently we don't need this; just do ``bin/zope-debug -O mcl run $PWD/support/upgradeMCL.py``
    portal = app['mcl']
    # Don't need this either, thanks to ``-O mcl``
    # setSite(portal)
    # setLDAPcacheParams(portal)  # not ready
    disableSearchEngines(portal)
    disableEmail(portal)
    # showDevWarning(portal)  # not ready
    transaction.commit()
    return True


def main(argv):
    _setupLogging()
    try:
        global app
        _main(app)
    except Exception as ex:
        logging.exception(u'This is most unfortunate: %s', unicode(ex))
        return False
    return True


if __name__ == '__main__':
    # The [2:] works around plone.recipe.zope2instance-4.2.6's lame bin/interpreter script issue
    sys.exit(0 if main(sys.argv[2:]) is True else -1)
