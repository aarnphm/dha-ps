dha-pr
======

|CircleCI| |Go Report Card| |PkgGoDev|

backend to determine product similarity

database comms / routing can be found under ``ingress``, semantic search
related tasks are under ``pr`` otherwise

Instruction for local development
---------------------------------

- Remember to install:
    * Go
    * docker/docker-compose
    * `poetry <https://python-poetry.org/docs/>`_ (Optional)
    * minikube and kubectl, then ``minikube addons add metrics-server``

-  Run ``make docker-build`` to generate docker images, then to deploy k8s locally do ``kubectl apply -f deploy/minikube.yml``.
-  Check ``kubectl get svc`` and you will get something like shown:

.. code-block:: sh

    NAME                 TYPE           CLUSTER-IP   EXTERNAL-IP       PORT(S)           AGE
    ingress-service      LoadBalancer   10.0.0.96    <pending>         80:31939/TCP      72s
    kubernetes           ClusterIP      10.0.0.1     <none>            443/TCP           38h
    recommender-service  NodePort       10.0.3.13    <none>            30000:32610/TCP   71s

-  One note that ``EXTERNAL-IP`` will be configured depends on each cloud provider. If using minikube just run ``minikube service ingress-service``
-  Included a cuda-enabled images ``for price_recommender``.  Make sure you have nvidia-docker_ install. After do so run:

.. code-block:: sh
    
    cd price_recommender 
    docker build -t aar0npham/dha-pr:with-cuda -f build/with-cuda.dockerfile .
    docker run -it --gpus=all -p 5000:5000 aar0npham/dha-pr:with-cuda


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

.. raw:: html

   <details><summary>when using GLoVe Embedding, check out <a href="https://github.com/aar0npham/dha-pr/blob/ad463699fc4e9b090ddbe4f8920ac6272487c002/recommender/notes.ipynb">here</a> </summary>
   <p>
      <ul>- <i>notes.ipynb</i> for demonstration, including few lines to download pretrained model</ul>
      <ul>- <i>wordsim.py</i> includes cosine similarity with Glove Embedding from standford</ul>
      
   </p></details>

-  ☐ k8s deployment
-  ☐ running model in browser?
-  ☒ generate godoc
-  ☒ prepare info from db for inference
-  ☒ streamline ``product_info`` into python server
-  ☒ added rate limiter for middleware
-  ☒ Find a model that fits with the requirement
-  ☒ Train on another dataset

.. _nvidia-docker: https://github.com/NVIDIA/nvidia-docker

.. _here: https://github.com/openssl/openssl/issues/5845#issuecomment-378601109

.. _nlp/net.py: pr/nlp/net.py

.. |CircleCI| image:: https://circleci.com/gh/aarnphm/dha-pr/tree/master.svg?style=svg
   :target: https://circleci.com/gh/aarnphm/dha-pr

.. |PkgGoDev| image:: https://pkg.go.dev/badge/mod/github.com/aarnphm/dha-pr/ingress
   :target: https://pkg.go.dev/mod/github.com/aarnphm/dha-pr/ingress
   
.. |Go Report Card| image:: https://goreportcard.com/badge/github.com/aar0npham/dha-pr
   :target: https://goreportcard.com/report/github.com/aar0npham/dha-pr
