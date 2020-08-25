# encoding: utf-8

u'''MCL — Discipline'''

from zope import schema
from interfaces import IDiscipline


IDiscipline.setTaggedValue('predicateMap', {
    u'http://purl.org/dc/terms/title': ('title', False),
    u'http://purl.org/dc/terms/description': ('description', False)
})
IDiscipline.setTaggedValue('fti', 'jpl.mcl.site.knowledge.discipline')
IDiscipline.setTaggedValue('typeURI', u'https://cancer.jpl.nasa.gov/rdf/types.rdf#Discipline')
