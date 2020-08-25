# encoding: utf-8

from plone.app.testing import PloneSandboxLayer, IntegrationTesting, FunctionalTesting, PLONE_FIXTURE
from . import PACKAGE_NAME
import pkg_resources, urllib2, urllib, httplib, plone.api


class TestSchemeHandler(urllib2.BaseHandler):
    u'''A special URL handler for the testing-only scheme ``testscheme``.'''
    def testscheme_open(self, req):
        try:
            selector = req.get_selector()
            path = 'tests/data/' + selector.split('/')[-1] + '.json'

            if pkg_resources.resource_exists(PACKAGE_NAME, path):
                return urllib.addinfourl(
                    pkg_resources.resource_stream(PACKAGE_NAME, path),
                    httplib.HTTPMessage(open('/dev/null')),
                    req.get_full_url(),
                    200
                )
            else:
                raise urllib2.URLError('Not found')
        except Exception:
            raise urllib2.URLError('Not found')


class JPLMCLSiteSciencedataLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        import jpl.mcl.site.sciencedata
        self.loadZCML(package=jpl.mcl.site.sciencedata)
        urllib2.install_opener(urllib2.build_opener(TestSchemeHandler))
    def setUpPloneSite(self, portal):
        wfTool = plone.api.portal.get_tool('portal_workflow')
        wfTool.setDefaultChain('plone_workflow')
        self.applyProfile(portal, 'jpl.mcl.site.sciencedata:default')


JPL_MCL_SITE_SCIENCEDATA_FIXTURE = JPLMCLSiteSciencedataLayer()
JPL_MCL_SITE_SCIENCEDATA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(JPL_MCL_SITE_SCIENCEDATA_FIXTURE,),
    name='JPLMCLSiteSciencedataLayer:IntegrationTesting'
)
JPL_MCL_SITE_SCIENCEDATA_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(JPL_MCL_SITE_SCIENCEDATA_FIXTURE,),
    name='JPLMCLSiteSciencedataLayer:FunctionalTesting'
)
