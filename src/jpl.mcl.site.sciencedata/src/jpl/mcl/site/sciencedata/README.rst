This package provides knowledge content types and RDF ingestion for the
Molecular and Cellular Characterization of Screen-Detected Lesions.


Functional Tests
================

To demonstrate the code, we'll classes in a series of functional tests.  And
to do so, we'll need a test browser::

    >>> app = layer['app']
    >>> from plone.testing.z2 import Browser
    >>> from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
    >>> browser = Browser(app)
    >>> browser.handleErrors = False
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
    >>> portal = layer['portal']    
    >>> portalURL = portal.absolute_url()

Here we go.


Labcas Collections
==================

A sciencedata is an academic rank conferred by a college or university after
examination or after completion of a course of study, or conferred as an honor
on a distinguished person.  They go in Labcas Collection Folders, which can be added
anywhere:

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='jpl-mcl-site-sciencedata-sciencedatafolder')
    >>> l.url.endswith('++add++jpl.mcl.site.sciencedata.sciencedatafolder')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'My Labcas Collection Folder'
    >>> browser.getControl(name='form.widgets.description').value = u'Some of my favorite sciencedatas.'
    >>> browser.getControl(name='form.widgets.labcasurl').value = u'testscheme://localhost/rdf/labcas'
    >>> browser.getControl(name='form.widgets.labcas_sourceurl_prefix').value = u'testscheme://localhost/ui/labcas'
    >>> browser.getControl(name='form.widgets.ingestEnabled:list').value = False
    >>> browser.getControl(name='form.buttons.save').click()
    >>> 'my-labcas-collection-folder' in portal.keys()
    True

The folder is currently empty::

    >>> folder = portal['my-labcas-collection-folder']
    >>> len(folder.keys())
    0

Note that we've set ``ingestEnabled`` to ``False``.  So if we try to ingest
that folder, nothing will happen.  How do we start the ingest process?  By
visiting a view at the root of the site::

    >>> from plone.registry.interfaces import IRegistry
    >>> from zope.component import getUtility
    >>> registry = getUtility(IRegistry)
    >>> registry['jpl.mcl.site.sciencedata.interfaces.ISettings.objects'] = [u'my-labcas-collection-folder']
    >>> import transaction
    >>> transaction.commit()
    >>> browser.open(portalURL + '/@@ingestScienceData')

But since the sciencedata folder had ingest disabled, it's still empty::

    >>> len(folder.keys())
    0

So let's enable ingest and try again::

    >>> browser.open(portalURL + '/my-labcas-collection-folder/@@edit')
    >>> browser.getControl(name='form.widgets.ingestEnabled:list').value = True
    >>> browser.getControl(name='form.buttons.save').click()

Will need to add Solr ability to ingest testscheme schemas instead of just http. Tests incomplete
