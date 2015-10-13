import urllib
from random import shuffle

from DateTime import DateTime
from zope.schema.fieldproperty import FieldProperty
from z3c.form import field
from zope import schema
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.directives import form
from plone.app.portlets.portlets import base

from plone.namedfile.field import NamedImage
from plone.namedfile.interfaces import IImageScaleTraversable

import z3cformhelper  # XXX: Import from plone.app.portlets since Plone 4.3


def _(x):
    """ Spoof gettext for now """
    return x


class IImagePortlet(form.Schema):
    """
    Define image portlet fields.
    """

    image = NamedImage(
            title=_(u"Image"),
            description=_(u"Please upload an image"),
            required=False,
        )

    link = schema.TextLine(title=_(u"Link"),
                           description=_(u"Absolute or site root relative link target"),
                           required=False,
                           default=None)

    image2 = NamedImage(
            title=_(u"Image #2"),
            description=_(u"Several images will be shown as a carousel"),
            required=False,
            default=None)

    link2 = schema.TextLine(title=_(u"Link #2"),
                           description=_(u"Absolute or site root relative link target for image #2"),
                           required=False,
                            default=None)

    image3 = NamedImage(
            title=_(u"Image #3"),
            description=_(u"Several images will be shown as a carousel"),
            required=False,
            default=None)

    link3 = schema.TextLine(title=_(u"Link #3"),
                           description=_(u"Absolute or site root relative link target for image #3"),
                           required=False,
                           default=None)

    image4 = NamedImage(
            title=_(u"Image #4"),
            description=_(u"Several images will be shown as a carousel"),
            required=False,
            default=None)

    link4 = schema.TextLine(title=_(u"Link #4"),
                           description=_(u"Absolute or site root relative link target for image #4"),
                           required=False,
                           default=None)

    image5 = NamedImage(
            title=_(u"Image #5"),
            description=_(u"Several images will be shown as a carousel"),
            required=False,
            default=None)

    link5 = schema.TextLine(title=_(u"Link #5"),
                           description=_(u"Absolute or site root relative link target for image #5"),
                           required=False,
                           default=None)

    image6 = NamedImage(
            title=_(u"Image #6"),
            description=_(u"Several images will be shown as a carousel"),
            required=False,
            default=None)

    link6 = schema.TextLine(title=_(u"Link #6"),
                           description=_(u"Absolute or site root relative link target for image #6"),
                           required=False,
                           default=None)

    image7 = NamedImage(
            title=_(u"Image #7"),
            description=_(u"Several images will be shown as a carousel"),
            required=False,
            default=None)

    link7 = schema.TextLine(title=_(u"Link #7"),
                           description=_(u"Absolute or site root relative link target for image #7"),
                           required=False,
                           default=None)

    image8 = NamedImage(
            title=_(u"Image #8"),
            description=_(u"Several images will be shown as a carousel"),
            required=False,
            default=None)

    link8 = schema.TextLine(title=_(u"Link #8"),
                           description=_(u"Absolute or site root relative link target for image #8"),
                           required=False,
                           default=None)

    image9 = NamedImage(
            title=_(u"Image #9"),
            description=_(u"Several images will be shown as a carousel"),
            required=False,
            default=None)

    link9 = schema.TextLine(title=_(u"Link #9"),
                           description=_(u"Absolute or site root relative link target for image #9"),
                           required=False,
                           default=None)

    image10 = NamedImage(
            title=_(u"Image #10"),
            description=_(u"Several images will be shown as a carousel"),
            required=False,
            default=None)

    link10 = schema.TextLine(title=_(u"Link #10"),
                           description=_(u"Absolute or site root relative link target for image #10"),
                           required=False,
                           default=None)


    headingText = schema.TextLine(title=_(u"Heading"),
                           description=_(u"Text above the portlet"),
                           required=False,
                           default=u"")

    text = schema.TextLine(title=_(u"On image text"),
                                description=_(u"Text over the image for buttonish images"),
                                required=False,
                                default=u"")

    #drawText = schema.Bool(title=_(u"Is the text visible on the image"), default=True)

    footerText = schema.TextLine(title=_(u"Footer"),
                           description=_(u"Text below the portlet"),
                           required=False,
                           default=u"")

    altText = schema.TextLine(title=_(u"ALT text"),
                           description=_(u"A placeholder text for web browsers which cannot display images. This text is only needed if the portlet has only the image and no other texts."),
                           required=False,
                           default=u"")

    css = schema.TextLine(title=_(u"HTML styling"),
                          description=_(u"Extra CSS classes"),
                          required=False)


class Assignment(base.Assignment):

    # We need to explicitly mark our persistant data for @@images view look-up
    implements(IImagePortlet, IImageScaleTraversable)

    # Make sure default values work correctly migration proof manner
    text = FieldProperty(IImagePortlet["text"])
    headingText = FieldProperty(IImagePortlet["headingText"])
    footerText = FieldProperty(IImagePortlet["footerText"])
    altText = FieldProperty(IImagePortlet["altText"])

    image = FieldProperty(IImagePortlet["image"])
    link = FieldProperty(IImagePortlet["link"])

    image2 = FieldProperty(IImagePortlet["image2"])
    link2 = FieldProperty(IImagePortlet["link2"])

    image3 = FieldProperty(IImagePortlet["image3"])
    link3 = FieldProperty(IImagePortlet["link3"])

    image4 = FieldProperty(IImagePortlet["image4"])
    link4 = FieldProperty(IImagePortlet["link4"])

    image5 = FieldProperty(IImagePortlet["image5"])
    link5 = FieldProperty(IImagePortlet["link5"])

    image6 = FieldProperty(IImagePortlet["image6"])
    link6 = FieldProperty(IImagePortlet["link6"])

    image7 = FieldProperty(IImagePortlet["image7"])
    link7 = FieldProperty(IImagePortlet["link7"])

    image8 = FieldProperty(IImagePortlet["image8"])
    link8 = FieldProperty(IImagePortlet["link8"])

    image9 = FieldProperty(IImagePortlet["image9"])
    link9 = FieldProperty(IImagePortlet["link9"])

    image10 = FieldProperty(IImagePortlet["image10"])
    link10 = FieldProperty(IImagePortlet["link10"])

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def modified(self):
        """
        plone.namedfield uses this information to refresh image URLs when the content changes

        (cache busting)
        """
        return DateTime(self._p_mtime)

    @property
    def title(self):
        """
        Be smart as what show as the management interface title.
        """
        entries = [self.text, self.altText, self.headingText, self.footerText, u"Image portlet"]
        for e in entries:
            if e:
                return e


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('templates/imageportlet.pt')

    def update(self):
        """
        """
        self.imageData = self.compileImageData()

    def compileImageData(self):
        """
        Compile a list of images
        """

        data = []

        if self.data.image:
            data.append(dict(image=self.data.image, link=self.data.link, id="image"))

        # getattr -> migration safe
        for i in range(2, 10):
            image_id = "image%d" % i
            link_id = "link%d" % i
            if getattr(self.data, image_id, None):
                image = getattr(self.data, image_id)
                link = getattr(self.data, link_id)
                data.append(dict(image=image, link=link, id=image_id))

        # if getattr(self.data, "image3", None):
        #    data.append(dict(image=self.data.image3, link=self.data.link3, id="image3"))

        # if getattr(self.data, "image4", None):
        #    data.append(dict(image=self.data.image4, link=self.data.link4, id="image4"))

        # Randomize the display order
        shuffle(data)

        return data

    def getDefaultImage(self):
        """
        Return the first available image or None
        """
        if len(self.imageData) > 0:
            return self.imageData[0]["image"]
        return None

    def getDefaultLink(self):
        """
        Return the only link for the portlet which can be used with the header/footer text.

        If we have several images we cannot rotate these links.
        """

        if len(self.imageData) == 1:
            return self.imageData[0]["link"]

        return None

    def getAcquisitionChainedAssigment(self):
        """
        FFFFUUUUUUU Plone.
        """

        # XXX: Persistently set by now by add form
        column = getattr(self.data, "column", None)
        if column:
            # column is PortletAssignmentMapping https://github.com/plone/plone.app.portlets/blob/master/plone/app/portlets/storage.py
            # which is http://svn.zope.org/zope.container/trunk/src/zope/container/ordered.py?rev=120790&view=auto
            for key, value in column.items():
                if value == self.data:
                    return column, key, column[key]

        return None

    def getOnImageText(self):
        """
        """
        return self.data.text

    def getStyle(self, imageDesc):
        """
        Get explicity style for the image-wrapper CSS class.

        Use image width and height
        """

        image = imageDesc["image"]

        width, height = image.getImageSize()

        return "background: url(%s) no-repeat top left; width: %dpx; height: %dpx" % (self.getImageURL(imageDesc), width, height)

    def getLink(self, imageDesc):
        """
        :return: absolute transformed link or None if link not present
        """

        link = imageDesc["link"]

        if not link:
            return None

        if "//" in link:
            return link

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')

        if link.startswith("/"):
            link = link[1:]

        return "%s/%s" % (portal_state.portal_url(), link)

    def getImageURL(self, imageDesc):
        """
        :return: The URL where the image can be downloaded from.

        """
        context = self.context.aq_inner

        # [{'category': 'context', 'assignment': <imageportlet.portlets.Assignment object at 0x1138bb140>, 'name': u'bound-method-assignment-title-of-assignment-at-1', 'key': '/Plone/fi'},
        params = dict(
            portletName=self.__portlet_metadata__["name"],
            portletManager=self.__portlet_metadata__["manager"],
            image=imageDesc["id"],
            modified=self.data._p_mtime,
            portletKey=self.__portlet_metadata__["key"],
        )

        imageURL = "%s/@@image-portlet-downloader?%s" % (context.absolute_url(), urllib.urlencode(params))

        return imageURL

    def getCarouselCSSClass(self):
        """
        """

        if len(self.imageData) > 1:
            # Referred in JS
            cls = "image-portlet-carousel"
        else:
            cls = "image-portlet-no-carousel"
        return cls

    def getPortletCSSClass(self):
        """
        """
        cls = ""

        if self.getOnImageText():
            cls += " image-portlet-text"
        else:
            cls += " image-portlet-no-text"

        if self.data.css:
            cls += self.data.css

        return cls

    def getWrapperStyle(self):
        """
        Allocate pixel spaces to show all carousel images, so no jumpy pages
        """
        max_width = 0
        max_height = 0

        for imageDesc in self.data.imageData:
            size = imageDesc["image"].getImageSize()
            max_width = max(size[0], max_width)
            max_height = max(size[1], max_height)

        return "width: %dpx; height: %dpx" % (max_width, max_height)


class AddForm(z3cformhelper.AddForm):

    fields = field.Fields(IImagePortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(z3cformhelper.EditForm):

    fields = field.Fields(IImagePortlet)
