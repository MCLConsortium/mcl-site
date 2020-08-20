# encoding: utf-8

u'''MCL Site Knowledge — Errors.'''


class IngestError(Exception):
    u'''Abstract error during RDF ingest.'''
    def __init__(self, message):
        super(IngestError, self).__init__(message)


class IngestDisabled(IngestError):
    u'''Quasi-exceptional condition that indicates that ingest is turned off
    for a particular container.'''
    def __init__(self, obj):
        super(IngestDisabled, self).__init__(
            u'Ingest disabled for object {}'.format(u'/'.join(obj.getPhysicalPath()))
        )


class RDFTypeMismatchError(IngestError):
    u'''Error when RDF predicates indicate an RDF type that doesn't match the
    RDF type we're expecting.'''
    def __init__(self, expected, got):
        u'''Indicate an error with the ``expected`` type URI against the type
        URI we actually ``got``.'''
        super(RDFTypeMismatchError, self).__init__(
            u'Expected type URI {} but got {}'.format(expected, got)
        )


class TitlePredicateMissing(IngestError):
    u'''Error when a Dublin Core "title" predicate is absent.'''
    def __init__(self):
        super(TitlePredicateMissing, self).__init__(u'Dublin Core "title" term missing; it is required')
