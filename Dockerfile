# MCL Site - Image Building
# =========================
#
# Used by "docker image build"
#
# The Twit-lock security scanner absolutely hates Debian Linux, so we can't
# base ourselves off the python:2.7 image either, which uses Debian. Further
# tests show that Ubuntu is out too (of course); the only acceptable Linuxes
# are centos:8 and alpine:3. So we either have to install Python, Plone, and
# all our dependencies on centos:8 or use the python:2.7.17-alpine3.11 as a
# base.
#
# FURTHER HEADACHE: we can't run as 26013 at JPL or any place else in the
# world because our data volume runs as 500, so let's throw Docker best
# practices out and make two images:
#
# ``Dockerfile`` (this file)
#     Makes an image the old fashioned way (user ID 500)
# ``Dockerfile-nci``
#     Makes an image with the user ID 26013 requirement

# Basis
# -----
#
# We'd normally just ue plone:5.2.1 but see the commentary above.

FROM python:2.7.17-alpine3.11


# Versions and digests
# --------------------
#

ENV \
    SETUPTOOLS=39.1.0 \
    PLONE_MAJOR=5.0 \
    PLONE_VERSION=5.0.8 \
    PLONE_VERSION_RELEASE=Plone-5.0.8-UnifiedInstaller-r2 \
    PLONE_MD5=246788240851f48bc2f84289a3dc6480


# Plone and MCL Setup
# -------------------
#
# OK, now that we have a working Python, let's change it up.
#
#
# Users and Directories
# ~~~~~~~~~~~~~~~~~~~~~
#
# See note above; for NCI we change to 26013 instead of 500

RUN : &&\
    addgroup -S -g 500 mcl &&\
    adduser -S -D -h /plone -G mcl -u 500 -g 'Plone for MCL User' mcl &&\
    mkdir -p /data/filestorage /data/blobstorage &&\
    chown -R mcl:mcl /data &&\
    :



# Milieu Setup
# ~~~~~~~~~~~~
#
# Note that there are lots of extra layer creation below. I don't care. We
# will address this when we upgrade to Plone 5.2+ and Python3.

RUN : &&\
    echo '@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing' >> /etc/apk/repositories &&\
    echo '@edge http://dl-cdn.alpinelinux.org/alpine/edge/main' >> /etc/apk/repositories &&\
    apk update --quiet &&\
    : More Twit-lock &&\
    apk del --quiet tiff &&\
    : We will uninstall these later &&\
    buildDeps="gcc bzip2-dev musl-dev libjpeg-turbo-dev openjpeg-dev pcre-dev openssl-dev tiff-dev libxml2-dev libxslt-dev zlib-dev openldap-dev cyrus-sasl-dev libffi-dev sudo make" &&\
    apk add --quiet --virtual plone-build $buildDeps &&\
    : These stay &&\
    runDeps="openjpeg@edge libldap libsasl libjpeg-turbo tiff libxml2 libxslt lynx netcat-openbsd libstdc++@edge libgcc@edge sqlite-libs@edge poppler-utils@edge rsync wv su-exec bash" &&\
    apk add --quiet $runDeps &&\
    : Get, check, and extract Plone &&\
    wget -q -O Plone.tgz https://launchpad.net/plone/$PLONE_MAJOR/$PLONE_VERSION/+download/Plone-$PLONE_VERSION-UnifiedInstaller.tgz &&\
    echo "$PLONE_MD5  Plone.tgz" | md5sum -c - &&\
    tar -xzf Plone.tgz &&\
    :

RUN : &&\
    /Plone-$PLONE_VERSION-UnifiedInstaller/install.sh --password=admin --daemon-user=mcl --owner=mcl --group=mcl --target=/plone --instance=instance --var=/data none &&\
    :


# Our Code
# ~~~~~~~~
#
# The ``etc`` and ``src`` directories are our own, as is the ``docker.cfg``;
# the ``buildout.cfg`` is duplicated (and modified) from plone/plone.docker,
# as is the ``docker-initialize.py`` and the (modified)
# ``docker-entrypoint.sh``.

COPY --chown=mcl:mcl buildout.cfg docker.cfg /plone/instance/
COPY --chown=mcl:mcl etc /plone/instance/etc
COPY --chown=mcl:mcl src /plone/instance/src
COPY docker-initialize.py docker-entrypoint.sh /


# Buildout
# ~~~~~~~~

RUN : &&\
    : Clean up anything copied from our src dirs &&\
    find /plone/instance/src -name '*.py[co]' -exec rm -f '{}' + &&\
    rm -rf /plone/instance/src/*/{var,bin,develop-eggs,parts} &&\
    :

RUN : &&\
    cd /plone/instance &&\
    sudo -u mcl LIBRARY_PATH=/lib:/usr/lib ./bin/buildout -c docker.cfg &&\
    ln -s /data/filestorage/ /plone/instance/var/filestorage &&\
    ln -s /data/blobstorage /plone/instance/var/blobstorage &&\
    chown -R mcl:mcl /plone /data &&\
    rm -rf /Plone* &&\
    apk del --quiet plone-build &&\
    rm -rf /plone/buildout-cache/downloads/* /var/cache/apk/* &&\
    :


# Context
# -------
#
# Finally, we set up the runtime context: volume, cwd, etc.

VOLUME      /data
EXPOSE      8080
USER        mcl:mcl
WORKDIR     /plone/instance
HEALTHCHECK --interval=1m --timeout=5s --start-period=1m CMD nc -z -w5 127.0.0.1 8080 || exit 1
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD        ["start"]


# Metadata
# --------
#
# Note that ``org.label-schema`` is deprecated, but it's a heck of a lot
# easier to understand.  Still, I have to wonder why they didn't just use
# Dublin Core.

LABEL "org.label-schema.docker.cmd"="docker container run --detach --publish 2345:8080 --volume \${MCL_DATA_DIR}/filestorage:/data/filestorage --volume \${MCL_DATA_DIR}/blobstorage:/data/blobstorage --volume \${MCL_DATA_DIR}/log:/data/log mcl-site"
LABEL "org.label-schema.name"="MCL Website/Portal"
LABEL "org.label-schema.description"="Plone 5-based portal for the Consortium for Molecular and Cellular Characterization of Screen-Detected Lesions"
LABEL "org.label-schema.version"="1.1.0"
LABEL "org.label-schema.schema-version"="1.0"
