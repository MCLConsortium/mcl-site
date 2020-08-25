# encoding: utf-8

u'''JPL MCL Site Science Data — setup handlers.'''

from ._utils import publish
from plone.dexterity.utils import createContentInContainer
from plone.registry.interfaces import IRegistry
from ZODB.DemoStorage import DemoStorage
from zope.component import getUtility

import socket, logging

_logger = logging.getLogger(__name__)


# There has to be a better way of doing this:
if socket.gethostname() == 'tumor.jpl.nasa.gov' or socket.gethostname().endswith('.local'):
    _logger.warn(u'Using development solr on labcas-dev instead of labcas production')
    _solrBaseURL = u'https://mcl-labcas.jpl.nasa.gov/solr/'
    #_labcasBaseURL = u'https://labcas-dev.jpl.nasa.gov/ui/c/'
    #temporarily using labcas production instead of development
    _labcasBaseURL = u'https://mcl-labcas.jpl.nasa.gov/ui/c/'
else:
    _solrBaseURL = u'https://mcl-labcas.jpl.nasa.gov/solr/'
    _labcasBaseURL = u'https://mcl-labcas.jpl.nasa.gov/ui/c/'


def createScienceDataFolders(setupTool):
    if setupTool.readDataFile('jpl.mcl.site.sciencedata.txt') is None: return
    portal = setupTool.getSite()
    # Don't bother if we're running in the test fixture
    if hasattr(portal._p_jar, 'db') and isinstance(portal._p_jar.db().storage, DemoStorage): return
    if 'science-data' in portal.keys():
        portal.manage_delObjects('science-data')
    sciencedata = createContentInContainer(
        portal, 'jpl.mcl.site.sciencedata.sciencedatafolder', title=u'Science Data',
        description=u"MCL's Science Data Environment",
        labcasurl=_solrBaseURL + u'collections', labcas_sourceurl_prefix=_labcasBaseURL , ingestEnabled=True
    )
    publish(sciencedata)
    registry = getUtility(IRegistry)

    registry['jpl.mcl.site.sciencedata.interfaces.ISettings.objects'] = [
        u'science-data'
    ]
