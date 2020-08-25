#!/usr/bin/env python
# encoding: utf-8
# Copyright 2020 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

import sys, logging, transaction
from Products.CMFPlone.utils import get_installer


_products = [
    # 'edrnsite.portlets',
    # 'edrn.theme',
    # 'eke.knowledge',
    # 'edrnsite.policy',
    # 'collective.js.jqueryui',    # This wants to be upgraded even though it says its profile version is the same
    # 'eea.facetednavigation',     # 11.7→13.8
]

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
app = globals().get('app', None)  # ``app`` comes from ``instance run`` magic.


def _setupLogging():
    channel = logging.StreamHandler()
    channel.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
    logger = logging.getLogger('jpl')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(channel)


def upgradeMCL(portal):
    # OK, so what needs to be done here?
    # Probably the equivalemnt of hitting the upgrade button on jpl.mcl.site.policy
    # on the add/remove programs panel in Plone, maybe followed by a full ingest
    qi = get_installer(portal)
    for productID in _products:
        logging.info(u'=== UPGRADING %s', productID)
        qi.upgrade_product(productID)


def _main(app):
    # Run: ``bin/zope-debug -O mcl run $PWD/support/upgradeMCL.py``
    portal = app['mcl']
    upgradeMCL(portal)
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
