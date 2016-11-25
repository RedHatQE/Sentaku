About Sentaku
==============

Sentaku is a library that allows objects to dynamically choose their implementation.
Sentaku is the Japanese word for choice.


Sentaku provides a easy way to describe applications and use-cases
while being able to choose implementations and fall back between them.

This helps to implement test setup/tear-down and execution.

A uniform API us used to describe the behavior,
and a the tests later can decide when to use what implementations.

A typical use case is Testing your modern html5 application.
Such an application usually consists of different layers.

1. the internal backend api
2. a rest api
3. a rich fronend

When doing test setup/teardown it is
desirable to run against the fast backend api or rest API,
while when running the actual acceptance/system tests
it is more desirable to run against the rich user interface or the rest API
