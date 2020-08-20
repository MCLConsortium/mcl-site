# encoding: utf-8

u'''MCL — testing fixtures and layers.'''

from plone.app.testing import IntegrationTesting, FunctionalTesting, PloneSandboxLayer
from Products.CMFPlone.factory import _CONTENT_PROFILE
from Products.CMFCore.utils import getToolByName

class MCLPolicy(PloneSandboxLayer):
    u'''MCL sandbox layer.'''
    def setUpZope(self, app, configurationContext):
        import jpl.mcl.site.policy
        self.loadZCML(package=jpl.mcl.site.policy)
    def setUpPloneSite(self, portal):
        wfTool = getToolByName(portal, 'portal_workflow')
        wfTool.setDefaultChain('plone_workflow')
        self.applyProfile(portal, _CONTENT_PROFILE)
        self.applyProfile(portal, 'jpl.mcl.site.policy:default')


MCL_POLICY = MCLPolicy()
MCL_POLICY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MCL_POLICY,), name='MCLPolicy:Integration'
)
MCL_POLICY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MCL_POLICY,), name='MCLPolicy:Functional'
)
