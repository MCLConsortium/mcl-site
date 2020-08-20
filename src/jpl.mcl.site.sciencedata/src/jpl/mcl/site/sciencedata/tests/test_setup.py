# encoding: utf-8

u'''MCL Site Science Data — setup tests'''

from jpl.mcl.site.sciencedata.testing import JPL_MCL_SITE_SCIENCEDATA_INTEGRATION_TESTING
import unittest, plone.api


class SetupTest(unittest.TestCase):
    layer = JPL_MCL_SITE_SCIENCEDATA_INTEGRATION_TESTING
    def setUp(self):
        super(SetupTest, self).setUp()
        self.portal = self.layer['portal']
    def testCatalogIndexes(self):
        u'''Ensure the catalog has our custom indexes'''
        catalog = plone.api.portal.get_tool('portal_catalog')
        indexes = catalog.indexes()
        self.assertTrue('subjectURI' in indexes, u'"subjectURI" index not installed')
    def testCatalogMetadata(self):
        u'''Check that the catalog has our custom metadata columns'''
        catalog = plone.api.portal.get_tool('portal_catalog')
        columns = catalog.schema()
        self.assertTrue('subjectURI' in columns, u'"subjectURI" column not installed')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
