# encoding: utf-8

u'''MCL Site Knowledge — setup tests'''

from jpl.mcl.site.knowledge.testing import JPL_MCL_SITE_KNOWLEDGE_INTEGRATION_TESTING
import unittest, plone.api


class SetupTest(unittest.TestCase):
    layer = JPL_MCL_SITE_KNOWLEDGE_INTEGRATION_TESTING
    def setUp(self):
        super(SetupTest, self).setUp()
        self.portal = self.layer['portal']
    def testCatalogIndexes(self):
        u'''Ensure the catalog has our custom indexes'''
        catalog = plone.api.portal.get_tool('portal_catalog')
        indexes = catalog.indexes()
        for index in ('subjectURI', 'phone', 'homepage', 'dcbflag', 'dcpflag'):
            self.assertTrue(index in indexes, u'"{}" index not installed'.format(index))
    def testCatalogMetadata(self):
        u'''Check that the catalog has our custom metadata columns'''
        catalog = plone.api.portal.get_tool('portal_catalog')
        columns = catalog.schema()
        for column in ('subjectURI', 'phone', 'homepage', 'dcbflag', 'dcpflag'):
            self.assertTrue(column in columns, u'"{}" column not installed'.format(column))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
