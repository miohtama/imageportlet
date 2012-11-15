Introduction
-------------

*imageportlet* add-on provides a new portlet type for `Plone CMS <http://plone.org>`_.

Features

* Inline image upload from a local computer directly into the portlet. No separate image bank folder management needed.

* Image can act as a link or simply serve as a decorative banner

* Plain text slots for heading, footer, over-the-image text (button) and ``<img>`` alt text

* Carousel images via `jQuery Cycle Lite <http://jquery.malsup.com/cycle/>`_

* Cache friendly: unique URLs after each edit allows the images cached forever in the front-end cache

Use cases
----------

* `Image menus and links <http://www.visitkalajoki.fi>`_

* `In-house advertisement banners <http://www.visitkalajoki.fi>`_

Benefits
----------

The benefit over static text portlet + TinyMCE uploaded images is vastly
easier user experience. You don't need to separate portlets or place to upload the image:
images are managed within the portlet.

The management is much streamlined for non-power users.

Installation
-------------

Plone 4.2 and newer: add ``imageportlet`` to eggs in buildout.cfg::

    eggs =
        ...
        imageportlet

Old releases: `With Dexterity 1.1 pindowns <http://plone.org/products/dexterity/documentation/how-to/install>`_::

    # Change the number here to change the version of Plone being used
    extends =
        http://dist.plone.org/release/3.3.5/versions.cfg
        http://good-py.appspot.com/release/dexterity/1.1?plone=3.3.5

    eggs =
        ...
        imageportlet

The add-on is compatible down to Plone 3.3.5.


Limitations
------------

IE6 might not render over-the-image text correclty, but the user interface is still functional.


Author
-------

`Mikko Ohtamaa <http://opensourcehacker.com>`_