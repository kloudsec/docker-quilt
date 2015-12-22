Quilt
=====

Quilt for docker is a fast autobuild service for `Dockerfile` projects that uses image layer caching.

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