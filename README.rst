About Sentaku
================

.. image:: https://readthedocs.org/projects/sentaku/badge/?version=latest


Sentaku provides primitives to describe the structure of your Application
and to implement different ways to perform actions with it.


This helps to implement test setup/tear-down and execution.

A uniform API us used to describe the actions,
and a python context.manager allows to configure how
the description is mapped to


A typical use case is Testing your "typical" modern application.
Such an application usually consists of different layers.

1. the internal backend api
2. a rest api
3. a rich fronend

Sentaku aims to run integration and system tests against all layers
and the ability to fall back to different layers
in case one of the layers is missing an implementation of functionality.

It also aims to support using fast layers for setup/teardown
and user-facing layers for test bodies
