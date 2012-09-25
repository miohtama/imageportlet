"""

    Plone views overrides.

    For more information see

    * http://collective-docs.readthedocs.org/en/latest/views/browserviews.html

"""

# Disable unused imports pylint warning as they are here
# here for example purposes
# W0611: 12,0: Unused import Interface

# pylint: disable=W0611

# Zope imports
from zope.interface import Interface
from zope.component import getUtility, getMultiAdapter
from five import grok

# Plone imports
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.namedfile.utils import set_headers, stream_data

# Local imports
from interfaces import IAddonSpecific

grok.templatedir("templates")
grok.layer(IAddonSpecific)


class ImagePortletHelper(grok.CodeView):
    """
    Expose stuff downloadable from the image portlet BLOBs.
    """
    grok.context(Interface)
    grok.baseclass()


class ImagePortletImageDownload(ImagePortletHelper):
    """
    Expose image fields as downloadable BLOBS from the image portlet.

    Allow set caching rules (content caching for this view)
    """
    grok.context(Interface)
    grok.name("image-portlet-downloader")

    def render(self):
        """

        """
        content = self.context

        # Read portlet assignment pointers from the GET query
        name = self.request.form.get("portletName")
        portletManager = self.request.form.get("portletManager")
        imageId = self.request.form.get("image")

        # Resolve portlet and its image field
        manager = getUtility(IPortletManager, name=portletManager, context=content)
        mapping = getMultiAdapter((content, manager), IPortletAssignmentMapping)
        portlet = mapping[name]
        image = getattr(portlet, imageId, None)
        if not image:
            # Ohops?
            return ""

        # Set content type and length headers
        set_headers(image, self.request.response)

        # Push data to the downstream clients
        return stream_data(image)
