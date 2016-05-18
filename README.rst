UPV Car Share Project
=====================

Made with Python 3 and Django with :heart:.

Install Spatialite
------------------

Install SpatiaLite with brew on Mac OS X::

    brew update
    brew install spatialite-tools
    brew install gdal


Static files
------------

The default folder for Django's ``STATICFILES_DIRS`` value is ``/static/dist/``, therefore all
static data have to be created by **gulp**.
