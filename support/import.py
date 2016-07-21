#!/usr/bin/env python
# encoding: utf-8
# Copyright 2016 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

import sys, argparse, logging, transaction, os, os.path, shutil
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager
from AccessControl.SecurityManager import setSecurityPolicy
from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy, OmnipotentUser


logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
app = globals().get('app', None)  # ``app`` comes from ``instance run`` magic.
_argParser = argparse.ArgumentParser(prog='import.py', description=u'Imports a ZEXP file into a Zope app server')
_argParser.add_argument('file', help=u'ZEXP file to import')
_argParser.add_argument('importdir', help=u"Zope's import directory")


def _setupZopeSecurity(app):
    logging.info(u'Setting up Zope security')
    acl_users = app.acl_users
    setSecurityPolicy(PermissiveSecurityPolicy())
    newSecurityManager(None, OmnipotentUser().__of__(acl_users))


def _importZEXP(app, zexpfile, importDir):
    app = makerequest.makerequest(app)
    _setupZopeSecurity(app)
    dest = os.path.join(os.path.abspath(importDir), 'mcl.zexp')
    logging.info(u'Moving %s to %s', zexpfile, dest)
    shutil.copy(zexpfile, dest)
    logging.info(u'Importing')
    app.manage_importObject('mcl.zexp', set_owner=0)
    transaction.commit()
    noSecurityManager()


def main(argv):
    try:
        global app
        args = _argParser.parse_args(argv[1:])
        _importZEXP(app, args.file, args.importdir)
    except Exception as ex:
        logging.exception(u'Cannot import "%s": %s', args.file, unicode(ex))
        return False
    return True


if __name__ == '__main__':
    # The [2:] works around plone.recipe.zope2instance-4.2.6's lame bin/interpreter script issue
    sys.exit(0 if main(sys.argv[2:]) is True else -1)
