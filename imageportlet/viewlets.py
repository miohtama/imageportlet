"""

    For more information see

    * http://collective-docs.readthedocs.org/en/latest/views/viewlets.html

"""

# Zope imports
from zope.interface import Interface
from zope.component import getMultiAdapter
from five import grok

# Plone imports
from plone.app.layout.viewlets.interfaces import IPortalFooter

# Local imports
from interfaces import IAddonSpecific

grok.templatedir("templates")
grok.layer(IAddonSpecific)

# By default, set context to zope.interface.Interface
# which matches all the content items.
# You can register viewlets to be content item type specific
# by overriding grok.context() on class body level
grok.context(Interface)

