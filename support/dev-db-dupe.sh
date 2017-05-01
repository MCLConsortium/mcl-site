#!/bin/sh -e
#
# Update our copy of the MCL site's database snapshots
#
# 2016-08-24 - created
#
# Copyright 2016 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.


# Please keep these secret:
username='USERNAME'
password='PASSWORD'


# Where we store stuff:
filestorage='/var/www/html/static/mcl-portal-snapshots/filestorage'
blobstorage='/var/www/html/static/mcl-portal-snapshots/blobstorage'


# First the content:
[ -d "$filestorage" ] || mkdir --parents "$filestorage"
cd "$filestorage"
/usr/bin/wget \
    --quiet \
    --execute robots=off \
    --timestamping \
    --no-check-certificate \
    --user="$username" \
    --password="$password" \
    https://mcl.nci.nih.gov/var/filestorage/Data.fs


# Now the blobs:
[ -d "$blobstorage" ] || mkdir --parents "$blobstorage"
cd "$blobstorage"
/usr/bin/wget \
    --quiet \
    --execute robots=off \
    --cut-dirs=1 \
    --reject='index.html*' \
    --no-host-directories \
    --mirror \
    --no-parent \
    --relative \
    --timestamping \
    --no-check-certificate \
    --recursive \
    --user="$username" \
    --password="$password" \
    https://mcl.nci.nih.gov/var/blobstorage/


# Yay:
exit 0
