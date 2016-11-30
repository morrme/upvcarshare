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


Install Virtualenv
------------------

.. code-block:: console

    $ sudo pip install virtualenv virtualenvwrapper

Add the following text to ``.bashrc`` file:

.. code-block:: bash

    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/bin/virtualenvwrapper.sh

Reload ``.bashrc``:

.. code-block:: console

    $ source ~/.bashrc

Install project
---------------

.. code-block:: console

    $ mkvirtualenv --python=/usr/local/bin/python3 carshare
    (carshare) $ git clone git@git.upv.es:GIT_CARSHARE/carshare-project.git
    (carshare) $ cd carshare-project
    (carshare) $ pip install -r requirements/production.txt


uWSGI
-----

Create a ``uwsgi.ini`` file, with the following content:

.. code-block:: ini

    [uwsgi]
    chdir           = /home/carshare/carshare-project/upvcarshare
    module          = config.wsgi
    home            = /home/carshare/.virtualenvs/carshare
    env             = DJANGO_SETTINGS_MODULE=config.settings.production
    master          = true
    processes       = 5
    socket          = /home/carshare/carshare.sock
    chmod-socket    = 666
    vacuum          = true
    stats           = /home/carshare/carshare_stats.sock


Be sure that the nginx user **can access** the ``carshare.sock`` file.

Supervisor
----------

Create the following file ``/etc/supervisord.d/carshare.ini``, with the correct secret data:

.. code-block:: ini

    [program:carshare]
    user                    = carshare
    command                 = /home/carshare/.virtualenvs/carshare/bin/uwsgi --ini /home/carshare/uwsgi.ini
    environment             = PATH="/home/carshare/.virtualenvs/carshare/bin",ORACLE_SID="ZETATEST",DJANGO_SETTINGS_MODULE="config.settings.production",DJANGO_ALLOWED_HOSTS="carsdes.cc.upv.es",DJANGO_SECRET_KEY="secret",DATABASE_URL="oraclegis://username:password@server:port/name"
    topsignal               = HUP
    stderr_logfile          = /var/log/carshare/carshare.log
    stderr_logfile_maxbytes = 50MB
    stderr_logfile_backups  = 10
    loglevel                = info

To load the new configuration file, restart supervisor service:

.. code-block:: bash

    $ sudo systemctl restart supervisord

To restart the process:

.. code-block:: bash

    $ sudo supervisorctl restart carshare

Nginx
-----

Create the following file ``/etc/nginx/conf.d/carshare.conf``:

.. code-block:: nginx

    upstream carshare_app {
        server unix:///home/carshare/carshare.sock;
    }

    server {
        listen 80;
        client_max_body_size 0;
        charset utf-8;

        location /media  {
            alias /home/carshare/carshare-project/upvcarshare/media;
        }

        location /static {
            alias /home/carshare/carshare-project/upvcarshare/public;
        }

        location / {
            uwsgi_pass  carshare_app;
            uwsgi_read_timeout 600;
            uwsgi_param  QUERY_STRING       $query_string;
            uwsgi_param  REQUEST_METHOD     $request_method;
            uwsgi_param  CONTENT_TYPE       $content_type;
            uwsgi_param  CONTENT_LENGTH     $content_length;
            uwsgi_param  REQUEST_URI        $request_uri;
            uwsgi_param  PATH_INFO          $document_uri;
            uwsgi_param  DOCUMENT_ROOT      $document_root;
            uwsgi_param  SERVER_PROTOCOL    $server_protocol;
            uwsgi_param  REMOTE_ADDR        $remote_addr;
            uwsgi_param  REMOTE_PORT        $remote_port;
            uwsgi_param  SERVER_ADDR        $server_addr;
            uwsgi_param  SERVER_PORT        $server_port;
            uwsgi_param  SERVER_NAME        $server_name;
            uwsgi_param UWSGI_SCHEME        http;
        }
    }
