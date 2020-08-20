# encoding: utf-8

from setuptools import setup, find_packages
import os.path

# Package data
# ------------

_name            = 'jpl.mcl.site.policy'
_version         = '1.0.2'
_description     = "Policy package for MCL"
_url             = 'http://mcl.jpl.nasa.gov/software/' + _name
_downloadURL     = 'http://oodt.jpl.nasa.gov/dist/mcl/' + _name + '-' + _version + '.tar.gz'
_author          = 'Sean Kelly'
_authorEmail     = 'sean.kelly@jpl.nasa.gov'
_maintainer      = 'Sean Kelly'
_maintainerEmail = 'sean.kelly@jpl.nasa.gov'
_license         = 'Proprietary'
_namespaces      = ['jpl', 'jpl.mcl', 'jpl.mcl.site']
_zipSafe         = False
_keywords        = 'plone zope site mcl policy dependency'
_testSuite       = 'jpl.mcl.site.policy.tests.test_suite'
_extras = {
    'test': ['plone.app.testing'],
}
_entryPoints = {
    'z3c.autoinclude.plugin': ['target=plone'],
}
_requirements = [
    'setuptools',
    'collective.captchacontactinfo',
    'collective.recaptcha',
    'eea.faceted.vocabularies',
    'eea.facetednavigation',
    'five.formlib == 1.0.4',
    'jpl.mcl.site.knowledge',
    'jpl.mcl.site.sciencedata',
    'plone.api',
    'plone.app.collection',
    'plone.app.form',
    'plone.app.imaging',
    'plone.app.ldap',
    'plone.app.upgrade',
    'plone.formwidget.recaptcha',
    'Products.Archetypes',
    'Products.ATContentTypes',
    'Products.CMFPlacefulWorkflow',
    'Products.CMFPlone',
    'Products.PloneFormGen',
    'yafowil.plone',
    'z3c.jbot',
]
_classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Plone',
    'License :: Other/Proprietary License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

# Setup Metadata
# --------------
#
# Nothing below here should require updating.

def _read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

_header = '*' * len(_name) + '\n' + _name + '\n' + '*' * len(_name)
_longDescription = _header + '\n\n' + _read('README.rst') + '\n\n' + _read('docs', 'INSTALL.txt') + '\n\n' \
    + _read('docs', 'HISTORY.txt')
open('doc.txt', 'w').write(_longDescription)

setup(
    author=_author,
    author_email=_authorEmail,
    classifiers=_classifiers,
    description=_description,
    download_url=_downloadURL,
    entry_points=_entryPoints,
    extras_require=_extras,
    include_package_data=True,
    install_requires=_requirements,
    keywords=_keywords,
    license=_license,
    long_description=_longDescription,
    maintainer=_maintainer,
    maintainer_email=_maintainerEmail,
    name=_name,
    namespace_packages=_namespaces,
    packages=find_packages('src', exclude=['ez_setup', 'bootstrap']),
    package_dir={'': 'src'},
    test_suite=_testSuite,
    url=_url,
    version=_version,
    zip_safe=_zipSafe,
)
