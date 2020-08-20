# encoding: utf-8

u'''MCL — Publication'''

from interfaces import IPublication, IPerson
from ._utils import getReferencedBrains
from Acquisition import aq_inner
from zope.intid.interfaces import IIntIds
from five import grok

from plone.memoize import view


IPublication.setTaggedValue('typeURI', u'https://cancer.jpl.nasa.gov/rdf/types.rdf#Publication')
IPublication.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': ('title', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#year': ('year', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#author': ('author', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#pmid': ('pmid', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#pi': ('pi', True),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#journal': ('journal', False)
})
IPublication.setTaggedValue('fti', 'jpl.mcl.site.knowledge.publication')

class View(grok.View):
    u'''View for a Publication'''
    grok.context(IPublication)
    grok.require('zope2.View')
    @view.memoize
    def pis(self):
        context = aq_inner(self.context)
        return getReferencedBrains(context.pi)
