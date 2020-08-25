This package provides content types and RDF ingest for knowledge items for the
website of the Molecular and Cellular Characterization of Screen-Detected
Lesions.  It's intended for the site https://mcl.nci.nih.gov/.


Features
--------

• RDF control panel
• Degree content type
• Organ content type
• Person content type
• Project content type
• Institution content type
• Participating Site content type
• Protocol content type
• Publication content type


Documentation
-------------

See the "docs" folder in the source distribution of this package.


Translations
------------

Currently this package supports the following languages:

• English (US American)


Developers
----------

Try this to avoid annoying buildout loops::

    virtualenv pyenv
    cd pyenv
    bin/pip install setuptools==38.5.1
    cd ..
    pyenv/bin/python bootstrap.py --setuptools-version=38.5.1
    bin/buildout
    bin/test


To Contribute
-------------

• Issue tracker: https://oodt.jpl.nasa.gov/jira/projects/CA
• Source code: https://github.com/MCLConsortium/jpl.mcl.site.knowledge
• Contact us at mailto:edrn-ic@jpl.nasa.gov

Copyright © 2016–2017 California Institute of Technology. US Government
sponsorship acknowledged. This software is licensed under the Apache License
version 2.  See the docs/LICNSE.txt file for details.
