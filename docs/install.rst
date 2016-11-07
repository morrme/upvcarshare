Installation on CentOS
======================

Instructions to install the project on a CentOS 7.2 server.

Install yum dependencies
------------------------

.. code-block:: console

    $ yum install libjpeg-devel zlib-devel gcc python-devel libcap-devel supervisor gdal gdal-devel yum-utils

Install Python 3
----------------
How  to install Python 3 on CentOS from source:

.. code-block:: console

    $ sudo yum-builddep python
    $ wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
    $ tar xf Python-3.5.2.tgz
    $ cd Python-3.5.2
    $ ./configure
    $ make
    $ sudo make install

