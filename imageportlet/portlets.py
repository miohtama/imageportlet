
from Acquisition import aq_parent, aq_inner
from DateTime import DateTime
from zope.schema.fieldproperty import FieldProperty
from z3c.form import field
from z3c.form.form import DisplayForm
from zope import schema
from zope.interface import implements
from zope.component import getMultiAdapter

from plone.directives import form
from five import grok

from plone.app.portlets.portlets import base
#from Products.TinyMCE.vocabularies import thumbnail_sizes_vocabulary

import z3cformhelper  # XXX: Import from plone.app.portlets since Plone 4.3

from plone.namedfile.field import NamedImage
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.namedfile.interfaces import IImageScaleTraversable


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
                           required=False)


    image2 = NamedImage(
            title=_(u"Image #2"),
            description=_(u"Several images will be shown as a carousel"),
            required=False,
        )

    link2 = schema.TextLine(title=_(u"Link #2"),
                           description=_(u"Absolute or site root relative link target for image #2"),
                           required=False)

    image3 = NamedImage(
            title=_(u"Image #3"),
            description=_(u"Several images will be shown as a carousel"),
            required=False,
        )

    link3 = schema.TextLine(title=_(u"Link #3"),
                           description=_(u"Absolute or site root relative link target for image #2"),
                           required=False)

    # XXX: Have site specific configurable vocabulary for portlets here
    #imageSize = schema.Choice(title=_(u"Image size"),
    #                         description=_(u"Leave empty to use the orignal size"),
    #                         source=thumbnail_sizes_vocabulary, required=False)

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
        if getattr(self.data, "image2", None):
            data.append(dict(image=self.data.image2, link=self.data.link2, id="image2"))

        if getattr(self.data, "image3", None):
            data.append(dict(image=self.data.image3, link=self.data.link3, id="image3"))

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
        Return the first available link or None
        """
        for desc in self.imageData:
            link = desc["link"]
            if link:
                return link
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
        :return: The tag to be used to rended <img>

        """

        # The real context, where the data is stored, here is Assignment
        # self.context points to the viewed portal item

        # http://plone.org/products/plone.app.imaging

        modified = self.data._p_mtime

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')

        imageId = imageDesc["id"]

        # Scaled version object
        # XXX: Hardcored until the mess called Plone portlet management can provide
        # this information in sane way
        imageURL = "%s%s/edit/++widget++form.widgets.%s/@@download/?buster=%s" % (portal_state.portal_url(), self.data.contextPath, imageId, modified)

        # XXX: Escape
        return imageURL

    def getCarouselCSSClass(self):
        """
        """
        if len(self.imageData) > 0:
            return "image-portlet-carousel"
        else:
            return "image-portlet-no-carousel"

class AddForm(z3cformhelper.AddForm):

    fields = field.Fields(IImagePortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(z3cformhelper.EditForm):

    fields = field.Fields(IImagePortlet)
