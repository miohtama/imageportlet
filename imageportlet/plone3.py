"""

    Plone 3 monkey-patches.

    We monkey-patch portlet renderer to have __portlet_metadata__ as introduced by Plone 4.
    This is needed in order to construct image download urls for portlets.


"""

import binascii
import logging

from ZODB.POSException import ConflictError

from plone.memoize.view import memoize
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletRetriever
import plone.portlets.manager

logger = logging.getLogger("imageportlet")


def hashPortletInfo(info):
    """Creates a hash from the portlet information.

    This is a bidirectional function. The hash must only contain characters
    acceptable as part of a html id.

    info is the portlet info dictionary. Hash is put into info, and
    also returned.
    """
    concat_txt = '%(manager)s\n%(category)s\n%(key)s\n%(name)s' % info
    info['hash'] = binascii.b2a_hex(concat_txt)
    return info['hash']


@memoize
def moar_metadata(self, manager):
    retriever = getMultiAdapter((self.context, manager), IPortletRetriever)
    items = []
    for p in self.filter(retriever.getPortlets()):
        renderer = self._dataToPortlet(p['assignment'].data)
        info = p.copy()
        info['manager'] = self.manager.__name__
        info['renderer'] = renderer
        hashPortletInfo(info)
        # Record metadata on the renderer
        renderer.__portlet_metadata__ = info.copy()
        del renderer.__portlet_metadata__['renderer']
        try:
            isAvailable = renderer.available
        except ConflictError:
            raise
        except Exception, e:
            isAvailable = False
            logger.exception(
                "Error while determining renderer availability of portlet "
                "(%r %r %r): %s" % (
                p['category'], p['key'], p['name'], str(e)))

        info['available'] = isAvailable
        items.append(info)

    return items

plone.portlets.manager.PortletManagerRenderer._lazyLoadPortlets = moar_metadata
