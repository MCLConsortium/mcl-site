# encoding: utf-8

u'''MCL Site Knowledge — functional tests'''

from jpl.mcl.site.knowledge import PACKAGE_NAME
from jpl.mcl.site.knowledge.testing import JPL_MCL_SITE_KNOWLEDGE_FUNCTIONAL_TESTING as LAYER
from plone.testing import layered
import doctest, unittest

_optionFlags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE)


def test_suite():
    return unittest.TestSuite([
        layered(doctest.DocFileSuite('README.rst', package=PACKAGE_NAME, optionflags=_optionFlags), LAYER),
    ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
