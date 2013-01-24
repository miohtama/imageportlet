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
from zExceptions import InternalError
from zope.interface import Interface
from zope.component import getUtility, getMultiAdapter
from five import grok

# Plone imports
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRetriever
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

    def getPortletById(self, content, portletManager, key, name):
        """
        :param content: Context item where the look-up is performed

        :param portletManager: Portlet manager name as a string

        :param key: Assignment key... context path as string for content portlets

        :param name: Portlet name as a string

        :return: Portlet assignment instance
        """

        # Make sure we got input
        assert key, "Give a proper portlet assignment key"
        assert name, "Give a proper portlet assignment name"

        # Resolve portlet and its image field
        manager = getUtility(IPortletManager, name=portletManager, context=content)

        # Mappings can be directly used only when
        # portlet is directly assignment to the content.
        # If it is assigned to the parent we would fail here.
        # mapping = getMultiAdapter((content, manager), IPortletAssignmentMapping)

        retriever = getMultiAdapter((content, manager,), IPortletRetriever)

        for assignment in retriever.getPortlets():
            if assignment["key"] == key and assignment["name"] == name:
                return assignment["assignment"]

        return None

    def render(self):
        """

        """
        content = self.context.aq_inner

        # Read portlet assignment pointers from the GET query
        name = self.request.form.get("portletName")
        manager = self.request.form.get("portletManager")
        imageId = self.request.form.get("image")
        key = self.request.form.get("portletKey", None)

        if not key:
            # This is probably a bot trying to fetch the image
            # and clearing the query string
            return "Bad query string - no image available"

        portlet = self.getPortletById(content, manager, key, name)
        if not portlet:
            raise InternalError("Portlet not found: %s %s" % (key, name))

        image = getattr(portlet, imageId, None)
        if not image:
            # Ohops?
            raise InternalError("Image was empty: %s" % imageId)

        # Set content type and length headers
        set_headers(image, self.request.response)

        # Push data to the downstream clients
        return stream_data(image)
