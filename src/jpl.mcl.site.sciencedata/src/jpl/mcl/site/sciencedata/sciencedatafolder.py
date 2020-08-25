# encoding: utf-8

u'''MCL — Sciencedata Folder'''

from ._base import IIngestableFolder, Ingestor, IngestableFolderView
from .sciencedata import ISciencedata
from five import grok


class ISciencedataFolder(IIngestableFolder):
    u'''Folder containing academic science data.'''


class SciencedataIngestor(Ingestor):
    u'''RDF ingestor for academic science data.'''
    grok.context(ISciencedataFolder)
    def getContainedObjectInterface(self):
        return ISciencedata


class View(IngestableFolderView):
    u'''View for an science data folder'''
    grok.context(ISciencedataFolder)
