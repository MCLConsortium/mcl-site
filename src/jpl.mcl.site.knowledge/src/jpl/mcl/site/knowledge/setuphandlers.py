# encoding: utf-8

u'''JPL MCL Site Knowledge — setup handlers.'''

from ._utils import publish, hideTab, rename, move
from plone.dexterity.utils import createContentInContainer
from plone.registry.interfaces import IRegistry
from ZODB.DemoStorage import DemoStorage
from zope.component import getUtility
import socket, logging, plone.api

_logger = logging.getLogger(__name__)


# There has to be a better way of doing this:
# MCL ID is currently 39 in KSDB
if socket.gethostname() == 'tumor.jpl.nasa.gov' or socket.gethostname().endswith('.local')  or socket.gethostname() == 'mcl-dev.jpl.nasa.gov':
    _logger.warn(u'Using development KSDB on edrn-dev.jpl.nasa.gov instead of production')
    _rdfBaseURL = u'https://edrn-dev.jpl.nasa.gov/ksdb/publishrdf/?filterby=program&filterval=1&rdftype='
else:
    _rdfBaseURL = u'https://mcl.jpl.nasa.gov/ksdb/publishrdf/?filterby=program&filterval=1&rdftype='


def createKnowledgeFolders(setupTool):
    if setupTool.readDataFile('jpl.mcl.site.knowledge.txt') is None: return
    portal = setupTool.getSite()
    # Don't bother if we're running in the test fixture
    if hasattr(portal._p_jar, 'db') and isinstance(portal._p_jar.db().storage, DemoStorage): return
    if 'resources' not in portal.keys():
        createContentInContainer(
            portal, 'Folder', title=u'Resources',
            description=u'Resources for MCL.'
        )

    if 'archive' not in portal.keys():
        createContentInContainer(
            portal, 'Folder', title=u'Archive',
            description=u'Archive for MCL.'
        )
        hideTab(portal['archive'])
    # Nuke resource folders not being used
    if 'datasets' in portal['resources'].keys():
        plone.api.content.delete(obj=portal['resources']['datasets'])
    if 'image-data' in portal['resources'].keys():
        plone.api.content.delete(obj=portal['resources']['image-data'])
    if 'pathology-data' in portal['resources'].keys():
        plone.api.content.delete(obj=portal['resources']['pathology-data'])

    if 'other-lists' not in portal['archive'].keys():
        createContentInContainer(
            portal['archive'], 'Folder', title=u'Other Lists',
            description=u'Other Lists for MCL.'
        )
    create_protocol_flag = True
    if 'protocols' in portal['resources'].keys():
        if not ('protocols' in portal['archive'].keys() or 'archived-protocols' in portal['archive'].keys()):
            #plone.api.content.delete(obj=portal['resources']['protocols'])
        #else:
            move(portal['resources']['protocols'], portal['archive'])
            rename(portal['archive']['protocols'], 'Archived Protocols')
        else:
            portal['resources']['protocols'].url = _rdfBaseURL + u'protocol'
            create_protocol_flag = False
    if create_protocol_flag:
        createContentInContainer(
            portal['resources'], 'jpl.mcl.site.knowledge.protocolfolder', title=u'Protocols', id=u'protocols',
            description=u'MCL Consortium studies',
            url=_rdfBaseURL + u'protocol', ingestEnabled=True
        )
    create_member_flag = True
    #members archived
    if 'members' in portal.keys():
        if not('members' in portal['archive'].keys() or 'archived-members' in portal['archive'].keys()):
            #plone.api.content.delete(obj=portal['members'])
            move(portal['members'], portal['archive'])
            rename(portal['archive']['members'], 'Archived Members')
        else:
            portal['members'].url = _rdfBaseURL + u'fundedsite'
            create_member_flag = False
    if create_member_flag:
        createContentInContainer(
            portal, 'jpl.mcl.site.knowledge.participatingsitefolder', title=u'Members', id=u'members',
            description=u'Hospitals, universities, and other institutions participating with MCL.',
            url=_rdfBaseURL + u'fundedsite', ingestEnabled=True
        )
    if 'publications' in portal['resources'].keys():
        if not('publications' in portal['archive'].keys() or 'archived-publications' in portal['archive'].keys()):
            #plone.api.content.delete(obj=portal['resources']['publications'])
        #else:
            move(portal['resources']['publications'], portal['archive'])
            rename(portal['archive']['publications'], 'Archived Publications')
    #Remove old publications folder to create new one
    publication = None
    if 'publications' not in portal.keys():
        #plone.api.content.delete(obj=portal['publications'])
        publication = createContentInContainer(
            portal, 'jpl.mcl.site.knowledge.publicationfolder', title=u'Publications', id='publications',
            description=u'Articles and other material published by the MCL Consortium.',
            url=_rdfBaseURL + u'publication', ingestEnabled=True
        )
    else:
        publication = portal['publications']
        portal['publications'].url = _rdfBaseURL + u'publication'

    if 'institutions' not in portal['archive']['other-lists'].keys():
        #plone.api.content.delete(obj=portal['archive']['other-lists']['institutions'])
        createContentInContainer(
            portal['archive']['other-lists'], 'jpl.mcl.site.knowledge.institutionfolder', title=u'Institutions', id=u'institutions',
            description=u'Universities, hospitals, and other institutions working with the consortium.',
            url=_rdfBaseURL + u'institution', ingestEnabled=True
        )
    else:
        portal['archive']['other-lists']['institutions'].url = _rdfBaseURL + u'institution'


    # working groups cannot be removed for some reason, so will just hide for now
    # [kelly/2017-05-01] THIS IS SO WEIRD
    if 'working-groups' in portal.keys():
        hideTab(portal['working-groups'])
    workingGroup = None
    if 'working-groups-new' not in portal.keys():
        #plone.api.content.delete(obj=portal['working-groups-new'])
        workingGroup = createContentInContainer(
            portal, 'jpl.mcl.site.knowledge.groupfolder', title=u'Working Groups', id='working-groups-new',
            description=u'Committees and other expert groups appointed to study and report on a particular areas and make recommendations to MCL based on findings.',
            url=_rdfBaseURL + u'group', ingestEnabled=True
        )
    else:
        portal['working-groups-new'].url = _rdfBaseURL + u'group'
        workingGroup = portal['working-groups-new']

    if 'organs' not in portal['archive']['other-lists'].keys():
        #plone.api.content.delete(obj=portal['archive']['other-lists']['organs'])
        createContentInContainer(
            portal['archive']['other-lists'], 'jpl.mcl.site.knowledge.organfolder', title=u'Organs',id='organs',
            description=u'Organs are collections of tissues joined in structural unit to serve a common function.',
            url=_rdfBaseURL + u'organ', ingestEnabled=True
        )
    else:
        portal['archive']['other-lists']['organs'].url = _rdfBaseURL + u'organ'

    if 'people' not in portal['resources'].keys():
        #plone.api.content.delete(obj=portal['resources']['people'])
        createContentInContainer(
            portal['resources'], 'jpl.mcl.site.knowledge.personfolder', title=u'People',id='people',
            description=u'Individuals working with and comprising the consortium.',
            url=_rdfBaseURL + u'person', ingestEnabled=True
        )
    else:
        portal['resources']['people'].url = _rdfBaseURL + u'person'

    if 'degrees' not in portal['archive']['other-lists'].keys():
        #plone.api.content.delete(obj=portal['archive']['other-lists']['degrees'])
        createContentInContainer(
            portal['archive']['other-lists'], 'jpl.mcl.site.knowledge.degreefolder', title=u'Degrees',id='degrees',
            description=u'Academic degrees are qualifications awarded on successful completion of courses of study.',
            url=_rdfBaseURL + u'degree', ingestEnabled=True
        )
    else:
        portal['archive']['other-lists']['degrees'].url = _rdfBaseURL + u'degree'

    if 'specimen-types' not in portal['archive']['other-lists'].keys():
        #plone.api.content.delete(obj=portal['archive']['other-lists']['specimen-types'])
        createContentInContainer(
            portal['archive']['other-lists'], 'jpl.mcl.site.knowledge.specimentypefolder', title=u'Specimen Types', id=u'specimen-types',
            description=u'Specimen Types being studied in MCL.',
            url=_rdfBaseURL + u'specimentype', ingestEnabled=True
        )
    else:
        portal['archive']['other-lists']['specimen-types'].url = _rdfBaseURL + u'specimentype'

    if 'species' not in portal['archive']['other-lists'].keys():
        #plone.api.content.delete(obj=portal['archive']['other-lists']['species'])
        createContentInContainer(
            portal['archive']['other-lists'], 'jpl.mcl.site.knowledge.speciesfolder', title=u'Species',id=u'species',
            description=u'Species being studied in MCL.',
            url=_rdfBaseURL + u'species', ingestEnabled=True
        )
    else:
        portal['archive']['other-lists']['species'].url = _rdfBaseURL + u'species'
        
    if 'disciplines' not in portal['archive']['other-lists'].keys():
        #plone.api.content.delete(obj=portal['archive']['other-lists']['disciplines'])
        createContentInContainer(
            portal['archive']['other-lists'], 'jpl.mcl.site.knowledge.disciplinefolder', title=u'Disciplines', id=u'disciplines',
            description=u'Disciplines being studied in MCL.',
            url=_rdfBaseURL + u'discipline', ingestEnabled=True
        )
    else:
        portal['archive']['other-lists']['disciplines'].url = _rdfBaseURL + u'discipline'

    if 'diseases' not in portal['archive']['other-lists'].keys():
        #plone.api.content.delete(obj=portal['archive']['other-lists']['diseases'])
        createContentInContainer(
            portal['archive']['other-lists'], 'jpl.mcl.site.knowledge.diseasefolder', title=u'Diseases',
            description=u'Diseases being studied in MCL.',
            url=_rdfBaseURL + u'disease', ingestEnabled=True
        )
    else:
        portal['archive']['other-lists']['diseases'].url = _rdfBaseURL + u'disease'

    publish(portal['resources'])
    publish(portal['members'])
    publish(workingGroup)
    publish(publication)

    registry = getUtility(IRegistry)

    registry['jpl.mcl.site.knowledge.interfaces.ISettings.objects'] = [
        u'archive/other-lists/organs',
        u'archive/other-lists/diseases',
        u'archive/other-lists/degrees',
        u'archive/other-lists/species',
        u'archive/other-lists/specimen-types',
        u'archive/other-lists/disciplines',
        u'resources/people',
        u'publications',
        u'archive/other-lists/institutions',
        u'members',
        u'resources/protocols',
        u'working-groups-new'
    ]
