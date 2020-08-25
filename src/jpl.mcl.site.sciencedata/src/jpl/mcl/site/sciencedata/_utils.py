# encoding: utf-8

u'''MCL Site Science Data — Utilities.'''


from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.WorkflowCore import WorkflowException
from zope.interface import noLongerProvides
from zope.component import getMultiAdapter
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.layout.interfaces import IFacetedLayout
from eea.facetednavigation.settings.interfaces import IHidePloneLeftColumn, IHidePloneRightColumn
import plone.api


def publish(context, wfTool=None):
    u'''Publish the ``context`` item and all of its contents using the given
    ``wfTool``.  If no ``wfTool`` is given, we'll look up the portal_workflow
    tool.'''
    try:
        if wfTool is None: wfTool = plone.api.portal.get_tool('portal_workflow')
        wfTool.doActionFor(context, action='publish')
        context.reindexObject()
    except WorkflowException:
        pass
    if IFolderish.providedBy(context):
        for itemID, subItem in context.contentItems():
            publish(subItem, wfTool)


class IngestResults(object):
    def __init__(self, created, updated, deleted):
        self.created, self.updated, self.deleted = created, updated, deleted

def setFacetedNavigation(folder, request, force=False):
    subtyper = getMultiAdapter((folder, request), name=u'faceted_subtyper')
    if (subtyper.is_faceted or not subtyper.can_enable) and not force: return
    subtyper.enable()
    urlTool = plone.api.portal.get_tool(name='portal_url')

    IFacetedLayout(folder).update_layout('faceted_sciencedata_view')
    noLongerProvides(folder, IHidePloneLeftColumn)
    noLongerProvides(folder, IHidePloneRightColumn)
