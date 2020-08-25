# encoding: utf-8

u'''MCL — Institution Folder'''

from ._base import IIngestableFolder, Ingestor, IngestableFolderView
from .interfaces import IInstitution
from five import grok


class IInstitutionFolder(IIngestableFolder):
    u'''Folder containing institutions.'''


class InstitutionIngestor(Ingestor):
    u'''RDF ingestor for instutitions.'''
    grok.context(IInstitutionFolder)
    def getContainedObjectInterface(self):
        return IInstitution


class View(IngestableFolderView):
    u'''View for an institution folder'''
    grok.context(IInstitutionFolder)
