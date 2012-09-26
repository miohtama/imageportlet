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

* Image menus and links

* In-house advertisement banners

Benefits
----------

The benefit over static text portlet + TinyMCE uploaded images is that
the image blob exist within the portlet. The management interface is simpler
and you do not separate image bank. The management is much streamlined for non-power users.

Limitations
------------

IE6 might not render over-the-image text correclty, but the user interface is still functional.

Installation
-------------

* http://plone.org/documentation/kb/installing-add-ons-quick-how-to

Author
-------

`Mikko Ohtamaa <http://opensourcehacker.com>`_