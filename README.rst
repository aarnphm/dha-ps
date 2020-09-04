dha-ps
======

|CircleCI| |Go Report Card| |PkgGoDev|

backend to determine product similarity

database comms / routing can be found under ``ingress``, semantic search
related tasks are under ``pr`` otherwise

Instruction for local development
---------------------------------

- Requirements:
    * Go
    * docker - docker-compose (Optional)
    * `poetry <https://python-poetry.org/docs/>`_ (Optional)
    * minikube and kubectl, then enable ``metrics-server`` with ``minikube addons add metrics-server``

-  Run ``make build`` to generate docker images, then to deploy k8s locally do ``kubectl apply -f deploy/minikube.yml``.
-  Check ``kubectl get svc`` and you will get something like shown:

.. code-block:: sh

    NAME                 TYPE           CLUSTER-IP   EXTERNAL-IP       PORT(S)           AGE
    ingress-service      LoadBalancer   10.0.0.96    <pending>         80:31939/TCP      72s
    kubernetes           ClusterIP      10.0.0.1     <none>            443/TCP           38h
    recommender-service  NodePort       10.0.3.13    <none>            30000:32610/TCP   71s

-  Note that ``EXTERNAL-IP`` will be configured depends on each cloud provider. If using minikube just run ``minikube service ingress-service`` to get the IP addr, then you should receive


.. code-block:: json

    "ProxyAlive":true,
    "StreamAlive":true

-  You can access ``/swaggerui/`` for API docs
-  Included a cuda-enabled images ``for price_recommender``.  Make sure you have nvidia-docker_ install. After do so run:

.. code-block:: sh
    
    cd price_recommender 
    docker build -t aar0npham/dha-pr:with-cuda -f build/with-cuda.dockerfile .
    docker run -it --gpus=all -p 5000:5000 aar0npham/dha-pr:with-cuda

- Below is an example with `minikube`_:

.. figure:: deploy/minikube.gif
   :alt: minikube example

Notes
-----
-  This serves as an API
-  the model is currently running on insufficient and unorganized test
   database as a mock test
-  please refers to `nlp/net.py`_ for more details on models
-  Assumed that ``product_info`` exists in database
-  A recent bug with GCP, and ``docker-compose`` relating to OpenSSL, fix here_
- ``NodePort`` when cofiguring usually get auto-assigned by the system. Assign at 32610

price_recommender
~~~~~~~~~~~~~~~~~
-  find a data model that fits with textile industry
-  what are the requirements of the garment industry?
-  what are the *domain* of garment industry?
-  targets, users, location?
-  labor cost?

Todo
----

-  ☐ running model in browser?
-  ☐ makes swagger functionable with k8s
    
.. code-block:: sh

    cd ingress && docker build -t aar0npham/dha-pr-swagger:latest -f build/swagger.dockerfile .
    docker run -p 8081:8080 -e URLS="[{url:'/swagger.yml', name: 'Ingress Server'}]" aar0npham/dha-pr-swagger:latest

-  ☒ k8s deployment
-  ☒ generate godoc
-  ☒ prepare info from db for inference
-  ☒ streamline ``product_info`` into python server
-  ☒ added rate limiter for middleware
-  ☒ Find a model that fits with the requirement
-  ☒ Train on another dataset

.. _minikube: image:: https://asciinema.org/a/8rztottpt8A58y2NtGUIhRERs.svg
   :target: https://asciinema.org/a/8rztottpt8A58y2NtGUIhRERs

.. _nvidia-docker: https://github.com/NVIDIA/nvidia-docker

.. _here: https://github.com/openssl/openssl/issues/5845#issuecomment-378601109

.. _nlp/net.py: price_recommender/nlp/net.py

.. |CircleCI| image:: https://circleci.com/gh/aarnphm/dha-ps/tree/master.svg?style=svg
   :target: https://circleci.com/gh/aarnphm/dha-ps

.. |PkgGoDev| image:: https://pkg.go.dev/badge/mod/github.com/aarnphm/dha-ps/ingress
   :target: https://pkg.go.dev/mod/github.com/aarnphm/dha-ps/ingress
   
.. |Go Report Card| image:: https://goreportcard.com/badge/github.com/aarnphm/dha-ps
   :target: https://goreportcard.com/report/github.com/aarnphm/dha-ps
