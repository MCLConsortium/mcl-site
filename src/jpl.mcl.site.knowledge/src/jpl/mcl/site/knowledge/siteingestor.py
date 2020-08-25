# encoding: utf-8

u'''MCL Site Knowledge — full site ingest of content from external data sources.'''

from ._utils import IngestResults
from .errors import IngestDisabled
from .interfaces import IIngestor
from datetime import datetime
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
import logging, transaction, plone.api


_logger = logging.getLogger(__name__)
_dawn = datetime(1970, 1, 1, 0, 0, 0, 0)


class SiteIngestor(grok.View):
    u'''A "view" that orders all knoweldge folders to update the content.'''
    grok.context(INavigationRoot)
    grok.name('ingestKnowledge')
    grok.require('cmf.ManagePortal')
    def update(self):
        self.request.set('disable_border', True)
        portal = plone.api.portal.get()
        # Plone/Zope needs some better way to do locking re-entrancy, but for now the best solution
        # seems to do long-running maintenance tasks in a second instance.  So, screw it for now.
        registry = getUtility(IRegistry)
        ingestStart = registry['jpl.mcl.site.knowledge.interfaces.ISettings.ingestStart']
        self.completeResults, self.skipped = IngestResults([], [], []), []
        if ingestStart and ingestStart > _dawn:
            self.ingestRunning, self.ingestStart = True, ingestStart
        else:
            try:
                registry['jpl.mcl.site.knowledge.interfaces.ISettings.ingestStart'] = datetime.now()
                transaction.commit()
                paths = registry['jpl.mcl.site.knowledge.interfaces.ISettings.objects']
                if not paths: return
                for path in paths:
                    folder = portal.unrestrictedTraverse(path.encode('utf-8'))
                    ingestor = IIngestor(folder)
                    try:
                        results = ingestor.ingest()
                        transaction.commit()
                        self.completeResults.created.extend(results.created)
                        self.completeResults.updated.extend(results.updated)
                        self.completeResults.deleted.extend(results.deleted)
                    except IngestDisabled:
                        self.skipped.append(folder)
            finally:
                self.ingestRunning = False
                registry['jpl.mcl.site.knowledge.interfaces.ISettings.ingestStart'] = _dawn
                self.completeResults.created.sort(lambda a, b: cmp(a.title, b.title))
                self.completeResults.updated.sort(lambda a, b: cmp(a.title, b.title))
                self.completeResults.deleted.sort()
                self.skipped.sort(lambda a, b: cmp(a.title, b.title))
                transaction.commit()
