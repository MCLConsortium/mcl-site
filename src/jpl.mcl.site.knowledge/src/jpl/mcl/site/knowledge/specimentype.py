# encoding: utf-8

u'''MCL — SpecimenType'''

from interfaces import ISpecimenType

ISpecimenType.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': ('title', False),
    u'http://purl.org/dc/terms/description': ('description', False)
})
ISpecimenType.setTaggedValue('fti', 'jpl.mcl.site.knowledge.specimentype')
ISpecimenType.setTaggedValue('typeURI', u'https://cancer.jpl.nasa.gov/rdf/types.rdf#SpecimenType')
