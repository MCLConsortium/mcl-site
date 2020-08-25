# encoding: utf-8

u'''MCL — Disease'''

from interfaces import IDisease

IDisease.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': ('title', False),
    u'http://purl.org/dc/terms/description': ('description', False)
})
IDisease.setTaggedValue('fti', 'jpl.mcl.site.knowledge.disease')
IDisease.setTaggedValue('typeURI', u'https://cancer.jpl.nasa.gov/rdf/types.rdf#Disease')
