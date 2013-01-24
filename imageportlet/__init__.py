"""

    Zope 2 style module init

"""

try:
    # Plone 4 and higher
    import plone.app.upgrade
    PLONE_VERSION = 4
except ImportError:
    PLONE_VERSION = 3

# W0613:  7,15:initialize: Unused argument 'context'
# pylint: disable=W0613

if PLONE_VERSION == 3:
    # do the monkey dance!
    import plone3


def initialize(context):
    """ Zope 2 init code goes here.

    Usually there is nothing to go here,
    so move foward.
    """

