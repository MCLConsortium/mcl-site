#!/bin/sh -e
#
# Devrebuild
# ==========
# 
# Download and build a development database massaged from NCI

PATH=/usr/local/bin:/usr/bin:/bin
export PATH
opsHost=tumor.jpl.nasa.gov
opsDir=/usr/local/edrn/mcl/portal/ops-nci/var

# Argument check

if [ $# -ne 0 ]; then
    echo "😩 This program takes no arguments; try again?" 1>&2
    exit 1
fi


# Sentinel files check

if [ \! -f "bootstrap.py" ]; then
    echo "🤔 Not finding the bootsrap.py file; are you in the right directory?" 1>&2
    exit 1
fi


# Warning

cat <<EOF
❗️ This program will wipe out your local Zope database and log files, then
copy the latest processed operations database, and then upgrade it to the
current development software you have in this working directory. If you have
any local changes to your content database or blob files you want to preserve,
abort now!

⏱ You have 5 seconds.
EOF
sleep 5
trap 'echo "😲 Interrupted" 1>&2; exit 1' SIGINT

echo "🏃‍♀️Here we go"

[ -x bin/zope-debug ] && echo "🛑 Stopping zope-debug, if any…\c" && bin/zope-debug stop >/dev/null 2>&1; echo "done"
for d in var/filestorage var/log; do
    [ -d "$d" ] && echo "🧨 Nuking files in ${d}…\c" && find "$d" -type f -delete && echo "done"
    [ \! -d "$d" ] && echo "📁 Making new empty ${d}…\c" && mkdir -p "$d" && echo "done"
done

echo "📀 Syncing content blobs"
rsync -cr --progress $opsHost:$opsDir/blobstorage var
echo "📈 Copying Zope database"
rsync -c --progress $opsHost:$opsDir/filestorage/Data.fs var/filestorage

# Stop here if you want to test by manually doing upgrades through the
# prefs_install_products_panel. Note: you'll need to manually ingest as well.
#
# You'll also have to manually add your own Zope "Manager" user.
#
# exit 0

password=`openssl rand -hex 16`
echo "👮‍♀️ Adding Manager account to Zope DB; username = «admin», password = «${password}»"
bin/zope-debug adduser admin ${password}
# echo "🆙 Upgrading Plone"
# bin/zope-debug -O mcl run $PWD/support/upgradePlone.py
# echo "🩺 Upgrading mcl"
# bin/zope-debug -O mcl run $PWD/support/upgradeMCL.py
echo "🍽 Ingesting RDF and other data"
bin/zope-debug -O mcl run $PWD/support/ingest.py
echo "🏁 Done! You can now start a debug Zope instance with «bin/zope-debug fg»."
exit 0
