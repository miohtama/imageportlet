
from Acquisition import aq_parent, aq_inner
from DateTime import DateTime

from z3c.form import field
from z3c.form.form import DisplayForm
from zope import schema
from zope.interface import implements
from zope.component import getMultiAdapter

from plone.directives import form
from five import grok

from plone.app.portlets.portlets import base
from Products.TinyMCE.vocabularies import thumbnail_sizes_vocabulary

import z3cformhelper  # XXX: Import from plone.app.portlets since Plone 4.3

from plone.namedfile.field import NamedImage
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.namedfile.interfaces import IImageScaleTraversable

# Spoof gettext for now
def _(x):
    return x


class IImagePortlet(form.Schema):
    """
    Define image portlet fields.
    """

    image = NamedImage(
            title=_(u"Please upload an image"),
            required=False,
        )

    # XXX: Have site specific configurable vocabulary for portlets here
    #imageSize = schema.Choice(title=_(u"Image size"),
    #                         description=_(u"Leave empty to use the orignal size"),
    #                         source=thumbnail_sizes_vocabulary, required=False)

    imageText = schema.TextLine(title=_(u"Image text"),
                                description=_(u"Text over the image for buttonish images"),
                                required=False)

    link = schema.TextLine(title=_(u"Link"),
                           description=_(u"Absolute or site root relative link target"),
                           required=False)

    css = schema.TextLine(title=_(u"HTML styling"),
                          description=_(u"Extra CSS classes"),
                          required=False)


class Assignment(base.Assignment):

    # We need to explicitly mark our persistant data for @@images view look-up
    implements(IImagePortlet, IImageScaleTraversable)

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def modified(self):
        """
        plone.namedfield uses this information to refresh image URLs when the content changes

        (cache busting)
        """
        return DateTime(self._p_mtime)


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('templates/imageportlet.pt')

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

    def getImageTag(self):
        """
        :return: The tag to be used to rended <img>

        """

        # The real context, where the data is stored, here is Assignment
        # self.context points to the viewed portal item

        # http://plone.org/products/plone.app.imaging

        modified = self.data._p_mtime

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')

        # Scaled version object
        # XXX: Hardcored until the mess called Plone portlet management can provide
        # this information in sane way
        imageURL = "%s%s/edit/++widget++form.widgets.image/@@download/?buster=%s" % (portal_state.portal_url(), self.data.contextPath, modified)

        return '<img src="%s" />' % imageURL


class AddForm(z3cformhelper.AddForm):

    fields = field.Fields(IImagePortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(z3cformhelper.EditForm):

    fields = field.Fields(IImagePortlet)
