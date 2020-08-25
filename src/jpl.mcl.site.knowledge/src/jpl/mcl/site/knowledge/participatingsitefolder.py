# encoding: utf-8

u'''MCL — ParticipatingSite Folder'''

from ._base import IIngestableFolder, Ingestor, IngestableFolderView
from .interfaces import IParticipatingSite
from five import grok


class IParticipatingSiteFolder(IIngestableFolder):
    u'''Folder containing participating sites.'''


class ParticipatingSiteIngestor(Ingestor):
    u'''RDF ingestor for pariticipating sites.'''
    grok.context(IParticipatingSiteFolder)
    def getContainedObjectInterface(self):
        return IParticipatingSite


class View(IngestableFolderView):
    u'''View for an participating site folder'''
    grok.context(IParticipatingSiteFolder)
