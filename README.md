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

    $ docker run -d -p 80:80 -p 40001:443 -i -t nubelacorp/docker-quilt
    
Configure it for the first time by visiting

     http://<host>/
     
     
To use
------

  1. Visit `http://<host>` to create a new `build flow`
  2. Add the generated webhook to your **repository push** event for your git project. It should look something like this

    http://<host>/dockerfile/webhook