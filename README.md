*************
 MCL Website
*************

This is the software that runs the website for the Consortium for Molecular
and Cellular Characterization of Screen-Detected Lesions, better known as the
MCL Consortium, nominally hosted at https://mcl.nci.nih.gov/.

This software is open source and licensed under the Apache License version 2;
see the file ``LICENSE.txt``.

This software was developed by and copyrighted 2016 by the California
Institute of Technology.  ALL RIGHTS RESERVED.  U.S. Government sponsorship
acknowledged.


Installation
============

See the file ``INSTALL.rst``.


Questions, Bug Reports, and Help
================================

For feedback about this product, please visit
http://cancer.jpl.nasa.gov/contact-info.


Support
=======

Once the MCL Portal is in operations at NCI, you can get post-operational
support by emailing ``ncicb@pop.nci.nih.gov``.


Developers
==========

You'll want to do::

    virtualenv python2.7-for-mcl-site
    cd python2.7-for-mcl-site
    bin/pip install setuptools==38.5.1
    cd ..
    git clone git@github.com:MCLConsortium/mcl-site.git
    cd mcl-site
    ../python2.7-for-mcl-site/bin/python2.7 bootstrap.py --setuptools-version=38.5.1 -c dev.cfg
    bin/buildout -c dev.cfg
