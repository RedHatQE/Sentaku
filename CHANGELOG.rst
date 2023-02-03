v0.8.0
=======

* migrate to hatch

  * drop tox
  * drop setuptools

* add type annotations


v0.7.2
=======

* loosen dependency on attrs


v0.7.1
======

* bugfix typo in release pipeline 💩

v0.7.0
=======

* update to setup.cfg metadata and modernize build
* drop python <3.6 support
* update pre-commiting
* drop the long deprecated reigster_external_implementations helper
* drop unnneeded reg/importscan requirements
* upgrade attrs to 20.x


v0.6.3
======


* upgrade attrs to at least 17.0.0 and s/convert/converter/

v0.6.2
======

* contextual property strictness
* freeze ImplementationName

v0.6.1
======

* fix the typo i introduced while overconfidently commiting the bits for v0.6

v0.6
====

* fix latent bug in legacy external implementation registration
  by taking away multi value registration,
  use multiple registration directives instead
* bring back a version of register_external_implementations_in
  in order to keep legacy code working
* add a feature to allow non-strict method calls that allow nesting
* split Element behaviour into ElementMixing to allow reuse with different inheritance trees


v0.5
====

* switch registration to dectate
* require custom context classes for registration of implementations and overriding

v0.4
====

* add ImplementationContext.from_instances
* add contextual properties



v0.2
====

* added implementationcontext.from_instances
