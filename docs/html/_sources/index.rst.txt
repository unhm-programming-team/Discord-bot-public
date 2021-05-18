.. UNHM Programming Club Discord Bot Documentation documentation master file, created by
   sphinx-quickstart on Thu May 13 18:58:20 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

UNHM Programming Club Discord Bot Documentation
===============================================

Note, some of the autodoc isn't yet working. Decorators are confusing the docstring parsing. See the code in `faces-cog.rst` for an example of a not-solution, which does capture part of the docstring, but also includes the documentation for the command object Discord is wrapping it in.

Some workarounds might be extracted from `this github issue <https://github.com/sphinx-doc/sphinx/issues/3783>`_

Some sphinx directives can be found `here <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#table-of-contents>`_

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   cogs
   our_packages



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Dependency Documentation
========================

`autoapi <https://sphinx-autoapi.readthedocs.io/en/latest/>`_

:py:mod:`discord.ext.commands`

:py

:py

:py:data:`discord.version_info`
