***************************************************
 Adding New Types to the MCL Knowledge Environment
***************************************************

The MCL Knowledge Environment consists of various Dexterity_ content types for
the Plone_ content management system that runs the website for MCL_, the
Consortium for Molecular and Cellular Characterization of Screen-Detected
Lesions.

Although Plone is certainly capable of curating all of the objects of the
Knowledge Environment itself, some in the Informatics Center (IC_) are
frightened of NoSQL_-style databases like the kind used by Plone.  So we develop
not one but two knowledge environments:

1.  One for curating the objects in the environment, which we call KSDB,
    which can create, update, delete, and display the objects,
2.  One for displaying them to the public, which is the MCL site, which can
    also create, update, delete, and display the objects, but instead
    does so through RDF_.

This document tells you how to add new content types to the MCL Knowledge
Environment and set it up for RDF ingest.  It will use an example type:
institution.


Write the Test Case
===================

The first step in any Plone development (or in *any* development for that
matter) is to write the test case.  But first, you'll want to make sure you can
actually build and run the code, so do::

    $ git clone git@github.com:MCLConsortium/jpl.mcl.site.knowledge.git
    $ cd jpl.mcl.site.knowledge
    $ python2.7 bootstrap.py
    $ bin/buildout
    $ bin/test

The tests should all pass.  Now edit the file
``src/jpl/mcl/site/knowledge/README.rst`` and add the following functional
test *after* the tests for people::

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
        >>> browser.open(portalURL + '/@@ingestContent')
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
        >>> members = [i.title for i in jpl.members]
        >>> members.sort()
        >>> members
        [u'Liu, Beverley', u'\u9234\u6728, \u5e78\u5b50']

    That works great.

Now, re-run the tests and ensure they *fail*.  Why?  Well, if they succeed, then
we know that either the new test is incorrect or we already have implemented
institutions and forgot about it!  So run them::

    $ bin/test
    Running tests at level 1
    Running jpl.mcl.site.knowledge.testing.JPLMCLSiteKnowledgeLayer:FunctionalTesting tests:
    …
    LinkNotFoundError

Good.  But before we create the new content types, we'll also need some test RDF
data.  Make the file ``src/jpl/mcl/site/knowledge/tests/data/institution.rdf``
with the following content::

    <?xml version="1.0" encoding="UTF-8"?>
    <rdf:RDF xmlns:ns1="http://xmlns.com/foaf/0.1/" xmlns:ns2="http://purl.org/dc/terms/" xmlns:ns3="https://mcl.jpl.nasa.gov/rdf/schema.rdf#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
        <rdf:Description rdf:about="http://mcl.jpl.nasa.gov/ksdb/institution/1">
            <rdf:type rdf:resource="https://mcl.jpl.nasa.gov/rdf/types.rdf#Institution"/>
            <ns2:title>Jet Propulsion Laboratory</ns2:title>
            <ns2:description>JPL is on the forefront of space exploration.</ns2:description>
            <ns3:department>Informatics Center</ns3:department>
            <ns3:abbreviatedName>JPL</ns3:abbreviatedName>
            <ns1:homepage rdf:resource="http://www.jpl.nasa.gov/"/>
            <ns1:member rdf:resource="http://mcl.jpl.nasa.gov/ksdb/people/1"/>
            <ns1:member rdf:resource="http://mcl.jpl.nasa.gov/ksdb/people/2"/>
        </rdf:Description>
        <rdf:Description rdf:about="http://mcl.jpl.nasa.gov/ksdb/institution/2">
            <rdf:type rdf:resource="https://mcl.jpl.nasa.gov/rdf/types.rdf#Institution"/>
            <ns2:title>National Cancer Institute</ns2:title>
            <ns2:description>Killing cancer dead.</ns2:description>
            <ns3:department>Early Detection Research Network</ns3:department>
            <ns3:abbreviatedName>NCI</ns3:abbreviatedName>
            <ns1:homepage rdf:resource="http://cancer.gov/"/>
        </rdf:Description>
    </rdf:RDF>


Create the Container
====================

Institutions should all go into the same container, so the first step is to
create the institution folder schema.  Create the following file in
``src/jpl/mcl/site/knowledge/institutionfolder.py``::

    # encoding: utf-8

    u'''MCL — Institution Folder'''

    from ._base import IIngestableFolder, Ingestor, IngestableFolderView
    from .institution import IInstitution
    from five import grok


    class IInstitutionFolder(IIngestableFolder):
        u'''Folder containing institutions.'''


    class InstitutionIngestor(Ingestor):
        u'''RDF ingestor for instutitions.'''
        grok.context(IInstitutionFolder)
        def getContainedObjectInterface(self):
            return IInstitution


    class View(IngestableFolderView):
        u'''View for an institution folder'''
        grok.context(IInstitutionFolder)

You'll see that the superclass of ``IInstitutionFolder``, ``IIngestableFolder``,
provides all of the fields necessary.  In addition, the ``InstitutionIngestor``
gets all of the plumbing needed to ingest from ``Ingestor``, but you can
override methods of that class for custom ingest behavior.  Luckily for
institutions, we don't need to do that.  You'll also see that we have a custom
``View`` class for the institution folder, so that means we have to do this::

    $ mkdir src/jpl/mcl/site/knowledge/institutionfolder_templates

And in that directory, create a file ``view.pt`` with the following contents::

    <html
        xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'
        xmlns:tal='http://xml.zope.org/namespaces/tal'
        xmlns:metal='http://xml.zope.org/namespaces/metal'
        xmlns:i18n='http://xml.zope.org/namespaces/i18n'
        i18n:domain='jpl.mcl.site.knowledge'
        metal:use-macro='context/main_template/macros/master'>
        <head>
            <title>Institution Folder View</title>
        </head>
        <body>
            <metal:content-core fill-slot='content-core'>
                <metal:content-core define-macro='content-core' tal:define='isManager view/isManager'>
                    <p tal:condition='isManager' class='discreet callout'>
                        <label for='form-widgets-url' class='horizontal' i18n:translate='rdfURL'>
                            RDF URL:
                        </label>
                        <span id='form-widgets-url' class='uri-widget uri-field'>
                            <a href='#' tal:attributes='href context/url' tal:content='context/url'>
                                http://somewhere.com/some/rdf/source
                            </a>
                        </span>
                        <label for='form-widgets-ingestEnabled' class='horizontal'>
                            Ingest Enabled:
                        </label>
                        <span id='form-widgets-ingestEnabled' class='uri-widget uri-field'>
                            <span tal:omit-tag='' tal:condition='context/ingestEnabled' i18n:translate='ingestEnabled'>
                                &#x2705;
                            </span>
                            <span tal:omit-tag='' tal:condition='not:context/ingestEnabled'
                                i18n:translate='ingestNotEnabled'>
                                &#x1f6ab; This folder will <em>not</em> be updated
                            </span>
                        </span>
                        <br/>
                        <span i18n:translate='youAreAManager'>
                            You are seeing this because you are logged in with management privileges.
                        </span>
                    </p>
                    <table class='listing' summary='Listing of Institutions' i18n:attributes='summary'>
                        <thead>
                            <tr>
                                <th i18n:translate='institutionName'>Name</th>
                                <th i18n:translate='institutionHomePage'>Home Page</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tal:repeat repeat='row view/contents'>
                                <tr class='odd' tal:define='odd repeat/row/odd'
                                    tal:attributes='class python:u"odd" if odd else u"even"'>
                                    <td>
                                        <a href='#' tal:attributes='href row/getURL' tal:content='row/Title'>
                                            Blow, Joe
                                        </a>
                                    </td>
                                    <td>
                                        <a href='#' tal:attributes='href row/homepage' tal:content='row/homepage'>
                                            http://some.com/page
                                        </a>
                                    </td>
                                </tr>
                            </tal:repeat>
                        </tbody>
                    </table>
                </metal:content-core>
            </metal:content-core>
        </body>
    </html>

You'll notice that in the table, we're showing two items in each row:

1.  The first links to the institution object.
2.  The second links to the institution's home page.

Because of the second item, we're going to need an index and metadata column
on the "homepage" field in the portal catalog.


Add the New Index and Metadata Column
=====================================

Of course, the first thing we need is a test.  Unit testing will do.  Update
``src/jpl/mcl/site/knowledge/tests/test_setup.py`` and add this line to the end
of ``testCatalogIndexes``::

    self.assertTrue('homepage' in indexes, u'"homepage" index not installed')

And add this line to the end of ``testCatalogMetadata``::

    self.assertTrue('homepage' in columns, u'"homepage" column not installed')

Once again, re-run the tests with ``bin/test`` and ensure these tests fail.

Now we can add the index and metadata column to the portal catalog.  Edit the
file ``src/jpl/mcl/site/knowledge/profiles/default/catalog.xml`` and add these
entries::

    <index name='homepage' meta_type='FieldIndex'>
        <indexed_attr value='homepage'/>
    </index>
    <column value='homepage'/>

If you run the tests now, both unit tests ``testCatalogIndexes`` and
``testCatalogMetadata`` should pass.  Of course, the functional tests are still
failing, but we'll soon fix that.


Create the Institution Schema
=============================

We're almost done now.  We can go ahead and create the schema for the
institution content type.  Create the file
``src/jpl/mcl/site/knowledge/institution.py`` and fill it with the following::

    # encoding: utf-8

    u'''MCL — Institution'''

    from . import MESSAGE_FACTORY as _
    from ._base import IKnowledgeObject
    from person import IPerson
    from plone.app.vocabularies.catalog import CatalogSource
    from z3c.relationfield.schema import RelationChoice, RelationList
    from zope import schema


    class IInstitution(IKnowledgeObject):
        u'''An institution participating with the MCL consortium.'''
        title = schema.TextLine(
            title=_(u'Name'),
            description=_(u'Name of this institution.'),
            required=True
        )
        description = schema.Text(
            title=_(u'Description'),
            description=_(u'A short summary of this institution.'),
            required=False,
        )
        department = schema.TextLine(
            title=_(u'Department'),
            description=_(u'The specific department participating with MCL.'),
            required=False,
        )
        abbreviation = schema.TextLine(
            title=_(u'Abbreviation'),
            description=_(u'And abbreviated name or acronym to simplify identifying this institution.'),
            required=False,
        )
        homepage = schema.TextLine(
            title=_(u'Home Page'),
            description=_(u"URL to the site's home page."),
            required=False,
        )
        members = RelationList(
            title=_(u'Members'),
            description=_(u'People employed or consulting to this institution.'),
            required=False,
            default=[],
            value_type=RelationChoice(
                title=_(u'Member'),
                description=_(u'A single member of this institution.'),
                source=CatalogSource(object_provides=IPerson.__identifier__)
            )
        )


    IInstitution.setTaggedValue('typeURI', u'https://mcl.jpl.nasa.gov/rdf/types.rdf#Institution')
    IInstitution.setTaggedValue('predicateMap', {
        u'http://purl.org/dc/terms/title': ('title', False),
        u'http://purl.org/dc/terms/description': ('description', False),
        u'https://mcl.jpl.nasa.gov/rdf/schema.rdf#department': ('department', False),
        u'https://mcl.jpl.nasa.gov/rdf/schema.rdf#abbreviatedName': ('abbreviation', False),
        u'http://xmlns.com/foaf/0.1/homepage': ('homepage', False),
        u'http://xmlns.com/foaf/0.1/member': ('members', True)
    })
    IInstitution.setTaggedValue('fti', 'jpl.mcl.site.knowledge.institution')

The schema for ``IInstitution`` is straightforward Dexterity.  Where things get
interesting are the three tagged values we've added.  These are what bridge the
RDF to the Dexterity content type:

``typeURI``
    This indicates URI of the RDF type is that we want.
``predicateMap``
    The value for this is a mapping from RDF predicate URIs to a pairs
    of (field name, boolean).  For example, if we see the predicate URI
    ``https://mcl.jpl.nasa.gov/rdf/schema.rdf#abbreviatedName``, we know that
    maps to the ``abbreviation`` field in the Dexterity type.  The boolean
    tells us if we're dealing with a literal value field or a reference
    field.  If ``False``, then we set the literal value on the field.  If
    ``True``, then we search for the matching objects and *link* them
    the field.
``fti``
    This indicates the name of the type (factory type information) so the RDF
    ingest can create the correct Dexterity object.

Speaking of factory type information …


Create the Factory Type Information
===================================

Plone and the CMF need information registered in the portal types tool in order
create these new types.  To do that, first edit
``src/jpl/mcl/site/knowledge/profiles/default/types.xml`` and add these two
lines::

    <object name='jpl.mcl.site.knowledge.institution' meta_type='Dexterity FTI'/>
    <object name='jpl.mcl.site.knowledge.institutionfolder' meta_type='Dexterity FTI'/>

Then create the file ``src/jpl/mcl/site/knowledge/profiles/default/types/jpl.mcl.site.knowledge.institutionfolder.xml``
and fill it with the following::

    <?xml version='1.0' encoding='utf-8'?>
    <object name='jpl.mcl.site.knowledge.institutionfolder' meta_type='Dexterity FTI' i18n:domain='jpl.mcl.site.knowledge'
        xmlns:i18n='http://xml.zope.org/namespaces/i18n'>
        <property name='title' i18n:translate=''>Institution Folder</property>
        <property name='description' i18n:translate=''>A container for institutions</property>
        <property name='content_icon'>++resource++jpl.mcl.site.knowledge/institutionfolder.png</property>
        <property name='allow_discussion'>False</property>
        <property name='global_allow'>True</property>
        <property name='filter_content_types'>True</property>
        <property name='allowed_content_types'>
            <element value='jpl.mcl.site.knowledge.institution'/>
        </property>
        <property name='schema'>jpl.mcl.site.knowledge.institutionfolder.IInstitutionFolder</property>
        <property name='klass'>plone.dexterity.content.Container</property>
        <property name='add_permission'>cmf.AddPortalContent</property>
        <property name='behaviors'>
            <element value='plone.app.content.interfaces.INameFromTitle'/>
        </property>
        <property name='default_view'>view</property>
        <property name='default_view_fallback'>False</property>
        <property name='view_methods'>
            <element value='view'/>
        </property>
        <alias from='(Default)' to='(dynamic view)'/>
        <alias from='edit' to='@@edit'/>
        <alias from='sharing' to='@@sharing'/>
        <alias from='view' to='(selected layout)'/>
        <action title='View' action_id='view' category='object' condition_expr='' url_expr='string:${object_url}'
            visible='True'>
            <permission value='View'/>
        </action>
        <action title='Edit' action_id='edit' category='object' condition_expr='' url_expr='string:${object_url}/edit'
            visible='True'>
            <permission value='Modify portal content'/>
        </action>
    </object>

Note that this file references an icon named ``institutionfolder.png``.  Create
a 16×16 PNG format icon named that and put it in
``src/jpl/mcl/site/knowledge/static``.

Next, create the file ``src/jpl/mcl/site/knowledge/profiles/default/types/jpl.mcl.site.knowledge.institution.xml`` and fill it::

    <?xml version='1.0' encoding='utf-8'?>
    <object name='jpl.mcl.site.knowledge.institution' meta_type='Dexterity FTI' i18n:domain='jpl.mcl.site.knowledge'
        xmlns:i18n='http://xml.zope.org/namespaces/i18n'>
        <property name='title' i18n:translate=''>Institution</property>
        <property name='description' i18n:translate=''>An institution participating with MCL</property>
        <property name='content_icon'>++resource++jpl.mcl.site.knowledge/institution.png</property>
        <property name='allow_discussion'>False</property>
        <property name='global_allow'>False</property>
        <property name='filter_content_types'>True</property>
        <property name='allowed_content_types'/>
        <property name='schema'>jpl.mcl.site.knowledge.institution.IInstitution</property>
        <property name='klass'>plone.dexterity.content.Item</property>
        <property name='add_permission'>cmf.AddPortalContent</property>
        <property name='behaviors'>
            <element value='plone.app.content.interfaces.INameFromTitle'/>
        </property>
        <property name='default_view'>view</property>
        <property name='default_view_fallback'>False</property>
        <property name='view_methods'>
            <element value='view'/>
        </property>
        <alias from='(Default)' to='(dynamic view)'/>
        <alias from='edit' to='@@edit'/>
        <alias from='sharing' to='@@sharing'/>
        <alias from='view' to='(selected layout)'/>
        <action title='View' action_id='view' category='object' condition_expr='' url_expr='string:${object_url}'
            visible='True'>
            <permission value='View'/>
        </action>
        <action title='Edit' action_id='edit' category='object' condition_expr='' url_expr='string:${object_url}/edit'
            visible='True'>
            <permission value='Modify portal content'/>
        </action>
    </object>


You'll also need an ``institution.png`` icon.


Does It Work?
=============

At this point, we have everything in place to support the new content type,
display of the folder, and RDF ingest.  Let's see if it works::

    $ bin/test
    Running tests at level 1
    Running jpl.mcl.site.knowledge.testing.JPLMCLSiteKnowledgeLayer:FunctionalTesting tests:
    …
    Total: 3 tests, 0 failures, 0 errors, 0 skipped in 17.757 seconds.

It works!  But we're not quite yet finished.


Add-on Setup
============

When we install this add-on into a Plone site, it would be convenient if we
didn't have to hand-create an Institution Folder somewhere in the MCL site,
specify its name, the ingest URL, check the ingest enabled box, etc.  So, update
``src/jpl/mcl/site/knowledge/setuphandlers.py`` and add the following just
before the line that reads ``publish(knowledge)``::

    createContentInContainer(
        knowledge, 'jpl.mcl.site.knowledge.institutionfolder', title=u'Institutions',
        description=u'Universities, hospitals, and other institutions working with the consortium.',
        url=_rdfBaseURL + u'institution', ingestEnabled=True
    )

And update the assignment to
``registry['jpl.mcl.site.knowledge.interfaces.ISettings.objects']`` so that it
reads as follows::

    registry['jpl.mcl.site.knowledge.interfaces.ISettings.objects'] = [
        u'knowledge/organs',
        u'knowledge/degrees',
        u'knowledge/people',
        u'knowledge/institutions'
    ]

Now we can see if that works by starting up Zope and creating a new Plone site.
Run::

    $ bin/plone fg

to start the Zope application server.  Then visit http://localhost:8080/
with a browser.  You should see a button "Create a new Plone site", but *do not*
click it.  Instead:

1.  Click "Advanced"
2.  When prompted to log in, use username ``admin`` and password ``admin``
3.  Under "Add-ons", check the box by "MCL Site Knowledge"
4.  Click "Create Plone Site"

You should now have a standard Plone site, but with a "Knowledge" link on the
global navigation bar.  Click it and you should see your new "Institutions"
folder.  However, it's currently empty!  We actually need to do an ingest.

To start an RDF ingest, visit http://localhost:8080/Plone/@@ingestContent.

It will take a *long* time to create so many content objects and index them, but
after a while you should see a results page.  (Incidentally, this is how the
nightly ingest will work.  A cron job will visit that URL using
``/usr/bin/curl`` to start a fresh ingest every 24 hours.)

*Warning:* Don't visit ``@@ingestContent`` with the Safari web browser.  Safari
fetches URLs twice, once to generate a preview, and a second time to display
the page.  This will cause two ingests to start.  Now, the RDF ingest mechanism
has machinery in place to prevent this, but because the second fetch is what's
shown in the browser, you won't see the results in the ingest. You'll just see
a message saying an ingest is already running.

Once done, visit http://localhost:8080/Plone/knowledge/institutions and you
should see a number of fresh institutions.


Deploying to the Development Server
===================================

Now that everything works, update the ``docs/HISTORY.txt`` mentioning the new
institutions feature under the topmost "TBD" release.  You can then ``git
commit`` and ``git push`` to promulgate the changes to GitHub_.

Then, to see your updates in action at https://mcl-dev.jpl.nasa.gov/portal:

1.  Visit https://edrn-dev.jpl.nasa.gov/jenkins/
2.  Log in with your JPL username and password
3.  Click "MCL Portal"
4.  Click "Build Now"

Jenkins will pull in your new changes and build a fresh instance of the MCL
Portal.  When it's done:

1.  Visit https://mcl-dev.jpl.nasa.gov/portal
2.  Log in with your MCL username and password
3.  Then visit https://mcl-dev.jpl.nasa.gov/portal/@@ingestContent

After a while, check to see if all your neat new institutions appear.


Conclusion
==========

We've seen how to:

• Create a functional test for new content types
• Create a unit test for catalog indexes supporting the content types
• Build the container for the type and declare its custom view
• Update the portal catalog indexes and metadata columns
• Declare the schema for the type and connect it to the RDF ingest mechanism
• Declare the factory type information for our two new types
• Automate the setup of the knowledge environment folders
• Manually start an RDF ingest

Armed with this knowledge you should be able to complete the MCL Knowledge
Environment with publications, protocols, projects, and funded sites—as well as
any future knowledge published by KSDB.


.. References:
.. _Dexterity: http://docs.plone.org/external/plone.app.dexterity/docs/index.html
.. _Plone: https://plone.org/
.. _MCL: https://mcl.nci.nih.gov/
.. _IC: https://cancer.jpl.nasa.gov/
.. _NoSQL: http://nosql-database.org
.. _RDF: https://www.w3.org/RDF/
.. _GitHub: https://github.com/MCLConsortium/jpl.mcl.site.knowledge
