# encoding: utf-8

u'''MCL — Disease Folder'''

from ._base import IIngestableFolder, Ingestor, IngestableFolderView
from .interfaces import IDisease
from five import grok


class IDiseaseFolder(IIngestableFolder):
    u'''Folder containing diseases.'''


class DiseaseIngestor(Ingestor):
    u'''RDF ingestor for diseases.'''
    grok.context(IDiseaseFolder)
    def getContainedObjectInterface(self):
        return IDisease


class View(IngestableFolderView):
    u'''View for an disease folder'''
    grok.context(IDiseaseFolder)
