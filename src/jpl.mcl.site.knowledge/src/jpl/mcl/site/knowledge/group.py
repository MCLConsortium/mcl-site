# encoding: utf-8

u'''MCL — Working Group'''

from . import MESSAGE_FACTORY as _
from ._utils import getReferencedBrains, getFirstInst
from Acquisition import aq_inner
from five import grok
from plone.memoize import view
from interfaces import IGroup, IPerson, IInstitution
from Products.CMFCore.utils import getToolByName
from zope.intid.interfaces import IIntIds
from zope.component import getUtility

class View(grok.View):
    u'''View for a working group.'''
    grok.context(IGroup)
    grok.require('zope2.View')
    @view.memoize
    def chairs(self):
        context = aq_inner(self.context)
        chairs = getReferencedBrains(context.chairs)
        catalog = getToolByName(context, 'portal_catalog')
        intids = getUtility(IIntIds)
        institutions = [i.getObject() for i in catalog(object_provides=IInstitution.__identifier__)]

        mem_inst = []
        for mem in chairs:
            myID = intids.getId(mem.getObject())
            inst = getFirstInst(myID, institutions)
            mem_inst.append((mem, inst))

        return mem_inst
    @view.memoize
    def cochairs(self):
        context = aq_inner(self.context)
        cochairs = getReferencedBrains(context.cochairs)
        catalog = getToolByName(context, 'portal_catalog')
        intids = getUtility(IIntIds)
        institutions = [i.getObject() for i in catalog(object_provides=IInstitution.__identifier__)]

        mem_inst = []
        for mem in cochairs:
            myID = intids.getId(mem.getObject())
            inst = getFirstInst(myID, institutions)
            mem_inst.append((mem, inst))

        return mem_inst
    @view.memoize
    def members(self):
        context = aq_inner(self.context)
        members = getReferencedBrains(context.members)
        catalog = getToolByName(context, 'portal_catalog')
        intids = getUtility(IIntIds)
        institutions = [i.getObject() for i in catalog(object_provides=IInstitution.__identifier__)]

        mem_inst = []
        for mem in members:
            myID = intids.getId(mem.getObject())
            inst = getFirstInst(myID, institutions)
            mem_inst.append((mem, inst))

        return mem_inst


IGroup.setTaggedValue('typeURI', u'https://cancer.jpl.nasa.gov/rdf/types.rdf#Group')
IGroup.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': ('title', False),
    u'http://purl.org/dc/terms/description': ('description', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#chair': ('chairs', True),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#cochair': ('cochairs', True),
    u'http://xmlns.com/foaf/0.1/member': ('members', True)
})
IGroup.setTaggedValue('fti', 'jpl.mcl.site.knowledge.group')
