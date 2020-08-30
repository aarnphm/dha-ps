price_recommender
------------------

FastAPI_ server performing semantic search for product similarity. Built with a customized DistilBERT_ on top of `huggingface/transformers`_

package-structure
~~~~~~~~~~~~~~~~~

::
  
    .
    ├── api
    │   └── handlers          # process comms from upstream
    ├── build                 # contains docker-related
    ├── core                  # included configs and env variables
    ├── internal           
    │   ├── domain            # include model for responses from upstream
    │   └── repository        # handles mongodb documents
    └── nlp                   # semantic search

notes
~~~~~

- run ``poetry install`` then do ``uvicorn main:app --port 5000 --reload`` to access nlp server
- added ONNX for inference on browser?


.. _FastAPI: https://github.com/tiangolo/fastapi

.. _DistilBERT: https://arxiv.org/pdf/1910.01108.pdf
.. _huggingface/transformers: https://github.com/huggingface/transformers
