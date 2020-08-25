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


Degrees
=======

A degree is an academic rank conferred by a college or university after
examination or after completion of a course of study, or conferred as an honor
on a distinguished person.  They go in Degree Folders, which can be added
anywhere:

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='jpl-mcl-site-knowledge-degreefolder')
    >>> l.url.endswith('++add++jpl.mcl.site.knowledge.degreefolder')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'My Degree Folder'
    >>> browser.getControl(name='form.widgets.description').value = u'Some of my favorite degrees.'
    >>> browser.getControl(name='form.widgets.url').value = u'testscheme://localhost/rdf/degrees1'
    >>> browser.getControl(name='form.widgets.ingestEnabled:list').value = False
    >>> browser.getControl(name='form.buttons.save').click()
    >>> 'my-degree-folder' in portal.keys()
    True

The folder is currently empty::

    >>> folder = portal['my-degree-folder']
    >>> len(folder.keys())
    0

Note that we've set ``ingestEnabled`` to ``False``.  So if we try to ingest
that folder, nothing will happen.  How do we start the ingest process?  By
visiting a view at the root of the site::

    >>> from plone.registry.interfaces import IRegistry
    >>> from zope.component import getUtility
    >>> registry = getUtility(IRegistry)
    >>> registry['jpl.mcl.site.knowledge.interfaces.ISettings.objects'] = [u'my-degree-folder']
    >>> import transaction
    >>> transaction.commit()
    >>> browser.open(portalURL + '/@@ingestKnowledge')

But since the degree folder had ingest disabled, it's still empty::

    >>> len(folder.keys())
    0

So let's enable ingest and try again::

    >>> browser.open(portalURL + '/my-degree-folder/@@edit')    
    >>> browser.getControl(name='form.widgets.ingestEnabled:list').value = True
    >>> browser.getControl(name='form.buttons.save').click()
    >>> browser.open(portalURL + '/@@ingestKnowledge')

And did it work?

    >>> browser.contents
    '...Ingest Complete...Objects Created (2)...'
    >>> len(folder.keys())
    2
    >>> keys = folder.keys()
    >>> keys.sort()
    >>> keys
    ['mph', 'phd']
    >>> mph = folder['mph']
    >>> mph.title
    u'MPH'
    >>> mph.description
    u'Master Public Health'
    >>> mph.subjectURI
    u'https://cancer.jpl.nasa.gov/ksdb/degreeinput/?id=2'
    >>> phd = folder['phd']
    >>> phd.title
    u'PhD'
    >>> phd.description
    u'Doctor of Philosophy'
    >>> phd.subjectURI
    u'https://cancer.jpl.nasa.gov/ksdb/degreeinput/?id=1'

Great!  Now let's see how we work in the face of alterations to data::

    >>> browser.open(portalURL + '/my-degree-folder/@@edit')    
    >>> browser.getControl(name='form.widgets.url').value = u'testscheme://localhost/rdf/degrees2'
    >>> browser.getControl(name='form.buttons.save').click()
    >>> browser.open(portalURL + '/@@ingestKnowledge')
    >>> browser.contents
    '...Ingest Complete...Objects Created (2)...Objects Updated (1)...'
    >>> len(folder.keys())
    3
    >>> keys = folder.keys()
    >>> keys.sort()
    >>> keys
    ['md', 'mph', 'phd-1']
    >>> md = folder['md']
    >>> md.title
    u'MD'
    >>> md.description
    u'Doctor of Medicine'
    >>> mph = folder['mph']
    >>> mph.description
    u'Master of Public Health'

Good, we got a new degree and an updated description to the MPH degree.  Now,
let's see what happens if a degree is deleted::

    >>> browser.open(portalURL + '/my-degree-folder/@@edit')    
    >>> browser.getControl(name='form.widgets.url').value = u'testscheme://localhost/rdf/degrees3'
    >>> browser.getControl(name='form.buttons.save').click()
    >>> browser.open(portalURL + '/@@ingestKnowledge')
    >>> browser.contents
    '...Ingest Complete...Objects Created (0)...Objects Updated (0)...Objects Deleted (1)...'
    >>> len(folder.keys())
    2
    >>> keys = folder.keys()
    >>> keys.sort()
    >>> keys
    ['md', 'mph']

Works great!


Organs
======

An organ is a system of the body.  They're pretty much identical to degrees in
that they have just titles and descriptions and go into organ folders::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='jpl-mcl-site-knowledge-organfolder')
    >>> l.url.endswith('++add++jpl.mcl.site.knowledge.organfolder')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'My Organ Folder'
    >>> browser.getControl(name='form.widgets.description').value = u'Some of my favorite organs.'
    >>> browser.getControl(name='form.widgets.url').value = u'testscheme://localhost/rdf/organs'
    >>> browser.getControl(name='form.widgets.ingestEnabled:list').value = True
    >>> browser.getControl(name='form.buttons.save').click()
    >>> 'my-organ-folder' in portal.keys()
    True
    >>> folder = portal['my-organ-folder']
    >>> folder.title
    u'My Organ Folder'
    >>> folder.description
    u'Some of my favorite organs.'
    >>> folder.url
    'testscheme://localhost/rdf/organs'
    >>> folder.ingestEnabled
    True

Let's ingest and see what we get::

    >>> registry['jpl.mcl.site.knowledge.interfaces.ISettings.objects'] = [u'my-degree-folder', u'my-organ-folder']
    >>> transaction.commit()
    >>> browser.open(portalURL + '/@@ingestKnowledge')
    >>> browser.contents
    '...Ingest Complete...Objects Created (2)...Objects Updated (0)...Objects Deleted (0)...'
    >>> len(folder.keys())
    2
    >>> keys = folder.keys()
    >>> keys.sort()
    >>> keys
    ['anus', 'spleen']
    >>> anus = folder['anus']
    >>> anus.title
    u'Anus'
    >>> anus.description
    u'The human anus is the external opening of the rectum.'

Works fine!


People
======

OK, let's try people::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='jpl-mcl-site-knowledge-personfolder')
    >>> l.url.endswith('++add++jpl.mcl.site.knowledge.personfolder')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'My Person Folder'
    >>> browser.getControl(name='form.widgets.description').value = u'Some of my favorite people.'
    >>> browser.getControl(name='form.widgets.url').value = u'testscheme://localhost/rdf/person'
    >>> browser.getControl(name='form.widgets.ingestEnabled:list').value = True
    >>> browser.getControl(name='form.buttons.save').click()
    >>> 'my-person-folder' in portal.keys()
    True
    >>> folder = portal['my-person-folder']
    >>> folder.title
    u'My Person Folder'
    >>> folder.description
    u'Some of my favorite people.'
    >>> folder.url
    'testscheme://localhost/rdf/person'
    >>> folder.ingestEnabled
    True

Let's ingest and see what we get::

    >>> registry['jpl.mcl.site.knowledge.interfaces.ISettings.objects'] = [u'my-degree-folder', u'my-organ-folder', u'my-person-folder']
    >>> transaction.commit()
    >>> browser.open(portalURL + '/@@ingestKnowledge')
    >>> browser.contents
    '...Ingest Complete...Objects Created (2)...Objects Updated (0)...Objects Deleted (0)...'
    >>> len(folder.keys())
    2
    >>> keys = folder.keys()
    >>> keys.sort()
    >>> keys
    ['92346728-5e785b50', 'liu-beverley']
    >>> liu = folder['liu-beverley']
    >>> liu.title
    u'Liu, Beverley'
    >>> liu.givenName
    u'Beverley'
    >>> liu.surname
    u'Liu'
    >>> degrees = [i.to_object.title for i in liu.degrees]
    >>> degrees.sort()
    >>> degrees
    [u'MD', u'MPH']
    >>> liu.email
    u'mailto:bl@mdanderson.org'
    >>> liu.phone
    u'+1 713 555 7856'

Works fine!


Institutions
============

Now let's exercise institutions::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='jpl-mcl-site-knowledge-institutionfolder')
    >>> l.url.endswith('++add++jpl.mcl.site.knowledge.institutionfolder')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'My Institutions Folder'
    >>> browser.getControl(name='form.widgets.description').value = u'Some of my favorite institutions.'
    >>> browser.getControl(name='form.widgets.url').value = u'testscheme://localhost/rdf/institution'
    >>> browser.getControl(name='form.widgets.ingestEnabled:list').value = True
    >>> browser.getControl(name='form.buttons.save').click()
    >>> 'my-institutions-folder' in portal.keys()
    True
    >>> folder = portal['my-institutions-folder']
    >>> folder.title
    u'My Institutions Folder'
    >>> folder.description
    u'Some of my favorite institutions.'
    >>> folder.url
    'testscheme://localhost/rdf/institution'
    >>> folder.ingestEnabled
    True

Let's ingest and see what we get::

    >>> registry['jpl.mcl.site.knowledge.interfaces.ISettings.objects'] = [u'my-degree-folder', u'my-organ-folder', u'my-person-folder', u'my-institutions-folder']
    >>> transaction.commit()
    >>> browser.open(portalURL + '/@@ingestKnowledge')
    >>> browser.contents
    '...Ingest Complete...Objects Created (2)...Objects Updated (0)...Objects Deleted (0)...'
    >>> len(folder.keys())
    2
    >>> keys = folder.keys()
    >>> keys.sort()
    >>> keys
    ['jet-propulsion-laboratory', 'national-cancer-institute']
    >>> jpl = folder['jet-propulsion-laboratory']
    >>> jpl.title
    u'Jet Propulsion Laboratory'
    >>> jpl.department
    u'Informatics Center'
    >>> jpl.description
    u'JPL is on the forefront of space exploration.'
    >>> jpl.abbreviation
    u'JPL'
    >>> jpl.homepage
    u'http://www.jpl.nasa.gov/'
    >>> members = [i.to_object.title for i in jpl.members]
    >>> members.sort()
    >>> members
    [u'Liu, Beverley', u'\u9234\u6728, \u5e78\u5b50']

That works great.

Funded Sites
============

Great, trying funded or participating sites::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='jpl-mcl-site-knowledge-participatingsitefolder')
    >>> l.url.endswith('++add++jpl.mcl.site.knowledge.participatingsitefolder')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'My Participating Sites Folder'
    >>> browser.getControl(name='form.widgets.description').value = u'Some of my favorite participating sites.'
    >>> browser.getControl(name='form.widgets.url').value = u'testscheme://localhost/rdf/participatingsite'
    >>> browser.getControl(name='form.widgets.ingestEnabled:list').value = True
    >>> browser.getControl(name='form.buttons.save').click()
    >>> 'my-participating-sites-folder' in portal.keys()
    True
    >>> folder = portal['my-participating-sites-folder']
    >>> folder.title
    u'My Participating Sites Folder'
    >>> folder.description
    u'Some of my favorite participating sites.'
    >>> folder.url
    'testscheme://localhost/rdf/participatingsite'
    >>> folder.ingestEnabled
    True

Let's ingest and see what we get::

    >>> registry['jpl.mcl.site.knowledge.interfaces.ISettings.objects'] = [u'my-degree-folder', u'my-organ-folder', u'my-person-folder', u'my-institutions-folder', u'my-participating-sites-folder']
    >>> transaction.commit()
    >>> browser.open(portalURL + '/@@ingestKnowledge')
    >>> browser.contents
    '...Ingest Complete...Objects Created (2)...Objects Updated (0)...Objects Deleted (0)...'
    >>> len(folder.keys())
    2
    >>> keys = folder.keys()
    >>> keys.sort()
    >>> keys
    ['dmcc', 'ic']
    >>> ic = folder['ic']
    >>> ic.title
    u'IC'
    >>> ic.description
    u'Informatics Center'
    >>> organs = [i.to_object.title for i in ic.organ]
    >>> organs.sort()
    >>> organs
    [u'Anus', u'Spleen']
    >>> staffs = [i.to_object.title for i in ic.staff]
    >>> staffs
    [u'\u9234\u6728, \u5e78\u5b50']
    >>> pis = [i.to_object.title for i in ic.pi]
    >>> pis
    [u'Liu, Beverley']
    >>> institutions = [i.to_object.title for i in ic.institution]
    >>> institutions
    [u'National Cancer Institute']

That works great.

Personnel
=========

This is same as person, unless this changes later, will skip for now...

Protocols
=========

Yippee, going for protocols::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='jpl-mcl-site-knowledge-protocolfolder')
    >>> l.url.endswith('++add++jpl.mcl.site.knowledge.protocolfolder')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'My Protocols Folder'
    >>> browser.getControl(name='form.widgets.description').value = u'Some of my favorite protocols.'
    >>> browser.getControl(name='form.widgets.url').value = u'testscheme://localhost/rdf/protocol'
    >>> browser.getControl(name='form.widgets.ingestEnabled:list').value = True
    >>> browser.getControl(name='form.buttons.save').click()
    >>> 'my-protocols-folder' in portal.keys()
    True
    >>> folder = portal['my-protocols-folder']
    >>> folder.title
    u'My Protocols Folder'
    >>> folder.description
    u'Some of my favorite protocols.'
    >>> folder.url
    'testscheme://localhost/rdf/protocol'
    >>> folder.ingestEnabled
    True

Let's ingest and see what we get::

    >>> registry['jpl.mcl.site.knowledge.interfaces.ISettings.objects'] = [u'my-degree-folder', u'my-organ-folder', u'my-person-folder', u'my-institutions-folder', u'my-participating-sites-folder', u'my-protocols-folder']
    >>> transaction.commit()
    >>> browser.open(portalURL + '/@@ingestKnowledge')
    >>> browser.contents
    '...Ingest Complete...Objects Created (2)...Objects Updated (0)...Objects Deleted (0)...'
    >>> len(folder.keys())
    2
    >>> keys = folder.keys()
    >>> keys.sort()
    >>> keys
    ['a-methylation-panel-for-bladder-cancer', 'ksdb-protocol']
    >>> ksdb = folder['ksdb-protocol']
    >>> ksdb.title
    u'KSDB Protocol'
    >>> ksdb.description
    u'ksdb abstract'
    >>> ksdb.irbapprovalnum
    u'1113232323'
    >>> organs = [i.to_object.title for i in ksdb.organ]
    >>> organs.sort()
    >>> organs
    [u'Anus', u'Spleen']
    >>> pis = [i.to_object.title for i in ksdb.pi]
    >>> pis.sort()
    >>> pis
    [u'Liu, Beverley', u'\u9234\u6728, \u5e78\u5b50']

That works great.

Publications
============

Finally, going for publications::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='jpl-mcl-site-knowledge-publicationfolder')
    >>> l.url.endswith('++add++jpl.mcl.site.knowledge.publicationfolder')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'My Publications Folder'
    >>> browser.getControl(name='form.widgets.description').value = u'Some of my favorite publications.'
    >>> browser.getControl(name='form.widgets.url').value = u'testscheme://localhost/rdf/publication'
    >>> browser.getControl(name='form.widgets.ingestEnabled:list').value = True
    >>> browser.getControl(name='form.buttons.save').click()
    >>> 'my-publications-folder' in portal.keys()
    True
    >>> folder = portal['my-publications-folder']
    >>> folder.title
    u'My Publications Folder'
    >>> folder.description
    u'Some of my favorite publications.'
    >>> folder.url
    'testscheme://localhost/rdf/publication'
    >>> folder.ingestEnabled
    True

Let's ingest and see what we get::

    >>> registry['jpl.mcl.site.knowledge.interfaces.ISettings.objects'] = [u'my-degree-folder', u'my-organ-folder', u'my-person-folder', u'my-institutions-folder', u'my-participating-sites-folder', u'my-protocols-folder', u'my-publications-folder']
    >>> transaction.commit()
    >>> browser.open(portalURL + '/@@ingestKnowledge')
    >>> browser.contents
    '...Ingest Complete...Objects Created (2)...Objects Updated (0)...Objects Deleted (0)...'
    >>> len(folder.keys())
    2
    >>> keys = folder.keys()
    >>> keys.sort()
    >>> keys
    ['test-publication-1', 'test-publication-2']
    >>> pub = folder['test-publication-1']
    >>> pub.title
    u'Test Publication 1'
    >>> pub.pmid
    u'20864512'
    >>> pub.year
    2006L
    >>> pub.journal
    u'Cancer Prev Res (Phil)'
    >>> authors = pub.author
    >>> authors.sort()
    >>> authors
    [u'Fang H', u'Jiang F', u'Li R', u'Stass SA.', u'Todd NW', u'Zhang H']

That works great.

Species
============

Finally, going for species::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='jpl-mcl-site-knowledge-speciesfolder')
    >>> l.url.endswith('++add++jpl.mcl.site.knowledge.speciesfolder')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'My Species Folder'
    >>> browser.getControl(name='form.widgets.description').value = u'Some of my favorite species.'
    >>> browser.getControl(name='form.widgets.url').value = u'testscheme://localhost/rdf/species'
    >>> browser.getControl(name='form.widgets.ingestEnabled:list').value = True
    >>> browser.getControl(name='form.buttons.save').click()
    >>> 'my-species-folder' in portal.keys()
    True
    >>> folder = portal['my-species-folder']
    >>> folder.title
    u'My Species Folder'
    >>> folder.description
    u'Some of my favorite species.'
    >>> folder.url
    'testscheme://localhost/rdf/species'
    >>> folder.ingestEnabled
    True

Let's ingest and see what we get::

    >>> registry['jpl.mcl.site.knowledge.interfaces.ISettings.objects'] = [u'my-degree-folder', u'my-organ-folder', u'my-person-folder', u'my-institutions-folder', u'my-participating-sites-folder', u'my-protocols-folder', u'my-publications-folder', u'my-species-folder']
    >>> transaction.commit()
    >>> browser.open(portalURL + '/@@ingestKnowledge')
    >>> browser.contents
    '...Ingest Complete...Objects Created (2)...Objects Updated (2)...Objects Deleted (0)...'
    >>> len(folder.keys())
    2
    >>> keys = folder.keys()
    >>> keys.sort()
    >>> keys
    ['test-species-1', 'test-species-2']
    >>> spe = folder['test-species-1']
    >>> spe.title
    u'Test Species 1'
    >>> spe.description
    u'Test Species description 1'

That works great.

Discipline
============

Finally, going for discipline::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='jpl-mcl-site-knowledge-disciplinefolder')
    >>> l.url.endswith('++add++jpl.mcl.site.knowledge.disciplinefolder')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'My Discipline Folder'
    >>> browser.getControl(name='form.widgets.description').value = u'Some of my favorite discipline.'
    >>> browser.getControl(name='form.widgets.url').value = u'testscheme://localhost/rdf/discipline'
    >>> browser.getControl(name='form.widgets.ingestEnabled:list').value = True
    >>> browser.getControl(name='form.buttons.save').click()
    >>> 'my-discipline-folder' in portal.keys()
    True
    >>> folder = portal['my-discipline-folder']
    >>> folder.title
    u'My Discipline Folder'
    >>> folder.description
    u'Some of my favorite discipline.'
    >>> folder.url
    'testscheme://localhost/rdf/discipline'
    >>> folder.ingestEnabled
    True

Let's ingest and see what we get::

    >>> registry['jpl.mcl.site.knowledge.interfaces.ISettings.objects'] = [u'my-degree-folder', u'my-organ-folder', u'my-person-folder', u'my-institutions-folder', u'my-participating-sites-folder', u'my-protocols-folder', u'my-publications-folder', u'my-species-folder', u'my-discipline-folder']
    >>> transaction.commit()
    >>> browser.open(portalURL + '/@@ingestKnowledge')
    >>> browser.contents
    '...Ingest Complete...Objects Created (2)...Objects Updated (2)...Objects Deleted (0)...'
    >>> len(folder.keys())
    2
    >>> keys = folder.keys()
    >>> keys.sort()
    >>> keys
    ['test-discipline-1', 'test-discipline-2']
    >>> dis = folder['test-discipline-1']
    >>> dis.title
    u'Test Discipline 1'
    >>> dis.description
    u'Test Discipline description 1'

That works great.

Specimen Type
============

Finally, going for specimentype::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='jpl-mcl-site-knowledge-specimentypefolder')
    >>> l.url.endswith('++add++jpl.mcl.site.knowledge.specimentypefolder')
    True
    >>> l.click()
    >>> browser.getControl(name='form.widgets.title').value = u'My Specimen Type Folder'
    >>> browser.getControl(name='form.widgets.description').value = u'Some of my favorite specimentype.'
    >>> browser.getControl(name='form.widgets.url').value = u'testscheme://localhost/rdf/specimentype'
    >>> browser.getControl(name='form.widgets.ingestEnabled:list').value = True
    >>> browser.getControl(name='form.buttons.save').click()
    >>> 'my-specimen-type-folder' in portal.keys()
    True
    >>> folder = portal['my-specimen-type-folder']
    >>> folder.title
    u'My Specimen Type Folder'
    >>> folder.description
    u'Some of my favorite specimentype.'
    >>> folder.url
    'testscheme://localhost/rdf/specimentype'
    >>> folder.ingestEnabled
    True

Let's ingest and see what we get::

    >>> registry['jpl.mcl.site.knowledge.interfaces.ISettings.objects'] = [u'my-degree-folder', u'my-organ-folder', u'my-person-folder', u'my-institutions-folder', u'my-participating-sites-folder', u'my-protocols-folder', u'my-publications-folder', u'my-species-folder', u'my-discipline-folder', u'my-specimen-type-folder']
    >>> transaction.commit()
    >>> browser.open(portalURL + '/@@ingestKnowledge')
    >>> browser.contents
    '...Ingest Complete...Objects Created (2)...Objects Updated (2)...Objects Deleted (0)...'
    >>> len(folder.keys())
    2
    >>> keys = folder.keys()
    >>> keys.sort()
    >>> keys
    ['test-specimen-type-1', 'test-specimen-type-2']
    >>> spe = folder['test-specimen-type-1']
    >>> spe.title
    u'Test Specimen Type 1'
    >>> spe.description
    u'Test Specimen Type description 1'

That works great.
