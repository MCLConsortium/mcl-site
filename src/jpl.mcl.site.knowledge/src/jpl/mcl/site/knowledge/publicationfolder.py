# encoding: utf-8

u'''MCL — Publication Folder'''

from ._base import IIngestableFolder, Ingestor, IngestableFolderView
from .interfaces import IPublication
from five import grok


class IPublicationFolder(IIngestableFolder):
    u'''Folder containing publications.'''


class PublicationIngestor(Ingestor):
    u'''RDF ingestor for publication.'''
    grok.context(IPublicationFolder)
    def getContainedObjectInterface(self):
        return IPublication


class View(IngestableFolderView):
    u'''View for an publication folder'''
    grok.context(IPublicationFolder)
