# encoding: utf-8

u'''MCL — Species Folder'''

from ._base import IIngestableFolder, Ingestor, IngestableFolderView
from .interfaces import ISpecies
from five import grok


class ISpeciesFolder(IIngestableFolder):
    u'''Folder containing species.'''


class SpeciesIngestor(Ingestor):
    u'''RDF ingestor for species.'''
    grok.context(ISpeciesFolder)
    def getContainedObjectInterface(self):
        return ISpecies


class View(IngestableFolderView):
    u'''View for an species folder'''
    grok.context(ISpeciesFolder)
