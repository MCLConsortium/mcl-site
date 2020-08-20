# encoding: utf-8

u'''MCL — Protocol Folder'''

from ._base import IIngestableFolder, Ingestor, IngestableFolderView
from .interfaces import IProtocol
from five import grok


class IProtocolFolder(IIngestableFolder):
    u'''Folder containing protocols.'''


class ProtocolIngestor(Ingestor):
    u'''RDF ingestor for protocol.'''
    grok.context(IProtocolFolder)
    def getContainedObjectInterface(self):
        return IProtocol


class View(IngestableFolderView):
    u'''View for an protocol folder'''
    grok.context(IProtocolFolder)
