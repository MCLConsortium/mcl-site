#!/bin/sh
#
# Sync NCI Operations
# ===================
#
# This syncs the MCL database from NCI operations to the local ``var/ops``
# directory.
#
# Expects the NIH_PASSWORD environment variable set to the password allowed
# access to the NCI operations database over HTTP.
#
# Set Up
# ------
#
# Get our environment and check things before we go.

# Known good path
PATH=/usr/local/bin:/usr/bin:/bin
export PATH

# Inherit settings from environment
NIH_USERNAME=${NIH_USERNAME:-kellysc}
NIH_PASSWORD=${NIH_PASSWORD:-}
WORKSPACE=${WORKSPACE:-${PWD:-`pwd`}}

# Check the password
if [ \! -n "$NIH_PASSWORD" ]; then
    echo "❌ The NIH_PASSWORD environment must be set" 1>&2
    exit 1
fi

# Here We Go
# ----------

echo "ℹ️ Syncing with username «${NIH_USERNAME}» to «${WORKSPACE}» in var/ops" 1>&2

filestorage=${WORKSPACE}/var/ops/filestorage
blobstorage=${WORKSPACE}/var/ops/blobstorage
source=https://mcl.nci.nih.gov/


# Zope Filestorage
# ----------------
#
# We always assume this thing is changing and frequently, so we delete our
# local copy and get a fresh one every time.

echo "📈 Retrieving Zope database" 1>&2
[ -d "$filestorage" ] || mkdir -p "$filestorage"
cd "$filestorage"
rm -f "Data.fs"
wget \
    --quiet \
    --execute robots=off \
    --timestamping \
    --no-check-certificate \
    --user="$NIH_USERNAME" \
    --password="$NIH_PASSWORD" \
    "$source/filestorage/Data.fs"


# Zope Blobs
# ----------
#
# There is a gigabyte worth of blobs and they hardly change, so we
# definitely take advantage of the timestamping and mirroring features of
# ``wget`` in order to speed things up on subsequent runs.

echo "📀 Retrieving blobs" 1>&2
[ -d "$blobstorage" ] || mkdir -p "$blobstorage"
cd "$blobstorage"
wget \
    --quiet \
    --execute robots=off \
    --cut-dirs=2 \
    --reject='index.html*' \
    --no-host-directories \
    --mirror \
    --no-parent \
    --relative \
    --timestamping \
    --no-check-certificate \
    --recursive \
    --user="$NIH_USERNAME" \
    --password="$NIH_PASSWORD" \
    "$source/blobstorage/"


echo "😌 All done" 1>&2
exit 0
