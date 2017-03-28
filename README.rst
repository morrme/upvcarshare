UPV Car Share Project
=====================

Made with Python 3 and Django with :heart:.

Install Spatialite (macOS)
--------------------------

Install SpatiaLite with brew on macOS::

    brew update
    brew install spatialite-tools
    brew install gdal

Install Oracle client (macOS)
-----------------------------

Download from `Oracle <http://www.oracle.com/technetwork/topics/intel-macsoft-096467.html>`_

- instantclient-basic-macos.x64-12.1.0.2.0.zip
- instantclient-sdk-macos.x64-12.1.0.2.0.zip

Create a directory ``/usr/local/lib/oracle``::

    export ORACLE_HOME=/usr/local/lib/oracle
    export VERSION=12.1.0.2.0
    export ARCH=x86_64

    mkdir -p $ORACLE_HOME

Unpack both files to that directory, and create symlinks::

    cd $ORACLE_HOME
    tar -xzf instantclient-basic-12.1.0.2.0-macosx-x64.zip
    tar -xzf instantclient-sdk-12.1.0.2.0-macosx-x64.zip
    mv instantclient_12_1/* $ORACLE_HOME
    rmdir instantclient_12_1

    cd /usr/local/lib/
    ln -s $ORACLE_HOME/libclntsh.dylib.12.1 libclntsh.dylib.12.1
    ln -s $ORACLE_HOME/libocci.dylib.12.1 libocci.dylib.12.1
    ln -s $ORACLE_HOME/libnnz12.dylib libnnz12.dylib

Install ``cx_Oracle`` from PIP::

    env ARCHFLAGS="-arch $ARCH" pip install cx_Oracle

Environment Variables
---------------------

List of environment variables that the project needs to work in production:

- ``DJANGO_ALLOWED_HOSTS="example.com"``
- ``DJANGO_SETTINGS_MODULE="config.settings.production"``
- ``DJANGO_SECRET_KEY="verylongstringwithnumbers"``
- ``DATABASE_URL="oraclegis://dbuser:dbpass@db.server.com:1521/dbname"``

Static files
------------

The default folder for Django's ``STATICFILES_DIRS`` value is ``/static/dist/``, therefore all
static data have to be created by **gulp**.

Run tests
---------

To run the tests using Docker::

    $ docker-compose -f dev.yml run app python3 manage.py test --settings=config.settings.test

