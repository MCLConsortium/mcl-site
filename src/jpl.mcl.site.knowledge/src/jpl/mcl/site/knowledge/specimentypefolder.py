# encoding: utf-8

u'''MCL — Specimen Type Folder'''

from ._base import IIngestableFolder, Ingestor, IngestableFolderView
from .interfaces import ISpecimenType
from five import grok


class ISpecimenTypeFolder(IIngestableFolder):
    u'''Folder containing specimentype.'''


class SpecimenTypeIngestor(Ingestor):
    u'''RDF ingestor for specimentype.'''
    grok.context(ISpecimenTypeFolder)
    def getContainedObjectInterface(self):
        return ISpecimenType


class View(IngestableFolderView):
    u'''View for an specimentype folder'''
    grok.context(ISpecimenTypeFolder)
