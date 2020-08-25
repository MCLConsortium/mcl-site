*****************
 Developer Notes
*****************


Some notes.


Buildout
========

We've got to move this to Plone 5.1 so we can get Python 3 support—but not
only that, setuptools is lightyears ahead so this is the command needed to
bootstrap::

    python2.7 bootstrap.py --setuptools-version=39.1.0 -c dev.cfg



Docker
======

Docker notes here.


Environemnt
-----------

Here's the env vars (csh-style)::

    setenv MCL_PORTAL_VERSION 1.1.0
    setenv MCL_DATA_DIR ${HOME}/Downloads/docker-data/mcl
    setenv MCL_PUBLISHED_PORT 4134

Make sure to create the log dir if it doesn't already exist—or else::

    mkdir -p ${MCL_DATA_DIR}/log


Building the Image
------------------

Build::

    docker image build --tag mcl-site .

But at NCI::

    docker image build --tag mcl-site --file Dockerfile-nci .

Publish::

    docker login
    docker image tag mcl-site:latest nutjob4life/mcl-site:latest
    docker image push nutjob4life/mcl-site:latest


Managing Individual Containers
------------------------------

Do::

    docker network create --driver bridge --label 'org.label-schema.name=MCL net' mcl-network

Start the DB::

    docker container run \
        --detach \
        --name mcl-db \
        --network mcl-network \
        --volume ${MCL_DATA_DIR}/filestorage:/data/filestorage \
        --volume ${MCL_DATA_DIR}/blobstorage:/data/blobstorage \
        --volume ${MCL_DATA_DIR}/log:/data/log \
        mcl-site:latest \
        zeo

Start an instance::

    docker container run \
        --name mcl-portal \
        --network mcl-network \
        --env ZEO_ADDRESS=mcl-db:8080 \
        --env ZEO_SHARED_BLOB_DIR=on \
        --publish ${MCL_PUBLISHED_PORT}:8080 \
        --volume ${MCL_DATA_DIR}/blobstorage:/data/blobstorage \
        --volume ${MCL_DATA_DIR}/log:/data/log \
        mcl-site:latest


Composition
-----------

Do::

    docker-compose --project-name mcl up --detach

If your ``docker-compose`` doesn't recognize ``--detach``, try ``-d``.

To change the Zope password::

    docker container run \
        --rm \
        --network mcl_backplane \
        --env ZEO_ADDRESS=mcl-db:8080 \
        mcl-site:latest \
        adduser NEWUSER PASSWORD
