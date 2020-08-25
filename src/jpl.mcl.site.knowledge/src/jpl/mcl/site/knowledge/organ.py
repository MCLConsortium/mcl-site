# encoding: utf-8

u'''MCL — Organ'''

from interfaces import IOrgan


IOrgan.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': ('title', False),
    u'http://purl.org/dc/terms/description': ('description', False)
})
IOrgan.setTaggedValue('fti', 'jpl.mcl.site.knowledge.organ')
IOrgan.setTaggedValue('typeURI', u'https://cancer.jpl.nasa.gov/rdf/types.rdf#Organ')
