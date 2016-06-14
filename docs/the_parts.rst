Components of Sentaku
======================

.. py:currentmodule:: sentaku


.. _implementation-context:

ImplementationContext
------------------------

.. autoclass:: ImplementationContext
  :members: impl, root

  .. automethod:: use(*implementation_types, [frozen=False])


.. _implementation-identification:

Implementation Identifications
------------------------------

Implementation Identifications are developer-choosen *Names* for Implementations.
By convention you should use :py:class:`sentaku.ImplementationName` instances.

Implementation Identifications are used to refer to implementations in the :ref:`implementation-context` abd they
are used to refer to implementations when  registring implementations of :ref:`contextual-method`


.. _application-element:

Application Elements
--------------------

Application elements are subclasses of :py:class:`sentaku.Element`.
They describe single Elements of Applications

Elements on a abstract perspective Refer to Collections, Entries and sets of actions.

Depending on implementation they can be listings,
forms, rest collections/data entries, or file contents.


.. autoclass:: Element
  :members:

  .. py::attr:: parent


.. _contextual-method:

Contextual Methods
------------------

.. autoclass:: ContextualMethod()
  :members:
