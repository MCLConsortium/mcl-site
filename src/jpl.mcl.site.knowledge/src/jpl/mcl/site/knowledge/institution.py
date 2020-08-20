# encoding: utf-8

u'''MCL — Institution'''
from ._utils import getReferencedBrains
from Acquisition import aq_inner
from five import grok
from .interfaces import IPerson, IInstitution
from plone.memoize import view
import plone.api

IInstitution.setTaggedValue('typeURI', u'https://cancer.jpl.nasa.gov/rdf/types.rdf#Institution')
IInstitution.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': ('title', False),
    u'http://purl.org/dc/terms/description': ('description', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#department': ('department', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#abbreviatedName': ('abbreviation', False),
    u'http://xmlns.com/foaf/0.1/homepage': ('homepage', False),
    u'http://xmlns.com/foaf/0.1/member': ('members', True)
})
IInstitution.setTaggedValue('fti', 'jpl.mcl.site.knowledge.institution')


class View(grok.View):
    u'''View for an institution'''
    grok.context(IInstitution)
    grok.require('zope2.View')
    @view.memoize
    def members(self):
        context = aq_inner(self.context)
        return getReferencedBrains(context.members)
