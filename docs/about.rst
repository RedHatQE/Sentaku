About Sentaku
==============

Sentaku_ is a python library that allows objects to dynamically choose their implementation.
Sentaku_ is the Japanese word for 'choice'.

With Sentaku_ it is possible to describe the elements of the applications you interact with
and the actions/attributes they have.
Sentaku_ takes care of choosing the implementation of the actions/attributes.


Installing
----------

::

	pip install sentaku



Use cases
-----------

A common use for such a system is testing various layers of an application with the same code,
as well as using different layers of an application for setup/teardown and for concise acceptance-tests.


A typical use case is testing your modern html5 application.
Such an application usually consists of different layers.

1. The internal back-end API
2. A rich front-end
3. A REST API
4. APIs that directly interact with other services the application uses

When doing test setup/teardown it is
desirable to run against the fast back-end API or REST API,
while when running the actual acceptance/system tests
it is more desirable to run against the rich user interface or the REST API.

.. _Sentaku: http://pypi.python.org/pypi/sentaku
