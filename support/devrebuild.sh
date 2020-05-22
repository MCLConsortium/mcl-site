#!/bin/sh
# encoding: utf-8
# Copyright 2016–2017 California Institute of Technology. ALL RIGHTS
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

echo 'Stopping zope-debug, if any'
bin/zope-debug stop
echo 'Updating content blobs'
rsync -crv --progress "$opsDBHost":"$opsDBPath/blobstorage" var
echo 'Updating content database'
rsync -cv --progress "$opsDBHost":"$opsDBPath/filestorage/Data.fs" var/filestorage
echo 'Adding a Manager account to zope'
bin/zope-debug run support/admin.py admin admin
echo 'Starting Zope for Plone upgrade'
bin/zope-debug start
echo 'Waiting for Zope to get ready for the first time'
sleep 30
echo 'Upgrading Plone'
curl -v 'http://localhost:6478/mcl/@@plone-upgrade' --user 'admin:admin' -H 'Content-Type: application/x-www-form-urlencoded' --data 'form.submitted%3Aboolean=True&submit=Upgrade'
echo 'Stopping Zope for the Plone upgrade'
bin/zope-debug stop
sleep 10
echo 'Upgrading MCL'
bin/zope-debug run support/upgrade.py admin admin
echo 'Starting Zope for the data ingest'
bin/zope-debug start
echo 'Waiting for Zope to get ready'
sleep 30
echo 'Ingesting'
curl 'http://localhost:6478/mcl/@@ingestKnowledge' --user 'admin:admin' >/dev/null
echo 'Stopping Zope'
bin/zope-debug stop
sleep 10
echo 'Done! You can start a debug instance with "bin/zope-debug fg"'
exit 0
