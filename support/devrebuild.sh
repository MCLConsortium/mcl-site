#!/bin/sh
# encoding: utf-8
# Copyright 2016 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.
#
# Rebuild your local development environment using the latest weekly snapshots
# from the operational site at mcl.nci.nih.gov.

PATH=/usr/local/bin:/usr/bin:/bin
export PATH
opsDBPath='/usr/local/edrn/mcl/portal/ops-nci/var'
opsDBHost='tumor.jpl.nasa.gov'

if [ $# -ne 0 ]; then
        echo Usage: `basename $0` 1>&2
        echo "(This program takes no arguments.)" 1>&2
        exit 1
fi

if [ ! -f bootstrap.py -o ! -d etc ]; then
        echo "Run this program from the buildout directory." 1>&2
        echo "There should be a bootstrap.py file, etc subdirectory, etc." 1>&2
        exit 1
fi

cat <<EOF 1>&2
This program will wipe out your local content database and copy the latest,
processed, operational content database from the operational MCL site at NCI.
If you have any local content changes you want to hold onto, abort this now!
You have 5 seconds.
EOF

sleep 5

echo 'Updating content blobs'
rsync -crv --progress "$opsDBHost":"$opsDBPath/blobstorage" var
echo 'Updating content database'
rsync -cv --progress "$opsDBHost":"$opsDBPath/filestorage/Data.fs" var/filestorage
echo 'Adding an admin user (with password "admin")'
bin/zope-debug adduser admin admin
if [ $? -ne 0 ]; then
    cat <<EOF 1>&2
Failed to add an new admin user. Try running

    bin/zope-debug adduser admin admin

yourself and figure out what went wrong.
EOF
    exit 1
fi

echo "At this point we'd run the upgrade step, but don't have it yet!"
exit 0
