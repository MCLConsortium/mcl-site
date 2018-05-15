#!/usr/bin/env python
# encoding: utf-8
# Copyright 2016 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager
from AccessControl.SecurityManager import setSecurityPolicy
from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy, OmnipotentUser
from Testing import makerequest
import sys, logging, transaction, argparse


logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
app = globals().get('app', None)  # ``app`` comes from ``instance run`` magic.
_argParser = argparse.ArgumentParser(prog='upgrade.py', description=u'Adds a Manager user')
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


def _nukeAdmins(app):
    logging.info(u'Remove old admin users')
    acl_users = app.acl_users
    acl_users.userFolderDelUsers(acl_users.getUserNames())


def _installAdmin(app, username, password):
    logging.info(u'Installing new admin user named %s with password %s', username, password)
    acl_users = app.acl_users
    acl_users.userFolderAddUser(username, password, ['Manager'], [])


def _addAdmin(app, username, password):
    app = makerequest.makerequest(app)
    _setupZopeSecurity(app)
    _nukeAdmins(app)
    _installAdmin(app, username, password)
    transaction.commit()
    noSecurityManager()


def main(argv):
    _setupLogging()
    try:
        global app
        args = _argParser.parse_args(argv[1:])
        _addAdmin(app, args.username, args.password)
    except Exception as ex:
        logging.exception(u'Cannot upgrade: %s', unicode(ex))
        return False
    return True


if __name__ == '__main__':
    # The [2:] works around plone.recipe.zope2instance-4.2.6's lame bin/interpreter script issue
    sys.exit(0 if main(sys.argv[2:]) is True else -1)