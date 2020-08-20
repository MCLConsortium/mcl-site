# encoding: utf-8

u'''MCL — Degree'''

from interfaces import IDegree

IDegree.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': ('title', False),
    u'http://purl.org/dc/terms/description': ('description', False)
})
IDegree.setTaggedValue('fti', 'jpl.mcl.site.knowledge.degree')
IDegree.setTaggedValue('typeURI', u'https://cancer.jpl.nasa.gov/rdf/types.rdf#Degree')
