#!/usr/bin/env python
# encoding: utf-8
# Copyright 2016 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

import logging, argparse, sys, os.path, os, shutil, atexit, tempfile, tarfile

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')

_argParser = argparse.ArgumentParser(description=u'Builds a release with installer for the MCL site')
_argParser.add_argument(
    'version',
    metavar='VERSION',
    help=u'Specifies the version of the MCL site to release'
)
_argParser.add_argument(
    'full',
    metavar='FULL-ZEXPFILE',
    help=u'Location of the complete MCL ZEXP export data'
)
_argParser.add_argument(
    'minimal',
    metavar='MIN-ZEXPFILE',
    help=u'Location of the stipped-down MCL ZEXP export data suitable for appscanning'
)

_distItems = (
    'bootstrap.py',
    'deploy.py',
    'etc',
    'INSTALL.rst',
    'ops.cfg.in',
    'patches',
    'README.rst',
    'support',
    'templates'
)


def _checkCWD():
    logging.info(u"Checking if we're in the right directory")
    sentinel = os.path.abspath('ops.cfg.in')
    if not os.path.exists(sentinel):
        raise IOError(u'Distribution file "{}" not found in current directory'.format(sentinel))


def _cleanOldDist(filename):
    logging.info(u'Removing old distributions for "%s"', filename)
    files = [os.path.abspath(os.path.join('dist', filename + i)) for i in ('', '.tar.bz2')]
    for f in files:
        if os.path.exists(f):
            logging.debug(u'Deleting "%s"', f)
            if os.path.isfile(f):
                os.remove(f)
            else:
                shutil.rmtree(f)


def _mkDist(full, minimal):
    logging.info(u'Creating new distribution layout')
    tmpdir = tempfile.mkdtemp()
    atexit.register(shutil.rmtree, tmpdir, True)
    for item in _distItems:
        logging.info(u'Copying "%s"', item)
        itemSrc = os.path.abspath(item)
        if os.path.isfile(itemSrc):
            shutil.copy(itemSrc, tmpdir)
        else:
            shutil.copytree(itemSrc, os.path.join(tmpdir, item), symlinks=True,
                ignore=shutil.ignore_patterns('[0-9A-Fa-f]*.0', 'mkdist.py', '.git', 'deploy.py'))
    dataDir = os.path.join(tmpdir, u'data')
    os.makedirs(dataDir)
    logging.info(u'Copying full zexp "%s"', full)
    shutil.copy(full, dataDir)
    logging.info(u'Copying minimal zexp "%s"', minimal)
    shutil.copy(minimal, dataDir)
    return tmpdir


def _patchDeployer(stagingArea, version):
    logging.info(u'Copying deployer script and patching its version number')
    srcName, dstName = os.path.abspath('deploy.py'), os.path.join(stagingArea, 'deploy.py')
    with open(srcName, 'r') as src, open(dstName, 'w') as dst:
        for i in src:
            if i.startswith(u'_version ='):
                dst.write(u"_version = '{}'\n".format(version))
            else:
                dst.write(i)


def _mkArchive(stagingArea, distname):
    logging.info(u'Creating archive')
    distDir = os.path.abspath('dist')
    if not os.path.isdir(distDir): os.makedirs(distDir)
    targetName = os.path.join(distDir, distname + u'.tar.bz2')
    target = tarfile.open(targetName, 'w:bz2')
    target.add(stagingArea, distname)
    target.close()


def main():
    try:
        args = _argParser.parse_args()
        _checkCWD()
        distname = u'mcl-site-{}'.format(args.version)
        _cleanOldDist(distname)
        stagingArea = _mkDist(args.full, args.minimal)
        _patchDeployer(stagingArea, args.version)
        _mkArchive(stagingArea, distname)
    except Exception as ex:
        logging.exception(u'Creating distribution failed: %s', unicode(ex))
        return False
    return True


if __name__ == '__main__':
    sys.exit(0 if main() else -1)
