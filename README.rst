Introduction
-------------

*imageportlet* add-on provides a portlet for `Plone CMS <http://plone.org>`_
for easily add images, banners and carousels around the content on your site.

.. contents:: :local:

Features
---------

* Inline image upload from a local computer directly into the portlet. No separate image bank folder management needed.

* Image can act as a link or simply serve as a decorative banner

* Plain text slots for heading, footer, over-the-image text (button) and ``<img>`` alt text

* Carousel images via `jQuery Cycle Lite <http://jquery.malsup.com/cycle/>`_

* Cache friendly: unique URLs after each edit allows the images cached forever in the front-end cache

.. image :: https://github.com/downloads/miohtama/imageportlet/Screen%20Shot%202012-11-15%20at%204.32.42%20PM.png

Use cases
----------

* `Image menus and links <http://www.visitkalajoki.fi>`_

* `image buttons <http://www.visitkalajoki.fi/fi/teemat/pariskunnat>`_.

* `In-house advertisement banners <http://www.visitkalajoki.fi>`_

* `Mini image carousels <http://www.hotellilevitunturi.fi/fi/>`_.

Benefits
----------

The benefit over static text portlet + TinyMCE uploaded images is vastly
easier user experience. You don't need to separate portlets or place to upload the image:
images are managed within the portlet.

The management is much streamlined for non-power users.

Installation
-------------

The add-on is compatible down to Plone 3.3.5.

Update buildout.

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


Run buildout.

Install the ``imageportlet`` add-on in Site Setup.

Go to any portlet manager and choose *Add new portlert... Image Portlet*.

Limitations
------------

IE6 might not render over-the-image text correclty, but the user interface is still functional.

Troubleshooting
----------------

Traceback::

    Traceback (innermost last):
      Module ZPublisher.Publish, line 119, in publish
      Module ZPublisher.mapply, line 88, in mapply
      Module ZPublisher.Publish, line 42, in call_object
      Module imageportlet.z3cformhelper, line 66, in __call__
      Module z3c.form.form, line 215, in __call__
      Module z3c.form.form, line 208, in update
      Module plone.z3cform.patch, line 21, in BaseForm_update
      Module z3c.form.form, line 149, in update
      Module z3c.form.form, line 128, in updateWidgets
      Module zope.component._api, line 103, in getMultiAdapter
    ComponentLookupError: ((<Products.Five.metaclass.AddForm object at 0x1137edfd0>, <HTTPRequest, URL=http://localhost:9888/test/++contextportlets++plone.rightcolumn/+/imageportlet.ImagePortlet>, <+ at /test/++contextportlets++plone.rightcolumn/+>), <InterfaceClass z3c.form.interfaces.IWidgets>, u'')

Reason: Make sure *Plone z3c.form support* is installed on the site.

Author
-------

`Mikko Ohtamaa <http://opensourcehacker.com>`_