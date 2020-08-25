# encoding: utf-8

u'''MCL — ParticipatingSite'''

from ._utils import getReferencedBrains, getFirstInst
from Acquisition import aq_inner
from five import grok
from plone.memoize import view
from Products.CMFCore.utils import getToolByName
from zope.intid.interfaces import IIntIds
from zope.component import getUtility
from interfaces import IParticipatingSite, IInstitution, IOrgan, IPerson

class View(grok.View):
    u'''View for an working group folder'''
    grok.context(IParticipatingSite)
    grok.require('zope2.View')
    @view.memoize
    def organs(self):
        context = aq_inner(self.context)
        return getReferencedBrains(context.organ)
    @view.memoize
    def pis(self):
        context = aq_inner(self.context)
        pis = getReferencedBrains(context.pi)
        catalog = getToolByName(context, 'portal_catalog')
        intids = getUtility(IIntIds)
        institutions = [i.getObject() for i in catalog(object_provides=IInstitution.__identifier__)]

        pi_inst = []
        for mem in pis:
            myID = intids.getId(mem.getObject())
            inst = getFirstInst(myID, institutions)
            pi_inst.append((mem, inst))

        return pi_inst

    @view.memoize
    def staff(self):
        context = aq_inner(self.context)
        staff = getReferencedBrains(context.staff)
        catalog = getToolByName(context, 'portal_catalog')
        intids = getUtility(IIntIds)
        institutions = [i.getObject() for i in catalog(object_provides=IInstitution.__identifier__)]

        staff_inst = []
        for mem in staff:
            myID = intids.getId(mem.getObject())
            inst = getFirstInst(myID, institutions)
            staff_inst.append((mem, inst))

        return staff_inst

    @view.memoize
    def contacts(self):
        context = aq_inner(self.context)
        return getReferencedBrains(context.contact)
    @view.memoize
    def institutions(self):
        context = aq_inner(self.context)
        return getReferencedBrains(context.institution)


IParticipatingSite.setTaggedValue('typeURI', u'https://cancer.jpl.nasa.gov/rdf/types.rdf#FundedSite')
IParticipatingSite.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': ('title', False),
    u'http://purl.org/dc/terms/description': ('description', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#aims': ('aims', False),
    u'http://purl.org/dc/terms/abstract': ('abstract', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#abbreviatedName': ('abbreviation', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#organ': ('organ', True),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#staff': ('staff', True),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#pi': ('pi', True),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#contact': ('contact', True),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#fundingStartDate': ('fundingStartDate', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#fundingFinishDate': ('fundingFinishDate', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#institution': ('institution', True)
})
IParticipatingSite.setTaggedValue('fti', 'jpl.mcl.site.knowledge.participatingsite')
