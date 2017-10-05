#!/usr/bin/env python
# encoding: utf-8

_version = 'UNKNOWN'


import logging, optparse, subprocess, os.path, sys, urllib2, tarfile, tempfile, contextlib, traceback, shutil, pwd, os
import random, string, getpass


_requiredHeaders = ['openssl/ssl.h', 'jpeglib.h', 'sasl/sasl.h']
_basePort = 6710
_cms = u'https://launchpad.net/plone/5.0/5.0.8/+download/Plone-5.0.8-UnifiedInstaller.tgz'
_pip = u'https://bootstrap.pypa.io/get-pip.py'
_bufsize = 512
# Stupid CBIIT systems so freakin' old they can't give us recent LDAP/SSL
_ldapURL = 'https://pypi.python.org/packages/source/p/python-ldap/python-ldap-2.4.25.tar.gz'


class _DeploymentException(Exception):
    u'''An exceptional condition indicating that something went wrong with deployment.'''
    pass


def _exec(executable, argv, cwd):
    logging.debug(u'Executing "%s" with arguments "%r" in "%s"', executable, argv, cwd)
    proc = subprocess.Popen(argv, executable=executable, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
    stdout, stderr = proc.communicate()
    logging.debug(u'Output:')
    for i in stdout.split('\n'):
        logging.debug(i)
    if proc.returncode != 0:
        raise _DeploymentException(u'Subprocess "%s" exited with %d' % (executable, proc.returncode))


def _setUpLogging():
    u'''Log to two destinations:
    1. Any message (even down to the DEBUG level) goes to ``deploy.log``.
    2. Messages from INFO and up go to the standard error.
    '''
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)-8s %(message)s',
        filename='deploy.log',
        filemode='w'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
    logging.getLogger('').addHandler(console)
    logging.debug('Logging set up')


def _checkHeader(directories, header):
    u'''Check for the existence of ``header`` file in standard locations and
    in additional ``directories``.
    '''
    logging.info(u'Checking for header file %s', header)
    locations = [
        u'/usr/local/openssl/include',
        u'/usr/local/openldap2.4/include',
        u'/usr/local/include',
        u'/usr/include',
        u'/include'
    ]
    locations.extend(directories)
    found = False
    for location in locations:
        candidate = os.path.join(location, header)
        if os.path.isfile(candidate):
            found = True
            break
    if not found:
        raise _DeploymentException(u'Cannot find header %s in any of the directories %s' % (
            header,
            u', '.join(locations)
        ))


def _checkHeaders(directories):
    u'''Ensure the required header files are available in the standard locations as well
    as in the additional ``directories``.
    '''
    logging.info(u'Checking header files')
    for header in _requiredHeaders:
        _checkHeader(directories, header)


def _makeOptParser(context):
    certFile = os.path.join(context, 'etc', 'certs', 'server.crt')
    keyFile = os.path.join(context, 'etc', 'certs', 'server.key')
    parser = optparse.OptionParser(
        version=_version,
        description=u'''Deploys the MCL site in this directory. This will download and configure the MCL software '''
        u'''and its dependencies, build it, and create the initial site content.''',
        usage=u'Usage: %prog [options] PUBLIC-HOSTNAME'
    )
    parser.add_option(
        u'-e', u'--existing-install', metavar=u'DIR',
        help=u'Migrate the content from the previous MCL site installed in DIR'
    )
    parser.add_option(
        u'-l', u'--ldap-password',
        help=u'''Password to access the MCL LDAP server. This is required if you're using --existing-install. '''
        u'''If not given you will be prompted.'''
    )
    ssl = optparse.OptionGroup(
        parser,
        u'SSL Options',
        u'Options to indicate where SSL/TLS certificate and key files are located'
    )
    ssl.add_option(
        u'-c', u'--certificate-file', default=certFile, metavar=u'FILE',
        help=u'Path to the SSL certificate file (default "%default")'
    )
    ssl.add_option(
        u'-k', u'--key-file', default=keyFile, metavar=u'FILE',
        help=u'Path to the SSL key file (default "%default")'
    )
    parser.add_option_group(ssl)
    supervisor = optparse.OptionGroup(
        parser,
        u'Supervisor Options',
        u'Process supervisor starts & monitors the processes that runs the MCL site.'
    )
    supervisor.add_option(
        u'-s', u'--supervisor-user', default=u'supervisor',
        help=u'Username for the Supervisor (default "%default"))'
    )
    supervisor.add_option(
        u'-x', u'--supervisor-password',
        help=u'Password for Supervisor (will be generated if not given)'
    )
    parser.add_option_group(supervisor)
    zope = optparse.OptionGroup(
        parser,
        u'Zope Options',
        u'Zope application server runs Plone and hence the MCL site.'
    )
    zope.add_option(
        u'-z', u'--zope-user', default=u'zope',
        help=u'Username for the Zope app server (default "%default")'
    )
    zope.add_option(
        u'-p', u'--zope-password',
        help=u'Password for Zope (will be generated if not given)'
    )
    parser.add_option_group(zope)
    ports = optparse.OptionGroup(
        parser,
        u'Ports',
        u'''Processes listen on TCP ports bound to localhost. Use a base port (each process gets base +1, base +2, '''
        u'''etc.) or select ports individually.'''
    )
    ports.add_option(
        u'--base-port',
        type='int',
        default=_basePort,
        help=u'''Base port (processes get base+1, base+2, etc.), defaults to %default'''
    )
    ports.add_option(
        u'--supervisor-port',
        type='int',
        metavar='NUM',
        help=u'''Supervisor port (default base+1)'''
    )
    ports.add_option(
        u'--zeo-monitor-port',
        type='int',
        metavar='NUM',
        help=u'''ZEO monitor port (default base+2)'''
    )
    ports.add_option(
        u'--zeo-port',
        type='int',
        metavar='NUM',
        help=u'''ZEO database port (default base+3)'''
    )
    ports.add_option(
        u'--zope-debug-port',
        type='int',
        metavar='NUM',
        help=u'''Zope debug instance port (default base+4)'''
    )
    ports.add_option(
        u'--zope-port',
        type='int',
        metavar='NUM',
        help=u'''Zope normal instance port (default base+5)'''
    )
    parser.add_option_group(ports)
    return parser


def _installLDAP(context):
    curl = os.path.abspath(u'/usr/bin/curl')
    args = (curl, '-kLO', _ldapURL)
    _exec(curl, args, context)
    tar = os.path.abspath(u'/bin/tar')
    args = (tar, u'-xzf', u'python-ldap-2.4.25.tar.gz')
    _exec(tar, args, context)
    patchfile = os.path.abspath(os.path.join(u'patches', u'python-ldap.patch'))
    patcher = os.path.abspath(u'/usr/bin/patch')
    args = (patcher, u'-p0', u'-i', patchfile)
    _exec(patcher, args, os.path.abspath(os.path.join(context, u'python-ldap-2.4.25')))
    py = os.path.abspath(os.path.join(context, u'plone', u'Python-2.7', u'bin', u'python2.7'))
    args = (py, u'setup.py', u'install')
    _exec(py, args, os.path.abspath(os.path.join(context, u'python-ldap-2.4.25')))


def _installCMS(context):
    logging.info(u'Installing CMS')
    workspace = tempfile.mkdtemp(prefix='mcl-')
    tar = os.path.join(workspace, 'install.tar.gz')
    with open(tar, 'wb') as o:
        with contextlib.closing(urllib2.urlopen(_cms)) as i:
            while True:
                buf = i.read(_bufsize)
                if len(buf) == 0: break
                o.write(buf)
    tar = tarfile.open(tar)
    tar.extractall(workspace)
    cmsDir = os.path.join(workspace, 'Plone-5.0.8-UnifiedInstaller')
    bpPatch = os.path.join(context, 'patches', 'bp.patch')
    _exec('/usr/bin/patch', ('patch', '-p0', '-i', bpPatch), cmsDir)
    installer = os.path.join(cmsDir, 'install.sh')
    target = os.path.join(context, 'plone')
    args = (installer, '--target=%s' % target, '--build-python', '--nobuildout', '--static-lxml', 'none')
    _exec(installer, args, context)
    shutil.rmtree(workspace)
    _installLDAP(context)


def _getCMS(context):
    logging.info(u'Checking CMS')
    sentinel = os.path.join(context, 'plone', 'zinstance', 'products', 'README.txt')
    if not os.path.isfile(sentinel):  # Plone not installed
        _installCMS(context)
    else:
        logging.debug(u'Using existing CMS')


def _checkDeploymentDirectory(context):
    logging.info(u'Checking if build environment is sane')
    sentinel = os.path.join(context, 'etc', 'base.cfg')
    if not os.path.isfile(sentinel):
        raise _DeploymentException(u'Distribution file "etc/base.cfg" not found; is current directory correct?')
    logging.debug(u'CWD is %s', context)


def _computePortNumbers(parser, options):
    logging.info(u'Figuring out port numbers')
    base = options.base_port
    index = 0
    ports = {}
    for name in ('supervisor_port', 'zeo_monitor_port', 'zeo_port', 'zope_debug_port', 'zope_port'):
        portNumber = getattr(options, name)
        label = name.replace('_', '-')
        if not portNumber:
            index += 1
            portNumber = base + index
            logging.debug(u'Port for %s computed from base %d to be %d', label, base, portNumber)
        else:
            logging.debug(u'Port for %s specified to be %d', label, portNumber)
        if portNumber in ports.values():
            parser.error(u'Port %d already in use; try a different port for "%s"' % (portNumber, label))
        if portNumber < 1024:
            parser.error(u'Port %d for "%s" requires root to run; choose a port number > 1024' % (portNumber, label))
        ports[name] = portNumber
    return ports


def _writeConfig(
    context, hostname, certFile, keyFile, unixAccount, superUser, superPassword, zopeUser, zopePassword, ports
):
    logging.info(u'Writing site configuration file')
    config = os.path.join(context, 'site.cfg')
    buildoutCache = os.path.join(context, 'plone', 'buildout-cache')
    eggs, downloads = os.path.join(buildoutCache, 'eggs'), os.path.join(buildoutCache, 'downloads')
    extends = os.path.join(context, 'extends')
    with open(config, 'w') as out:
        print >>out, '[versions]'
        print >>out, 'python-ldap = 2.4.25'
        print >>out, '[ssl]'
        print >>out, 'certificate-file = %s' % certFile
        print >>out, 'key-file = %s' % keyFile
        print >>out, '[hosts]'
        print >>out, 'public-hostname = %s' % hostname
        print >>out, '[zope]'
        print >>out, 'username = %s' % zopeUser
        print >>out, 'password = %s' % zopePassword
        print >>out, '[supervisor]'
        print >>out, 'username = %s' % superUser
        print >>out, 'password = %s' % superPassword
        print >>out, '[users]'
        print >>out, 'zeo = %s' % unixAccount
        print >>out, 'zope = %s' % unixAccount
        print >>out, '[ports]'
        print >>out, 'supervisor = %d' % ports['supervisor_port']
        print >>out, 'zeo = %d' % ports['zeo_port']
        print >>out, 'zeo-monitor = %d' % ports['zeo_monitor_port']
        print >>out, 'zope = %d' % ports['zope_port']
        print >>out, 'zope-debug = %d' % ports['zope_debug_port']
        print >>out, '[buildout]'
        print >>out, 'extends = ops.cfg.in'
        print >>out, 'eggs-directory = %s' % eggs
        print >>out, 'download-cache = %s' % downloads
        print >>out, 'extends-cache = %s' % extends
        print >>out, 'parts += python-ldap'
        print >>out, '[python-ldap]'
        print >>out, 'recipe = syseggrecipe'
        print >>out, 'eggs = python-ldap'


def _getCurrentUser():
    username = pwd.getpwuid(os.getuid())[0]
    logname = os.environ['LOGNAME']
    if logname != username:
        logging.warning(
            u'LOGNAME "%s" does not match current Unix user ID\'s account name "%s"; preferring latter',
            logname, username
        )
    logging.info(u'Processes will run under Unix account "%s"', username)
    return username


def _checkPassword(parser, password):
    if password is None:
        password = u''.join([random.choice(string.letters + string.digits) for i in range(32)])
    elif u':' in password:
        parser.error(u'Passwords cannot contain the colon ":" character')
    return password


def _installPIP(context):
    logging.info(u'Installing pip, setuptools')
    sentinel = os.path.join(context, 'plone', 'Python-2.7', 'lib', 'python2.7', 'site-packages', 'six.py')
    if not os.path.isfile(sentinel):
        workspace = tempfile.mkdtemp(prefix='mcl-')
        getPIP = os.path.join(workspace, 'get-pip.py')
        with open(getPIP, 'wb') as o:
            with contextlib.closing(urllib2.urlopen(_pip)) as i:
                while True:
                    buf = i.read(_bufsize)
                    if len(buf) == 0: break
                    o.write(buf)
        py = os.path.join(context, 'plone', 'Python-2.7', 'bin', 'python')
        args = (py, getPIP)
        _exec(py, args, context)
    else:
        logging.debug(u'Already installed pip, setuptools')


def _bootstrap(context):
    logging.info(u'Bootstrapping the buildout')
    sentinel = os.path.join(context, 'bin', 'buildout')
    if not os.path.isfile(sentinel):  # Already bootstrapped?
        py = os.path.join(context, 'plone', 'Python-2.7', 'bin', 'python')
        bootstrap = os.path.join(context, 'bootstrap.py')
        config = os.path.join(context, 'site.cfg')
        args = (py, bootstrap, '--allow-site-packages', '-c', config)
        _exec(py, args, context)
    else:
        logging.debug(u'Already boostrapped.')


def _buildout(context):
    logging.info(u'Building out')
    buildout = os.path.join(context, 'bin', 'buildout')
    config = os.path.join(context, 'site.cfg')
    args = (buildout, '-c', config)
    _exec(buildout, args, context)


def _patchDists(context):
    logging.info(u'Patching dists.cfg')
    dists = os.path.join(context, 'etc', 'versions', 'dists.cfg')
    extends = os.path.join(context, 'plone', 'zinstance', 'versions.cfg')
    with open(dists, 'w') as out:
        print >>out, '[buildout]'
        print >>out, 'extends = %s' % extends


def _populate(context, data):
    logging.info(u'Populating portal content')
    dataFile = os.path.join(context, u'data', data)
    zeo, zope = os.path.join(context, u'bin', u'zeo'), os.path.join(context, u'bin', u'zope-debug')
    try:
        logging.debug(u'Stopping any existing zeo using %s', zeo)
        _exec(zeo, (zeo, 'stop'), context)
    except:
        pass
    logging.debug(u'Starting zeo using %s', zeo)
    _exec(zeo, (zeo, 'start'), context)
    s, d = os.path.join(context, u'support', u'import.py'), os.path.join(context, u'var', u'zope-debug', u'import')
    args = (zope, 'run', s, dataFile, d)
    logging.debug(u'Running zope at %s with import script %s and import directory %s', zope, s, d)
    try:
        _exec(zope, args, context)
    finally:
        logging.debug(u'Stopping zeo at %s', zeo)
        _exec(zeo, (zeo, 'stop'), context)


def _migrate(old, context, username, password):
    logging.info(u'Migrating content from %s', old)
    database = os.path.join(old, u'var', u'filestorage', u'Data.fs')
    shutil.copy(database, os.path.join(context, u'var', u'filestorage'))
    shutil.rmtree(os.path.join(context, u'var', u'blobstorage'), ignore_errors=True)
    shutil.copytree(os.path.join(old, u'var', u'blobstorage'), os.path.join(context, u'var', u'blobstorage'))
    zeo, zope = os.path.join(context, u'bin', u'zeo'), os.path.join(context, u'bin', u'zope-debug')
    try:
        logging.debug(u'Stopping any existing zeo using %s', zeo)
        _exec(zeo, (zeo, 'stop'), context)
    except:
        pass
    logging.debug(u'Starting zeo using %s', zeo)
    _exec(zeo, (zeo, 'start'), context)
    upper = os.path.join(context, u'support', u'upgrade.py')
    args = (zope, 'run', upper, username, password)
    try:
        logging.debug(u'Running zope at %s with upgrade script %s', zope, upper)
        _exec(zope, args, context)
    finally:
        logging.debug(u'Stopping zeo at %s', zeo)
        _exec(zeo, (zeo, 'stop'), context)


def main(argv):
    os.environ['PYTHONHTTPSVERIFY'] = '0'
    if argv is None:
        argv = sys.argv
    try:
        context = os.path.abspath(os.getcwd())
        _setUpLogging()
        parser = _makeOptParser(context)
        options, args = parser.parse_args(argv)
        if len(args) != 2:
            parser.error(
                u'''Specify the public hostname of the MCL site, such as "mcl.nci.nih.gov", '''
                u'''"mcl-dev.nci.nih.gov", etc.'''
            )
        if options.existing_install:
            if options.ldap_password:
                ldapPassword = options.ldap_password
            else:
                ldapPassword = getpass.getpass(u'MCL LDAP Password: ')
        _checkDeploymentDirectory(context)
        publicHostname = args[1]
        ports = _computePortNumbers(parser, options)
        unixAccount = _getCurrentUser()
        zopePassword = _checkPassword(parser, options.zope_password)
        supervisorPassword = _checkPassword(parser, options.supervisor_password)
        _checkHeaders([])
        _getCMS(context)
        _patchDists(context)
        _installPIP(context)
        _writeConfig(
            context,
            publicHostname,
            os.path.abspath(options.certificate_file),
            os.path.abspath(options.key_file),
            unixAccount,
            options.supervisor_user,
            supervisorPassword,
            options.zope_user,
            zopePassword,
            ports
        )
        _bootstrap(context)
        try:
            _buildout(context)
        except:
            # Sometimes you just need to try again
            try:
                _buildout(context)
            except:
                # And again
                _buildout(context)
        if options.existing_install:
            os.environ['LDAP_PASSWORD'] = ldapPassword
            _migrate(options.existing_install, context, options.zope_user, zopePassword)
        else:
            _populate(context, 'mcl-lite.zexp')
        logging.info(u'COMPLETE!')
    except SystemExit:
        return True
    except _DeploymentException as ex:
        logging.debug(u'Exception: %r', ex)
        logging.debug(u'\n'.join(traceback.format_tb(sys.exc_info()[2])))
        logging.critical(u'Deployment failed: %s', ex)
        logging.critical(u'Unable to continue.')
        return False
    return True


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv) else -1)

