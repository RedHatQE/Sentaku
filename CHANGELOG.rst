0.6.1
======

* fix the typo i introduced while overconfidently commiting the bits for v0.6

0.6
===

* fix latent bug in legacy external implementation registration
  by taking away multi value registration,
  use multiple registration directives instead
* bring back a version of register_external_implementations_in
  in order to keep legacy code working
* add a feature to allow non-strict method calls that allow nesting
* split Element behaviour into ElementMixing to allow reuse with different inheritance trees


0.5
===

* switch registration to dectate
* require custom context classes for registration of implementations and overriding

0.4
===

* add ImplementationContext.from_instances
* add contextual properties



0.2
====

* added implementationcontext.from_instances
