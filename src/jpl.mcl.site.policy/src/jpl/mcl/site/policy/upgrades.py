# encoding: utf-8

u'''MCL — custom upgrade steps.'''


from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import INavigationSchema
from Products.PluggableAuthService.interfaces.plugins import (
    IAuthenticationPlugin, IPropertiesPlugin, IUserAdderPlugin, IUserEnumerationPlugin, IRolesPlugin,
    IRoleEnumerationPlugin, IGroupsPlugin, IGroupEnumerationPlugin, ICredentialsResetPlugin
)
from Products.PlonePAS.interfaces.plugins import IUserManagement
from Products.PlonePAS.interfaces.group import IGroupManagement, IGroupIntrospection
from zope.component import getUtility
import plone.api, socket, logging, os


_logger = logging.getLogger(__name__)


# There has to be a better way of doing this:
if socket.gethostname() == 'tumor.jpl.nasa.gov' or socket.gethostname().endswith('.local') or socket.gethostname() == 'mcl-dev.jpl.nasa.gov':
    _rdfBaseURL = u'https://edrn-dev.jpl.nasa.gov/ksdb/publishrdf/?rdftype='
else:
    _rdfBaseURL = u'https://mcl.jpl.nasa.gov/ksdb/publishrdf/?rdftype='


def _getPortal(context):
    return getToolByName(context, 'portal_url').getPortalObject()


def nullUpgradeStep(context):
    u'''Null upgrade step does nothing for when no custom behavior is needed.'''
    pass


def installJPLMCLSiteKnowledge(context):
    u'''Install jpl.mcl.site.knowledge.'''
    qi = plone.api.portal.get_tool('portal_quickinstaller')
    qi.installProduct('jpl.mcl.site.knowledge')


def installJPLMCLSiteSciencedata(context):
    u'''Install jpl.mcl.site.sciencedata.'''
    qi = plone.api.portal.get_tool('portal_quickinstaller')
    qi.installProduct('jpl.mcl.site.sciencedata')


def orderFolderTabs(context):
    u'''order folder tabs in logical order'''
    portal = _getPortal(context)

    # Expose the correct folder tabs
    registry = getUtility(IRegistry)
    navigation_settings = registry.forInterface(INavigationSchema, prefix='plone')
    navigation_settings.displayed_types = ('Folder', 'jpl.mcl.site.knowledge.groupfolder', 'jpl.mcl.site.knowledge.participatingsitefolder', 'jpl.mcl.site.sciencedata.sciencedatafolder')

    # Members < Working Groups < Resources < News & Meetings < Science Data
    idx = 1
    for i in ('members', 'working-groups-new', 'resources', 'news-meetings', 'science-data'):
        portal.moveObject(i, idx)
        idx += 1
    ploneUtils = getToolByName(portal, 'plone_utils')
    ploneUtils.reindexOnReorder(portal)


def addPublicationTab(context):
    u'''add publication tabs and reorder logical order'''
    _logger.warn(u'Adding publications to MCL front page.')
    portal = _getPortal(context)

    # Expose the correct folder tabs
    registry = getUtility(IRegistry)
    navigation_settings = registry.forInterface(INavigationSchema, prefix='plone')
    navigation_settings.displayed_types = ('Folder', 'jpl.mcl.site.knowledge.groupfolder', 'jpl.mcl.site.knowledge.participatingsitefolder', 'jpl.mcl.site.sciencedata.sciencedatafolder', 'jpl.mcl.site.knowledge.publicationfolder')


def _setPluginOrder(plugins, interface, desiredOrder):
    _logger.debug('Setting plugin order for %r to %r', interface, desiredOrder)
    current = plugins[interface]
    toOrder = []
    for i in desiredOrder:
        if i in current:
            toOrder.append(i)
    plugins[interface] = tuple(toOrder)


def installLDAP(context):
    pass


def byeByePloneAppLDAP(context):
    # Uninstall the product
    # try:
    #     qi = plone.api.portal.get_tool('portal_quickinstaller')
    #     qi.uninstallProducts(['plone.app.ldap'])
    # Remove the 
    # But it left all this cruft!
    pass
