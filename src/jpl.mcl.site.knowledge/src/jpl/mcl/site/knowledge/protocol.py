# encoding: utf-8

u'''MCL — Protocol'''

from ._utils import getReferencedBrains
from Acquisition import aq_inner
from five import grok
from plone.memoize import view
from interfaces import IProtocol, IPerson, IPublication, IParticipatingSite, IOrgan


IProtocol.setTaggedValue('typeURI', u'https://cancer.jpl.nasa.gov/rdf/types.rdf#Protocol')
IProtocol.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': ('title', False),
    u'http://purl.org/dc/terms/abstract': ('description', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#humanSubjectTraining': ('humanSubjectTraining', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#sitecontact': ('sitecontact', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#irbcontact': ('irbcontact', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#startDate': ('startDate', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#irbapprovalnum': ('irbapprovalnum', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#irbapproval': ('irbapproval', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#organ': ('organ', True),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#pi': ('pi', True),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#custodian': ('custodian', True),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#publication': ('publication', True),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#site': ('site', True)
})
IProtocol.setTaggedValue('fti', 'jpl.mcl.site.knowledge.protocol')


class View(grok.View):
    u'''View for a protocol'''
    grok.context(IProtocol)
    grok.require('zope2.View')
    @view.memoize
    def pis(self):
        context = aq_inner(self.context)
        return getReferencedBrains(context.pi)
    @view.memoize
    def custodians(self):
        context = aq_inner(self.context)
        return getReferencedBrains(context.custodian)
    @view.memoize
    def organs(self):
        context = aq_inner(self.context)
        return getReferencedBrains(context.organ)
    @view.memoize
    def publications(self):
        context = aq_inner(self.context)
        return getReferencedBrains(context.publication)
    @view.memoize
    def sites(self):
        context = aq_inner(self.context)
        return getReferencedBrains(context.site)
