# encoding: utf-8

u'''MCL setup tests'''

from jpl.mcl.site.policy.testing import MCL_POLICY_INTEGRATION_TESTING
import plone.api, unittest


class SetupTest(unittest.TestCase):
    layer = MCL_POLICY_INTEGRATION_TESTING
    def setUp(self):
        super(SetupTest, self).setUp()
        self.portal = self.layer['portal']
    def testTitle(self):
        '''Check that title is what we want.'''
        self.assertEquals(u'MCL', self.portal.getProperty('title'))
    def testPortalDescription(self):
        '''Ensure the site's description is correct.'''
        self.assertEquals(u'Molecular and Cellular Characterization of Screen-Detected Lesions',
            self.portal.getProperty('description'))
    def testDependencies(self):
        '''Verify our dependencies got installed'''
        qi = plone.api.portal.get_tool('portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('jpl.mcl.site.knowledge'), 'jpl.mcl.site.knowledge failed to install')
        self.assertTrue(qi.isProductInstalled('jpl.mcl.site.sciencedata'), 'jpl.mcl.site.knowledge failed to install')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
