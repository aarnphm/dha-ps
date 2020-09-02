ingress
-------

|Go Report Card| |PkgGoDev|

network-related controller for database comms. Built with `gorilla/mux`_ and `jmoiron/sqlx`_

package-structure
~~~~~~~~~~~~~~~~~

::
 
    .
    ├── api             
    │   ├── handlers            # specific routes for each handler
    │   ├── httputil            # general http error
    │   └── middleware          # contains rate-limiter and authentication middleware (todo)
    ├── docs                     
    │   ├── rest                # contains swagger handler
    │   └── ui                  # go binary of ui
    ├── bin                     # contains binary file
    ├── configs                 # trade secrets lies here
    └── internal
        ├── models              # database models
        │   └── mocks
        ├── repository          # CRUD (Postgres)
        └── services            # handling connection between repository and api/handlers

description
~~~~~~~~~~~

- The package implements `Uncle Bob's Clean Architecture`_. This is probably the first time I forced myself to follow the `twelve-factor app`_ methodology and came accross Uncle Bob's.
- refers to the `main README.rst`_ for docker and k8s instruction

local instruction
~~~~~~~~~~~~~~~~~
- ``go run server.go``, and you should see at ``localhost:8080`` as below

.. code-block:: json

    "ProxyAlive":true,
    "StreamAlive":true


todo
~~~~

-  ☐ added authentication
-  ☐ fixed rate-limiter
-  ☐ **finish test code**
-  ☒ improved Swagger docs with more detailed response model

.. _main README.rst: https://github.com/aarnphm/dha-ps/blob/master/README.rst

.. _twelve-factor app: https://12factor.net/

.. _Uncle Bob's Clean Architecture: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html

.. _gorilla/mux: https://github.com/gorilla/mux

.. _jmoiron/sqlx: https://github.com/jmoiron/sqlx

.. |PkgGoDev| image:: https://pkg.go.dev/badge/mod/github.com/aarnphm/dha-ps/ingress
   :target: https://pkg.go.dev/mod/github.com/aarnphm/dha-ps/ingress
   
.. |Go Report Card| image:: https://goreportcard.com/badge/github.com/aarnphm/dha-ps
   :target: https://goreportcard.com/report/github.com/aarnphm/dha-ps
