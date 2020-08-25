#!/usr/bin/env python
# encoding: utf-8
# Copyright 2020 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

import sys, logging, transaction, plone.api


logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
app = globals().get('app', None)  # ``app`` comes from ``instance run`` magic.


def _setupLogging():
    channel = logging.StreamHandler()
    channel.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
    logger = logging.getLogger('jpl')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(channel)


def upgradePlone(portal):
    migrationTool = plone.api.portal.get_tool('portal_migration')
    migrationTool.upgrade()


def _main(app):
    portal = app['mcl']
    upgradePlone(portal)
    transaction.commit()
    return True


def main(argv):
    _setupLogging()
    try:
        global app
        _main(app)
    except Exception as ex:
        logging.exception(u'This sucks: %s', unicode(ex))
        return False
    return True


if __name__ == '__main__':
    # The [2:] works around plone.recipe.zope2instance-4.2.6's lame bin/interpreter script issue
    sys.exit(0 if main(sys.argv[2:]) is True else -1)
