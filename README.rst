About Sentaku
================

.. image:: https://readthedocs.org/projects/sentaku/badge/?version=latest


Sentaku provides primitives to model domain objects that are
exposed via different interfaces to facilitate the same operations.

This helps to implement test setup/teardown and execution following
a uniform api while using efficient methods in setup/teardown
and configurable user-facing methods in test bodies.


A typical use case is Testing your "typical" modern application
that has a internal backend api, a rest api and a rich frontend.
The use-cases that describe the system at interaction/acceptance test level
should work at all of those layers.

For functional tests one might want
to run tests and setup/teardown in the api layer
while for smoke tests, one might want to run them all on the frontend layer.

For complex applications there might be different User Interfaces
aimed at different interest groups (administrative vs in house vs customers).


For scope limited and restricted applications
not all layers provide all functionalities and
it might be necessary to fallback.
