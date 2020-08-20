# encoding: utf-8

u'''MCL Site Knowledge — interfaces.'''

from . import MESSAGE_FACTORY as _
from zope import schema
from zope.interface import Interface
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.textfield import RichText


class IIngestor(Interface):
    u'''Interface for objects that are ingestors.'''
    def ingest():
        u'''Ingest data from your RDF source and populate your items.  Returns an IngestResults object.'''


class IKnowledgeObject(model.Schema):
    u'''An abstract base class for content that are identified by RDF subject URIs.'''
    subjectURI = schema.URI(
        title=_(u'Subject URI'),
        description=_(u"Uniform Resource Identifier that identifies the subject of this object.'"),
        required=True
    )

class ISettings(Interface):
    u'''Schema for MCL Site Knowledge settings control panel.'''
    ingestEnabled = schema.Bool(
        title=_(u'Enable Ingest'),
        description=_(u'True (checked) if global RDF ingest is enabled'),
        required=False,
    )
    ingestStart = schema.Datetime(
        title=_(u'Start Time'),
        description=_(u"If value appears, this indicates the time an active ingest started. You won't need to set this."),
        required=False,
    )
    objects = schema.List(
        title=_(u'Objects'),
        description=_(u'Paths to objects that should be ingested.'),
        required=False,
        value_type=schema.TextLine(
            title=_(u'Object'),
            description=_(u'Path to an object whose contents should be ingested.')
        )
    )
    
class IDegree(IKnowledgeObject):
    u'''An academic degree that a university typically confers upon an individual.'''
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'The name of this degree.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A brief description of this degree.'),
        required=False,
    )
    
class IPerson(IKnowledgeObject):
    u'''An individual member of the MCL consortium.'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Full name of this person.'),
        required=True
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this person.'),
        required=False,
    )
    surname = schema.TextLine(
        title=_(u'Surname'),
        description=_(u'Surname (family name, last name, etc.) of this person.'),
        required=False,
    )
    givenName = schema.TextLine(
        title=_(u'Given Name'),
        description=_(u'Given name (first name, etc.) of this person.'),
        required=False,
    )
    degrees = RelationList(
        title=_(u'Degrees'),
        description=_(u'Academic degrees conferred upon this person.'),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u'Degree'),
            description=_(u'A single academic degree conferred upon this person.'),
            source=CatalogSource(object_provides=IDegree.__identifier__)
        )
    )
    email = schema.TextLine(
        title=_(u'Email Address'),
        description=_(u'Electronic mail address via which this person may be contacted.'),
        required=False,
    )
    phone = schema.TextLine(
        title=_(u'Telephone Number'),
        description=_(u'Public switched telephone network number where this person may be called.'),
        required=False,
    )
    dcbflag = schema.Bool(
        title=_(u'Part of DCB?'),
        description=_(u'True (checked) if person is part of DCB Committee'),
        required=False,
    )
    dcpflag = schema.Bool(
        title=_(u'Part of DCP?'),
        description=_(u'True (checked) if person is part of DCP Committee'),
        required=False,
    )

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
        description=_(u'An abbreviated name or acronym to simplify identifying this institution.'),
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

class ISpecimenType(IKnowledgeObject):
    u'''An specimentype is a branch of knowledge studied under.'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Name of this specimentype.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A brief description of this specimentype.'),
        required=False,
    )
    
class ISpecies(IKnowledgeObject):
    u'''An species is a basic way to categorize living organisms.'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Name of this species.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A brief description of this species.'),
        required=False,
    )
    
class IOrgan(IKnowledgeObject):
    u'''An organ is a collection of tissues joined in a structural unit to serve a common function.'''
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'The name of this organ.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A brief description of this organ.'),
        required=False,
    )
    
class IDisease(IKnowledgeObject):
    u'''An disease is a collection of tissues joined in a structural unit to serve a common function.'''
    title = schema.TextLine(
        title=_(u'ICD10 Name'),
        description=_(u'ICD10 name of this disease.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A brief description of this disease.'),
        required=False,
    )
    
class IDiscipline(IKnowledgeObject):
    u'''An discipline is a branch of knowledge studied under.'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Name of this discipline.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A brief description of this discipline.'),
        required=False,
    )


class IGroup(IKnowledgeObject):
    u'''A working group participating with the MCL consortium.'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Name of this working group.'),
        required=True
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this working group.'),
        required=False,
    )
    members = RelationList(
        title=_(u'Members'),
        description=_(u'People employed or consulting to this group.'),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u'Member'),
            description=_(u'A single member of this group.'),
            source=CatalogSource(object_provides=IPerson.__identifier__)
        )
    )
    chairs = RelationList(
        title=_(u'Chair(s)'),
        description=_(u'Chair(s) of this group.'),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u'Chair'),
            description=_(u'A single chair of this group.'),
            source=CatalogSource(object_provides=IPerson.__identifier__)
        )
    )
    cochairs = RelationList(
        title=_(u'Co-Chair(s)'),
        description=_(u'Co-chairs of this group.'),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u'Co-Chair'),
            description=_(u'A single co-chair of this group.'),
            source=CatalogSource(object_provides=IPerson.__identifier__)
        )
    )
    additionalText = RichText(title=u"Additional Text", 
        description=_(u'Any additional rich text information you want to add to this working group.'),
        required=False)

class IParticipatingSite(IKnowledgeObject):
    u'''An participatingsite participating with the MCL consortium.'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Name of this participating site.'),
        required=True
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this participating site.'),
        required=False,
    )
    aims = RichText(
        title=_(u'Aims'),
        description=_(u'The aims of this participating site.'),
        required=False,
    )
    abstract = RichText(
        title=_(u'Abstract'),
        description=_(u'A abstract of this participating site.'),
        required=False,
    )
    abbreviation = schema.TextLine(
        title=_(u'Abbreviation'),
        description=_(u'A abbreviated name of this participating site.'),
        required=False,
    )
    organ = RelationList(
        title=_(u'Organs'),
        description=_(u'Organs associated with this Participating Site.'),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u'Organ'),
            description=_(u'A single organ studied in this Participating Site.'),
            source=CatalogSource(object_provides=IOrgan.__identifier__)
        )
    )
    staff = RelationList(
        title=_(u'Staff'),
        description=_(u'Staff associated with this Participating Site.'),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u'Staff Member'),
            description=_(u'A individual staff member in this Participating Site.'),
            source=CatalogSource(object_provides=IPerson.__identifier__)
        )
    )
    pi = RelationList(
        title=_(u'PIs'),
        description=_(u'PIs associated with this Participating Site.'),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u'PI'),
            description=_(u'An individual PI in this Participating Site.'),
            source=CatalogSource(object_provides=IPerson.__identifier__)
        )
    )
    contact = RelationList(
        title=_(u'Contacts'),
        description=_(u'Contacts in this Participating Site.'),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u'Contact'),
            description=_(u'An individual contact in this Participating Site.'),
            source=CatalogSource(object_provides=IPerson.__identifier__)
        )
    )
    institution = RelationList(
        title=_(u'Institutions'),
        description=_(u'Institutions associated with this Participating Site.'),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u'Institution'),
            description=_(u'A single institution studied in this Participating Site.'),
            source=CatalogSource(object_provides=IInstitution.__identifier__)
        )
    )
    fundingStartDate = schema.Datetime(
        title=_(u'Funding Start Date'),
        description=_(u'Funding start date for this participating site.'),
        required=False,
    )
    fundingFinishDate = schema.Datetime(
        title=_(u'Funding Finish Date'),
        description=_(u'Funding finish date for this participating site.'),
        required=False,
    )
    additionalText = RichText(
        title=u"Additional Text", 
        description=_(u'Any additional rich text information you want to add to this participating site.'),
        required=False)

class IPublication(IKnowledgeObject):
    u'''An publication participating with the MCL consortium.'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Name of this publication.'),
        required=True
    )
    year = schema.Int(
        title=_(u'Year'),
        description=_(u'The year this publication was published.'),
        required=False,
    )
    author = schema.List(
        title=_(u'Authors'),
        description=_(u'Authors who wrote this publication.'),
        required=False,
        value_type=schema.TextLine(
            title=_(u'Author'),
            description=_(u'Individual author associated with this publication.')
        )
    )
    pmid = schema.TextLine(
        title=_(u'Pubmed ID'),
        description=_(u'This publications pubmed ID.'),
        required=False,
    )
    journal = schema.TextLine(
        title=_(u'Journal'),
        description=_(u'The publications was published in this journal.'),
        required=False,
    )
    pi = RelationList(
        title=_(u'PIs'),
        description=_(u'The principle investigator assigned to this publication.'),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u'PI'),
            description=_(u'A single PI assigned to this publication.'),
            source=CatalogSource(object_provides=IPerson.__identifier__)
        )
    )


class IProtocol(IKnowledgeObject):
    u'''An protocol participating with the MCL consortium.'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Name of this protocol.'),
        required=True
    )
    description = schema.Text(
        title=_(u'Abstract'),
        description=_(u'A brief summary of this protocol.'),
        required=False,
    )
    humanSubjectTraining = schema.Text(
        title=_(u'Human Subject Training'),
        description=_(u'Human subject training flag for this protocol.'),
        required=False,
    )
    sitecontact = schema.TextLine(
        title=_(u'Site Contact'),
        description=_(u'The site contact for this protocol.'),
        required=False,
    )
    irbcontact = schema.TextLine(
        title=_(u'IRB Contact'),
        description=_(u'IRB Contact email for this protocol.'),
        required=False,
    )
    pi = RelationList(
        title=_(u'PIs'),
        description=_(u'The principle investigator assigned to this protocol.'),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u'PI'),
            description=_(u'A single PI assigned to this protocol.'),
            source=CatalogSource(object_provides=IPerson.__identifier__)
        )
    )
    custodian = RelationList(
        title=_(u'Custodians'),
        description=_(u'The custodian who provided to this protocol.'),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u'Custodian'),
            description=_(u'One of the custodians who provided this protocol.'),
            source=CatalogSource(object_provides=IPerson.__identifier__)
        )
    )
    organ = RelationList(
        title=_(u'Organs'),
        description=_(u'Organs associated with this protocol.'),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u'Organ'),
            description=_(u'A single organ studied in this protocol.'),
            source=CatalogSource(object_provides=IOrgan.__identifier__)
        )
    )
    publication = RelationList(
        title=_(u'Publications'),
        description=_(u'Publications associated with this Protocol.'),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u'Publication'),
            description=_(u'A single publication studied in this Protocol.'),
            source=CatalogSource(object_provides=IPublication.__identifier__)
        )
    )
    site = RelationList(
        title=_(u'Participating Sites'),
        description=_(u'Participating sites associated with this Protocol.'),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u'Participating Site'),
            description=_(u'A single participating site studied in this Protocol.'),
            source=CatalogSource(object_provides=IParticipatingSite.__identifier__)
        )
    )
    startDate = schema.Datetime(
        title=_(u'Start Date'),
        description=_(u'IRB Contact email for this protocol.'),
        required=False,
    )
    irbapprovalnum = schema.TextLine(
        title=_(u'IRB Approval Number'),
        description=_(u'IRB approval number used to approve this protocol.'),
        required=False,
    )
    irbapproval = schema.TextLine(
        title=_(u'IRB Approval'),
        description=_(u'Whether IRB Approved this protocol or not.'),
        required=False,
    )



    
