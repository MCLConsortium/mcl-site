# encoding: utf-8

u'''MCL — Discipline Folder'''

from ._base import IIngestableFolder, Ingestor, IngestableFolderView
from .interfaces import IDiscipline
from five import grok


class IDisciplineFolder(IIngestableFolder):
    u'''Folder containing disciplines.'''


class DisciplineIngestor(Ingestor):
    u'''RDF ingestor for disciplines.'''
    grok.context(IDisciplineFolder)
    def getContainedObjectInterface(self):
        return IDiscipline


class View(IngestableFolderView):
    u'''View for an discipline folder'''
    grok.context(IDisciplineFolder)
