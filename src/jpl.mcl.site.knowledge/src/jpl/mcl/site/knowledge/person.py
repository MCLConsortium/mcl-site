# encoding: utf-8

u'''MCL — Person'''
from ._utils import getReferencedBrains
from Acquisition import aq_inner
from zope.component import getUtility
from .interfaces import IPerson, IDegree, IInstitution
from zope.intid.interfaces import IIntIds
from five import grok

from plone.memoize import view
import plone.api
from Products.CMFCore.utils import getToolByName

FOAF_SURNAME = u'http://xmlns.com/foaf/0.1/surname'
FOAF_GIVENNAME = u'http://xmlns.com/foaf/0.1/givenname'

IPerson.setTaggedValue('predicateMap', {
    FOAF_SURNAME: ('surname', False),
    FOAF_GIVENNAME: ('givenName', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#degree': ('degrees', True),
    u'http://xmlns.com/foaf/0.1/mbox': ('email', False),
    u'http://purl.org/dc/terms/description': ('description', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#has_dcp': ('dcpflag', False),
    u'https://cancer.jpl.nasa.gov/rdf/schema.rdf#has_dcb': ('dcbflag', False),
    u'http://xmlns.com/foaf/0.1/phone': ('phone', False)
})
IPerson.setTaggedValue('fti', 'jpl.mcl.site.knowledge.person')
IPerson.setTaggedValue('typeURI', u'https://cancer.jpl.nasa.gov/rdf/types.rdf#Person')

class View(grok.View):
    u'''View for a Person'''
    grok.context(IPerson)
    grok.require('zope2.View')
    @view.memoize
    def degrees(self):
        context = aq_inner(self.context)
        return getReferencedBrains(context.degrees)
    @view.memoize
    def institutions(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        intids = getUtility(IIntIds)
        myID = intids.getId(context)
        institutions = [i.getObject() for i in catalog(object_provides=IInstitution.__identifier__)]
        myInstitutions = []
        for i in institutions:
            for rel in i.members:
                if myID == rel.to_id:
                    myInstitutions.append(i)
        return myInstitutions
