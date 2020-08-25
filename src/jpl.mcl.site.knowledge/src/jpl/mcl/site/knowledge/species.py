# encoding: utf-8

u'''MCL — Species'''

from interfaces import ISpecies

ISpecies.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': ('title', False),
    u'http://purl.org/dc/terms/description': ('description', False)
})
ISpecies.setTaggedValue('fti', 'jpl.mcl.site.knowledge.species')
ISpecies.setTaggedValue('typeURI', u'https://cancer.jpl.nasa.gov/rdf/types.rdf#Species')
