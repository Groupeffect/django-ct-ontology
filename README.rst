=====================
django-ct-ontology
=====================

A Django application for handling database content types with rdf ontology and more.

.. contents:: Table of Contents
   :depth: 2
   :local:


Requirements
============

- Python ≥ 3.12
- Django ≥ 6.0

Runtime dependencies (installed automatically):

- ``django-filter`` ≥ 25
- ``djangorestframework`` ≥ 3.16
- ``rdflib`` ≥ 7.6


Installation
============

Install from PyPI:

.. code-block:: bash

   pip install django-ct-ontology

Or via `uv <https://docs.astral.sh/uv/>`_:

.. code-block:: bash

   uv add django-ct-ontology


Configuration
=============

Add ``ontology`` to your ``INSTALLED_APPS`` in ``settings.py``:

.. code-block:: python

   INSTALLED_APPS = [
       ...
       'ontology',
   ]

To include the API endpoints, add the following to your project's ``urls.py``:

.. code-block:: python

   from django.urls import path, include

   urlpatterns = [
       ...
       path('api/', include('ontology.urls')),
   ]


Settings
========

The following settings can be configured in your ``settings.py``:

- ``ONTOLOGY_DISABLE_MODELS``: Set to ``True`` to disable loading the ontology database models and API routing. (Default: ``False``)
- ``ONTOLOGY_DISABLE_ADMIN``: Set to ``True`` to disable registering the models in the Django admin interface. (Default: ``False``)


API Endpoints
=============

When mounted at ``api/`` as shown above, the following endpoints are available:

- ``/api/ontology/predicate/``
- ``/api/ontology/subject/``
- ``/api/ontology/object/``
- ``/api/ontology/triple/``
- ``/api/ontology/domain/``
- ``/api/ontology/graph/``

These endpoints provide standard CRUD operations based on your authentication status.
