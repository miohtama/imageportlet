"""

    Declare a Python package imageportlet

    See

    * http://wiki.python.org/moin/Distutils/Tutorial

    * http://packages.python.org/distribute/setuptools.html#developer-s-

    * http://plone.org/products/plone/roadmap/247

"""

from setuptools import setup

long_desc = open("README.rst").read() + "\n" + open("CHANGES.txt").read()

version = '1.0'

setup(name = "imageportlet",
    version = version,
    description = "imageportlet add-on provides a portlet for Plone CMS for easily add images, banners and carousels around the content on your site",
    long_description=long_desc,
    author = "Mikko Ohtamaa",
    author_email = "mikko@opensourcehacker.com",
    url = "http://opensourcehacker.com",
    install_requires = ["five.grok", "z3c.jbot", "plone.namedfile", "plone.formwidget.namedfile"],
    packages = ['imageportlet'],
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    license="GPL2",
    include_package_data = True,
    zip_safe=False,
    entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
)
