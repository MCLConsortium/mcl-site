# encoding: utf-8

u'''MCL — Degree Folder'''

from ._base import IIngestableFolder, Ingestor, IngestableFolderView
from .interfaces import IDegree
from five import grok


class IDegreeFolder(IIngestableFolder):
    u'''Folder containing academic degrees.'''


class DegreeIngestor(Ingestor):
    u'''RDF ingestor for academic degrees.'''
    grok.context(IDegreeFolder)
    def getContainedObjectInterface(self):
        return IDegree


class View(IngestableFolderView):
    u'''View for an degree folder'''
    grok.context(IDegreeFolder)
