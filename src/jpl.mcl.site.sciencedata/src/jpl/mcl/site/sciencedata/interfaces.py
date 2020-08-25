# encoding: utf-8

u'''MCL Site Knowledge — interfaces.'''

from . import MESSAGE_FACTORY as _
from zope import schema
from zope.interface import Interface


class IIngestor(Interface):
    u'''Interface for objects that are ingestors.'''
    def ingest():
        u'''Ingest data from your RDF source and populate your items.  Returns an IngestResults object.'''


class ISettings(Interface):
    u'''Schema for MCL Site Knowledge settings control panel.'''
    ingestEnabled = schema.Bool(
        title=_(u'Enable Ingest'),
        description=_(u'True (checked) if global RDF ingest is enabled'),
        required=False,
    )
    ingestStart = schema.Datetime(
        title=_(u'Start Time'),
        description=_(u"If value appears, this indicates the time an active ingest started. You won't need to set this."),
        required=False,
    )
    objects = schema.List(
        title=_(u'Objects'),
        description=_(u'Paths to objects that should be ingested.'),
        required=False,
        value_type=schema.TextLine(
            title=_(u'Object'),
            description=_(u'Path to an object whose contents should be ingested.')
        )
    )
