#!/usr/bin/env python
# encoding: utf-8
# Copyright 020 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from jpl.mcl.site.knowledge.interfaces import IIngestor
from plone.registry.interfaces import IRegistry
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.WorkflowCore import WorkflowException
from zope.component import getUtility
import sys, logging, transaction, plone.api, csv, codecs


logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
app = globals().get('app', None)  # ``app`` comes from ``instance run`` magic.


# From https://docs.python.org/2/library/csv.html
class UTF8Recoder(object):
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


# From https://docs.python.org/2/library/csv.html
class UnicodeReader(object):
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


def _publish(context, workflowTool=None):
    try:
        if workflowTool is None: workflowTool = plone.api.portal.get_tool('portal_workflow')
        workflowTool.doActionFor(context, action='publish')
        context.reindexObject()
    except WorkflowException:
        pass
    if IFolderish.providedBy(context):
        for itemID, subItem in context.contentItems():
            _publish(subItem, workflowTool)


def _ingest(portal):
    u'''Do an RDF ingest of all of the folders listed in the registry key
    ``eke.knowledge.ingest.IPanel.objects`` regardless of whether ingest is on or off.
    '''
    registry = getUtility(IRegistry)
    paths = registry['jpl.mcl.site.knowledge.interfaces.ISettings.objects']
    if not paths:
        logging.warn(u'No objects set in registry key jpl.mcl.site.knowledge.interfaces.ISettings.objects; nothing to do')
        return
    else:
        logging.warn(u'About to ingest from the following: %r', paths)
    for path in paths:
        if not path: continue
        logging.info(u'Ingesting %s', path)
        folder = portal.unrestrictedTraverse(path.encode('utf-8'))
        try:
            ingestor = IIngestor(folder)
            ingestor.ingest()
            transaction.commit()
        except TypeError:
            logging.info(u"Can't adapt IIngestor to folder at path %s; skipping", path)

    # Make sure everything is indexed so they appear where they need to be
    logging.info('Clearing and rebuilding the catalog')
    catalog = plone.api.portal.get_tool('portal_catalog')
    catalog.clearFindAndRebuild()
    logging.info('DONE')
    # At this point we could disable ingest which is safer in most cases but we'll leave it be for now


def _main(app):
    # Run this with ``bin/zope-debug -O mcl run $PWD/support/ingest.py``
    portal = app['mcl']
    _ingest(portal)
    transaction.commit()
    return True


def main(argv):
    try:
        global app
        _main(app)
    except Exception as ex:
        logging.exception(u'This is most unfortunate: %s', unicode(ex))
        return False
    return True


if __name__ == '__main__':
    # The [2:] works around plone.recipe.zope2instance-4.2.6's lame bin/interpreter script issue
    sys.exit(0 if main(sys.argv[2:]) is True else -1)
