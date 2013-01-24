import time

from z3c.form import button
from z3c.form import form
from zope.component import getMultiAdapter
from zope.interface import implements

from Acquisition import aq_parent, aq_inner

try:
    from plone.app.portlets import PloneMessageFactory as _
    PLONE4 = True
except ImportError:
    # Plone 3.3 fallbacks
    def _(x, default=""):
        if default != "":
            return default
        return x
    PLONE4 = False

from plone.app.portlets.browser.interfaces import IPortletAddForm
from plone.app.portlets.browser.interfaces import IPortletEditForm
from plone.app.portlets.interfaces import IPortletPermissionChecker


def getSiteRootRelativePath(context, request):
    """ Get site root relative path to an item

    @param context: Content item which path is resolved

    @param request: HTTP request object

    @return: Path to the context object, relative to site root, prefixed with a slash.
    """

    portal_state = getMultiAdapter((context, request), name=u'plone_portal_state')
    site = portal_state.portal()

    # Both of these are tuples
    site_path = site.getPhysicalPath()
    if not hasattr(context, "getPhysicalPath"):
        # Plone 3 fix
        #  <Products.Five.metaclass.AddForm object at 0x106671290> ->
        #  /xx/fi/++contextportlets++ContentWellPortlets.AbovePortletManager1/+>
        context = context.context

    context_path = context.getPhysicalPath()

    relative_path = context_path[len(site_path):]

    return "/" + "/".join(relative_path)


class AddForm(form.AddForm):
    implements(IPortletAddForm)

    label = _(u"Configure portlet")

    def add(self, object):
        ob = self.context.add(object)
        self._finishedAdd = True
        return ob

    def __call__(self):
        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(AddForm, self).__call__()

    def nextURL(self):
        addview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(addview))
        url = str(getMultiAdapter((context, self.request),
                                  name=u"absolute_url"))
        return url + '/@@manage-portlets'

    @button.buttonAndHandler(_(u"label_save", default=u"Save"), name='add')
    def handleAdd(self, action):
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return

        obj = self.createAndAdd(data)

        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True

            column = self.context.aq_parent

            # Store site root relative path of the assigment in the assigment itself
            path = getSiteRootRelativePath(column, self.request)
            obj.contextPath = path + "/" + obj.getId()

    @button.buttonAndHandler(_(u"label_cancel", default=u"Cancel"),
                             name='cancel_add')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(nextURL)
        return ''


class EditForm(form.EditForm):
    """An edit form for portlets.
    """

    implements(IPortletEditForm)

    label = _(u"Modify portlet")

    def __call__(self):
        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(EditForm, self).__call__()

    def nextURL(self):
        editview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(editview))
        url = str(getMultiAdapter((context, self.request),
                                  name=u"absolute_url"))
        return url + '/@@manage-portlets'

    @button.buttonAndHandler(_(u"label_save", default=u"Save"), name='apply')
    def handleSave(self, action):

        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)

        if changes:
            self.status = "Changes saved"
        else:
            self.status = "No changes"

        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''

    @button.buttonAndHandler(_(u"label_cancel", default=u"Cancel"),
                             name='cancel_add')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(nextURL)
        return ''
