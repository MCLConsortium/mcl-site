# encoding: utf-8

u'''MCL — custom upgrade steps.'''

import plone.api
from eea.facetednavigation.layout.interfaces import IFacetedLayout
from Products.CMFCore.utils import getToolByName
from ._utils import setFacetedNavigation

def _getPortal(context):
    return getToolByName(context, 'portal_url').getPortalObject()

def installSciencedataView(setupTool):
    u'''Install jpl.mcl.site.sciencedata.'''
    '''Set up faceted navigation and add disclaimers on all Science Folders.'''
    portal = _getPortal(setupTool)
    request = portal.REQUEST
    sciencefolder = portal['science-data']
    setFacetedNavigation(sciencefolder, request, force=True)

def emptyfunc(setupTool):
    u'''Empty function'''
    print("Upgraded")
