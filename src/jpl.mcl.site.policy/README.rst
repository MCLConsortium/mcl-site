This package provides the *policy* for MCL, the Molecular and Cellular
Characterization of Screen-Detected Lesions.  As such, it orchestrates
dependiencies, codifies characteristics, and systematizes settings to
make the Zope_ application server and the Plone_ content management
system into the MCL website.


LDAP Authentication
===================

Note that to use LDAP accounts painlessly with this package you'll want to
install memcached_. Most Linux systems will want to use system installers.


Mac Installation of memcached
-----------------------------

By far the easiest way to install memcached on a Mac is to use Homebrew_.
Just type::

    brew install memcached

You should see something like::

    To have launchd start memcached now and restart at login:
      brew services start memcached
    Or, if you don't want/need a background service you can just run:
      /usr/local/opt/memcached/bin/memcached
    ==> Summary
    🍺  /usr/local/Cellar/memcached/1.5.12: 11 files, 198.9KB
    ==> Caveats
    ==> openssl
    A CA file has been bootstrapped using certificates from the SystemRoots
    keychain. To add additional certificates (e.g. the certificates added in
    the System keychain), place .pem files in
      /usr/local/etc/openssl/certs

    and run
      /usr/local/opt/openssl/bin/c_rehash

    openssl is keg-only, which means it was not symlinked into /usr/local,
    because Apple has deprecated use of OpenSSL in favor of its own TLS and crypto libraries.

    If you need to have openssl first in your PATH run:
      echo 'setenv PATH /usr/local/opt/openssl/bin:$PATH' >> ~/.tcshrc

    For compilers to find openssl you may need to set:
      setenv LDFLAGS -L/usr/local/opt/openssl/lib;
      setenv CPPFLAGS -I/usr/local/opt/openssl/include;

    For pkg-config to find openssl you may need to set:
      setenv PKG_CONFIG_PATH /usr/local/opt/openssl/lib/pkgconfig;

    ==> memcached
    To have launchd start memcached now and restart at login:
      brew services start memcached
    Or, if you don't want/need a background service you can just run:
      /usr/local/opt/memcached/bin/memcached

You'll likely want this started at login so you can work on MCL, so like the
message above says::

    brew services start memcached



.. _Zope: http://zope.org/
.. _Plone: https://plone.org/
.. _memcached: https://memcached.org/
.. _brew: https://brew.sh