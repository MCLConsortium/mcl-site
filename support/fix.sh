#!/bin/sh

PATH=/usr/bin:/bin
export PATH

find /local/content/web/mcl/mcl.nci.nih.gov/var -type d -print0 | xargs -0 chmod 755
find /local/content/web/mcl/mcl.nci.nih.gov/var -type f -print0 | xargs -0 chmod 644
