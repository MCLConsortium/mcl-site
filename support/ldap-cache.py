#!/usr/bin/env python
# encoding: utf-8
# Copyright 2017 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager
from AccessControl.SecurityManager import setSecurityPolicy
from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy, OmnipotentUser
from Products.CMFCore.utils import getToolByName
from Testing import makerequest
from zope.component.hooks import setSite
import sys, logging, transaction


logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
app = globals().get('app', None)  # ``app`` comes from ``instance run`` magic.


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
    logging.info(u'Getting the portal')
    portal = app.unrestrictedTraverse('mcl')
    portal.setupCurrentSkin(app.REQUEST)
    setSite(portal)
    return portal


def _fixLDAPcache(app):
    app = makerequest.makerequest(app)
    _setupZopeSecurity(app)
    portal = _setupPortal(app)
    ramCache = getToolByName(portal, 'RAMCache')
    ramCache.ZCacheManager_setAssociations({'associate_acl_users': 1, 'associate_acl_users/ldap-plugin': 1})
    transaction.commit()
    noSecurityManager()


def main(argv):
    _setupLogging()
    try:
        global app
        _fixLDAPcache(app)
    except Exception as ex:
        logging.exception(u'Cannot fix LDAP caching: %s', unicode(ex))
        return False
    return True


if __name__ == '__main__':
    # The [2:] works around plone.recipe.zope2instance-4.2.6's lame bin/interpreter script issue
    sys.exit(0 if main(sys.argv[2:]) is True else -1)
