# encoding: utf-8

u'''JPL MCL Site Science Data — browser views — settings control panel.'''

from jpl.mcl.site.sciencedata import MESSAGE_FACTORY as _
from jpl.mcl.site.sciencedata.interfaces import ISettings
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm


class SettingsEditForm(RegistryEditForm):
    u'''Edit form for MCL Site Science Data settings control pannel.'''
    schema = ISettings
    label = _(u'Science Data Settings')
    description = _(u'Control panel settings for MCL Site Science Data.')


class SettingsControlPanel(ControlPanelFormWrapper):
    u'''The settings control panel itself'''
    form = SettingsEditForm
