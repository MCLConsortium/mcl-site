# encoding: utf-8

u'''JPL MCL Site Knowledge — browser views — settings control panel.'''

from jpl.mcl.site.knowledge import MESSAGE_FACTORY as _
from jpl.mcl.site.knowledge.interfaces import ISettings
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm


class SettingsEditForm(RegistryEditForm):
    u'''Edit form for MCL Site Knowledge settings control pannel.'''
    schema = ISettings
    label = _(u'Knowledge Settings')
    description = _(u'Control panel settings for MCL Site Knowledge.')


class SettingsControlPanel(ControlPanelFormWrapper):
    u'''The settings control panel itself'''
    form = SettingsEditForm
