Quilt
=====

Quilt for docker is a fast autobuild service for `Dockerfile` projects that uses image layer caching.

Features
--------

  * Supports private bitbucket repositories
  * Optional `no-caching` building

To install
----------

Run the docker instance in your server

    $ sudo docker run -p 80:80 -it nubelacorp/docker-quilt
    
Configure it for the first time by visiting

     http://<host>/