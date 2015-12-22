Quilt
=====

Quilt for docker is a fast autobuild service for `Dockerfile` projects that uses image layer caching.

Why?
----

Have you ever tried using Dockerhub's autobuild service? It sucks.

  * No image caching (means super slow if you have compilation steps in your Dockerfile, like we do)
  * Non-predictable builds (not sure when it will begin)

Screenshots
-----------

![Login](http://i.imgur.com/IQY4vs5.png)

![Manage builds](http://i.imgur.com/nmbbdPt.png)

Features
--------

  * Supports private bitbucket repositories
  * Optional `no-caching` building

To install
----------

Run the docker instance in your server

    $ sudo docker run -v /var/run/docker.sock:/run/docker.sock -v $(which docker):/bin/docker -v /usr/lib/x86_64-linux-gnu/libapparmor.so.1.1.0:/lib/x86_64-linux-gnu/libapparmor.so.1 -p 80:80 -it nubelacorp/docker-quilt
    
Configure it for the first time by visiting

     http://<host>/
     
To use
------

* Just add webhook (specified in the build card) to your Git repository push events
* To build without caching, simply include `<no-caching>` in your commit message.

How does it work?
-----------------

1. When you push changes to your `Dockerfile` project, **Quilt** will receive an inbound webhook, which notifies it to pull from the reposistory, and build it.

2. Once it is done, it will push the image to the Docker Hub registry, with the following tags
     * [original branch name]
     * latest (if branch name == 'master')
     * staging (if branch name == 'develop')