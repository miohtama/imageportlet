import time
from z3c.form import field
from zope import schema
from zope.component import getUtility, getMultiAdapter, queryMultiAdapter
from zope.interface import implements
from zope.site.hooks import setHooks, setSite

from plone.directives import form

from plone.app.portlets.portlets import base
import z3cformhelper  # XXX: Import from plone.app.portlets since Plone 4.3

from plone.namedfile.field import NamedImage


# Spoof gettext
def _(x):
    return x


class IImagePortlet(form.Schema):
    """
    Define portlet fields.
    """

    image = NamedImage(
            title=_(u"Please upload an image"),
            required=False,
        )


class Assignment(base.Assignment):

    implements(IImagePortlet)

    def __init__(self):
        pass


class Renderer(base.Renderer):

    def render(self, context, request):
        pass


class AddForm(z3cformhelper.AddForm):

    fields = field.Fields(IImagePortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(z3cformhelper.EditForm):

    fields = field.Fields(IImagePortlet)
