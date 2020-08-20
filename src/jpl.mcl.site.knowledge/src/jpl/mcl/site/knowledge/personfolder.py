# encoding: utf-8

u'''MCL — Person Folder'''

from ._base import IIngestableFolder, Ingestor, IngestableFolderView
from .person import FOAF_SURNAME, FOAF_GIVENNAME
from .interfaces import IPerson
from five import grok
from rdflib import URIRef


class IPersonFolder(IIngestableFolder):
    u'''Folder containing people.'''


class PersonIngestor(Ingestor):
    u'''RDF ingestor for people.'''
    grok.context(IPersonFolder)
    def getContainedObjectInterface(self):
        return IPerson
    def getTitles(self, predicates):
        u'''We override this so we can generate a title from the person's names'''
        first = last = None                                               # Assume we have no names
        lasts = predicates.get(URIRef(FOAF_SURNAME))                      # Get all the last names
        firsts = predicates.get(URIRef(FOAF_GIVENNAME))                   # And all the first names
        if lasts and lasts[0]:                                            # Do we have at least one last name?
            last = unicode(lasts[0])                                      # Grab it
        if firsts and firsts[0]:                                          # Do we have at least one first name?
            first = unicode(firsts[0])                                    # Grab it
        if first and last:                                                # Did we get both a first & last name?
            return [u'{}, {}'.format(last, first)]                        # Let's get formal with LAST, FIRST!
        name = [i for i in (last, first) if i]                            # OK, let's get ANY name we can
        if name:                                                          # Got one?
            return name                                                   # Great, use it
        else:                                                             # Nope?
            return None                                                   # Nope.


class View(IngestableFolderView):
    u'''View for an organ folder'''
    grok.context(IPersonFolder)
