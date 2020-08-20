# encoding: utf-8

u'''MCL — Group Folder'''

from ._base import IIngestableFolder, Ingestor, IngestableFolderView
from .interfaces import IGroup
from five import grok


class IGroupFolder(IIngestableFolder):
    u'''Folder containing working groups.'''


class GroupIngestor(Ingestor):
    u'''RDF ingestor for working groups.'''
    grok.context(IGroupFolder)
    def getContainedObjectInterface(self):
        return IGroup


class View(IngestableFolderView):
    u'''View for an working group folder'''
    grok.context(IGroupFolder)
