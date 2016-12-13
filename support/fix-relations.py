# encoding: utf-8
#
# Run this with: bin/zope-debug fix-relations.py

app = globals().get('app', None)  # ``app`` comes from ``zope run`` magic.

import transaction
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.User import system
from Testing.makerequest import makerequest
from zope.component.hooks import setSite
from zope.globalrequest import setRequest
from zc.relation.interfaces import ICatalog
from z3c.relationfield.event import _relations
from z3c.relationfield.event import _setRelation
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from z3c.relationfield.event import updateRelations
from z3c.relationfield.interfaces import IHasRelations

app = makerequest(app)
newSecurityManager(None, system)
portal = app.mcl
setSite(portal)
portal.REQUEST['PARENTS'] = [portal]
portal.REQUEST.setVirtualRoot('/')
setRequest(portal.REQUEST)

THRESHOLD = 100

relations_catalog = getUtility(ICatalog)

paths = ['/'.join(r.from_object.getPhysicalPath())
         for r in relations_catalog.findRelations() if hasattr(r, 'from_object') and r.from_object]

relations_catalog.clear()

counter = 0
for path in paths:
    obj = app.unrestrictedTraverse(path)
    for name, relation in _relations(obj):
        _setRelation(obj, name, relation)
    counter += 1
    if counter % THRESHOLD == 0:
        transaction.savepoint()
transaction.commit()

pc = getToolByName(portal, 'portal_catalog')
brains = pc.searchResults(object_provides=IHasRelations.__identifier__)
for brain in brains:
    obj = brain.getObject()
    updateRelations(obj, None)
transaction.commit()
