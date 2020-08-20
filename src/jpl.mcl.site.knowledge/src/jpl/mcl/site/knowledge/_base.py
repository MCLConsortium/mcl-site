# encoding: utf-8

u'''MCL — Base classes'''

from . import MESSAGE_FACTORY as _
from ._utils import IngestResults, publish
from .errors import IngestDisabled, RDFTypeMismatchError, TitlePredicateMissing, IngestError
from .interfaces import IIngestor, IKnowledgeObject
from Acquisition import aq_inner
from five import grok
from plone.dexterity.utils import createContentInContainer
from plone.supermodel import model
from z3c.relationfield import RelationValue
from zope import schema
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
import rdflib, plone.api, logging


_logger = logging.getLogger(__name__)
DC_TITLE = rdflib.URIRef(u'http://purl.org/dc/terms/title')


class IIngestableFolder(model.Schema):
    u'''An abstract base class for folders whose content can be created via ingestion from RDF.'''
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'The name of this folder.'),
        required=True
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A brief description of this folder.'),
        required=False
    )
    url = schema.URI(
        title=_(u'RDF URL'),
        description=_(u'Uniform Resource Locator to the Resource Description Framework source of knowledge.'),
        required=True
    )
    ingestEnabled = schema.Bool(
        title=_(u'Ingest Enabled'),
        description=_(u'True if this folder should update its contents during routine ingest.'),
        required=False
    )


class IngestableFolderView(grok.View):
    grok.context(IIngestableFolder)
    grok.require('zope2.View')
    grok.baseclass()
    def isManager(self):
        context = aq_inner(self.context)
        membership = plone.api.portal.get_tool('portal_membership')
        return membership.checkPermission('Manage Portal', context)
    def contents(self):
        context = aq_inner(self.context)
        catalog = plone.api.portal.get_tool('portal_catalog')
        return catalog(path={'query': '/'.join(context.getPhysicalPath()), 'depth': 1}, sort_on='sortable_title')


class Ingestor(grok.Adapter):
    grok.provides(IIngestor)
    grok.context(IIngestableFolder)
    def getContainedObjectInterface(self):
        u'''Return the interface for objects that should be contained in the
        folder that this class adapts.'''
        raise NotImplementedError(u'Subclasses must implement getContainedObjectInterface')
    def getTitles(self, predicates):
        u'''Get the DC title from the given ``predicates``.  Subclasses may
        override this.'''
        return predicates.get(DC_TITLE)
    def _checkPredicates(self, predicates):
        u'''Check the given ``predicates`` to see if they make sense for the
        kinds of objects we'll be creating.  If not, raise an exception.  But
        if so, return the type's interface, the factory type info, the
        predicate map, and the object's title.'''
        iface          = self.getContainedObjectInterface()              # Content type's interface
        fti            = iface.getTaggedValue('fti')                     # Factory Type Information
        predicateMap   = iface.getTaggedValue('predicateMap')            # Mapping RDF predicate to content's field name
        desiredTypeURI = rdflib.URIRef(iface.getTaggedValue('typeURI'))  # RDF type URI that we want
        typeURI        = predicates[rdflib.RDF.term('type')][0]          # RDF type URI that we're given
        titles         = self.getTitles(predicates)                      # Get the object's title
        if typeURI != desiredTypeURI:                                    # Do we have the right RDF type?
            raise RDFTypeMismatchError(desiredTypeURI, typeURI)          # Nope, abort
        if not titles or not titles[0]:                                  # Do we have a title?
            raise TitlePredicateMissing()                                # Nope; everything MUST have a title
        return iface, fti, predicateMap, unicode(titles[0])              # Done!
    def _setValue(self, obj, fti, iface, predicate, predicateMap, values):
        u'''On the object ``obj`` set the field indicated by ``predicate``
        (which we can find via the ``predicateMap``) to the given ``values``.
        We can indicate a problem with the named ``fti`` and can access fields
        by the given ``iface``.
        '''
        catalog = plone.api.portal.get_tool('portal_catalog')
        fieldName, isRef = predicateMap[unicode(predicate)]
        if not values:
            _logger.info(
                u'For type %s we want predicate %s but not given; leaving %s un-set',
                fti, predicate, fieldName
            )
            return
        field = iface.get(fieldName)                                     # Get the field out of the content interface
        fieldBinding = field.bind(obj)                                   # Bind that field to the content object
        if isRef:                                                        # Is this a reference field?
            idUtil = getUtility(IIntIds)                                 # Get the intids utility
            items = [i.getObject() for i in catalog(subjectURI=values)]  # Find matching objects
            if len(items) != len(values):                                # Find them all?
                _logger.info(
                    u'For type %s predicate %s linked to %d URIs, but only %d found',
                    fti, predicate, len(values), len(items)
                )
            intids = [idUtil.getId(i) for i in items]                    # Go from matching objects to int ids
            rvs = [RelationValue(i) for i in intids]                     # And from int ids to RelationValues
            if schema.interfaces.ICollection.providedBy(field):          # Multi reference?
                fieldBinding.set(obj, rvs)                               # Yes, set them all
            elif len(items) > 0:                                         # Single reference and we have an item?
                fieldBinding.set(obj, rvs[0])                            # Set single value
        else:                                                            # It's a non-reference field
            if schema.interfaces.ICollection.providedBy(field):          # Is it multi valued?
                fieldBinding.validate(values)                            # Yes, validate all the values
                fieldBinding.set(obj, values)                            # And set all the values
            else:                                                        # No, it's not multi valued
                fieldBinding.validate(values[0])                         # Validate just one value
                fieldBinding.set(obj, values[0])                         # And set just one value
    def createObjects(self, context, uris, statements):
        u'''Create new objects in the ``context`` identified by ``uris`` and
        described in the ``statements``.  Return a sequence of those newly
        created objects. Subclasses may override this for special ingest
        needs.'''
        createdObjects = []
        # For each subject URI in the RDF
        for uri in uris:
            # Get the predicates for just that subject
            predicates = statements[uri]
            try:
                # Get the content type's interface, factory type info,
                # mapping of predicates to fields, and the title
                iface, fti, predicateMap, title = self._checkPredicates(predicates)
            except IngestError as ex:
                _logger.exception(u'Ingest error on %s: %r; skipping %s', u'/'.join(context.getPhysicalPath()), ex, uri)
                continue
            # Create a brand new content object
            obj = createContentInContainer(context, fti, title=title, subjectURI=unicode(uri))
            # Now set its fields
            for predicate in predicateMap:
                predicate = rdflib.URIRef(predicate)                      # Convert from string to URIRef
                if predicate == DC_TITLE:                                 # Is this the Dublin Core title?
                    continue                                              # We already set that, skip it
                values = predicates.get(predicate)                        # Get the values
                if not values: continue                                   # Skip if empty
                values = [i.toPython() for i in values]                   # Convert Literal+URIRefs to unicode
                try:
                    self._setValue(obj, fti, iface, predicate, predicateMap, values)
                except schema.ValidationError:
                    _logger.exception(u'Data "%r" for field %s invalid; skipping', values, predicate)
                    continue
            publish(obj)
            obj.reindexObject()
            createdObjects.append(obj)
        return createdObjects
    def updateObjects(self, context, uris, brains, statements):
        u'''Update those objects in ``context`` that have matching ``uris`` by
        using the ``statements`` to determine what needs updating.  To quickly
        find those objects, there's a lookup table ``brains`` that maps from
        subject URI to a portal catalog brain.  Subclasses may override this
        for special ingest needs.'''
        catalog = plone.api.portal.get_tool('portal_catalog')
        updatedObjects = []                                                                  # Start w/no updated objs
        for uri in uris:                                                                     # For each subject URI
            brain = brains[uri]                                                              # Get matching brain
            obj = brain.getObject()                                                          # Get matching object
            predicates = statements[uri]                                                     # Subject-specific preds
            objectUpdated = False                                                            # Assume no update
            iface, fti, predicateMap, title = self._checkPredicates(predicates)              # Get usual suspects
            for predicate, (fieldName, isRef) in predicateMap.iteritems():                   # For each pred+field name
                field = iface.get(fieldName)                                                 # Get the field
                fieldBinding = field.bind(obj)                                               # Bind it to the obj
                newValues = predicates.get(rdflib.URIRef(predicate), [])                     # Get new values
                newValues = [i.toPython() for i in newValues]                                # Literals to Python types
                if isRef:                                                                    # Is this a reference?
                    rvs = fieldBinding.get(obj)                                              # Get the RelationValues
                    paths = [i.to_path for i in rvs if i.to_path is not None]
                    matches = catalog(path={'query': paths, 'depth': 0})
                    currentRefs = [i['subjectURI'].decode('utf-8') for i in matches]
                    currentRefs.sort()                                                       # Sort 'em
                    newValues.sort()                                                         # Sort the new ones, too
                    if currentRefs != newValues:                                             # Any change?
                        self._setValue(obj, fti, iface, predicate, predicateMap, newValues)  # Yup, update
                        objectUpdated = True                                                 # We changed
                else:                                                                        # Literal field
                    currentValues = fieldBinding.get(obj)                                        # Get current values
                    if schema.interfaces.ICollection.providedBy(field):                          # Multi-valued field?
                        if currentValues != newValues:                                           # Values different?
                            self._setValue(obj, fti, iface, predicate, predicateMap, newValues)  # Yep, set new values
                            objectUpdated = True                                                 # We updated the obj
                    else:                                                                        # Single-valued field
                        if len(newValues) > 0:
                            if currentValues != newValues[0]:                                        # Value different?
                                self._setValue(obj, fti, iface, predicate, predicateMap, newValues)  # Set thew new value
                                objectUpdated = True                                                 # We updated the obj
            if objectUpdated:                                                                # Did we update the obj?
                obj.reindexObject()                                                          # Yep, reindex it
                updatedObjects.append(obj)                                                   # Add it to the list
        return updatedObjects                                                                # We updated these objs
    def ingest(self):
        u'''Ingest'''
        context = aq_inner(self.context)                                                     # Get our container
        if not context.ingestEnabled: raise IngestDisabled(context)                          # Do we ingest?
        catalog = plone.api.portal.get_tool('portal_catalog')                                # Get the catalog
        statements = self._readStatements(context.url)                                       # Read the RDF
        # Find out what we currently contain
        results = catalog(
            object_provides=IKnowledgeObject.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1)
        )
        # Make a lookup table from those current brains' subjectURIs to the brains
        existingBrains = {}
        for i in results:
            uri = i['subjectURI'].decode('utf-8')
            existingBrains[rdflib.URIRef(uri)] = i
        existingURIs   = set(existingBrains.keys())     # Set of currently existing URIs in the context
        statementURIs  = set(statements.keys())         # Set of URIs in the newly read RDF
        newURIs        = statementURIs - existingURIs   # Set of URIs for brand new objects
        deadURIs       = existingURIs - statementURIs   # Set of URIs for objects to delete
        updateURIs     = statementURIs & existingURIs   # Set of URIs for objects that may need to be updated
        newObjects     = self.createObjects(context, newURIs, statements)
        updatedObjects = self.updateObjects(context, updateURIs, existingBrains, statements)
        context.manage_delObjects([existingBrains[i]['id'].decode('utf-8') for i in deadURIs])
        return IngestResults(newObjects, updatedObjects, deadURIs)
    def _readStatements(self, url):
        u'''Read the statements made at the RDF at ``url`` and return a
        dictionary of {s → [{p → [o]}]} where ``s`` is a subject URI mapping
        to a sequence of dictionaries whose keys ``p`` are predicate URIs
        mapping to a sequence of ``o`` objects, which may be literal values
        or reference URIs.'''
        graph = rdflib.Graph()
        graph.parse(url)
        statements = {}
        for s, p, o in graph:
            if s not in statements:
                statements[s] = {}
            predicates = statements[s]
            if p not in predicates:
                predicates[p] = []
            predicates[p].append(o)
        return statements
