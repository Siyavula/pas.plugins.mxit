import os

from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import \
    ILoginPasswordHostExtractionPlugin

import interface
import plugins

def password_hash(userid):
    secret = os.environ['MXIT_SECRET']
    hstr = userid + secret
    m = md5()
    m.update(hstr)
    return m.hexdigest()

def member_id(userid):
    return '%s@mxit.com' % userid


class MXitHelper(BasePlugin):
    """ Authenticate MXit users as members
    """

    meta_type = 'MXit Helper'
    security = ClassSecurityInfo()

    def __init__( self, id, title=None ):
        self._setId( id )
        self.title = title

    #
    #   ILoginPasswordExtractionPlugin implementation
    #
    security.declarePrivate('extractCredentials')
    def extractCredentials(self, request):
        """ Extract credentials from cookie or 'request'. """
        creds = {}

        if not os.environ.has_key('MXIT_SECRET'):
            return {}

        if request.has_key('X-MXit-USERID-R'):
            userid = member_id(request.get('X-MXit-USERID-R'))
            creds['password'] = password_hash(userid)

        return creds


classImplements(MXitHelper,
                ILoginPasswordHostExtractionPlugin,
                interface.IMXitHelper)

InitializeClass(MXitHelper)
