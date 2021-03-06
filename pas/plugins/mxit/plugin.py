import os
from hashlib import md5

from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import \
    ILoginPasswordHostExtractionPlugin

from Products.CMFCore.utils import getToolByName

import interface
import plugins


USER_ID_TOKEN = 'HTTP_X_MXIT_USERID_R'

SECRET_KEY = 'mxit_secret'

def password_hash(context, userid):
    ppt = getToolByName(context, 'portal_properties')
    secret = ppt.site_properties.getProperty(SECRET_KEY)
    hstr = userid + secret
    m = md5()
    m.update(hstr)
    return m.hexdigest()

def member_id(userid):
    if not userid:
        return None
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

        ppt = getToolByName(self, 'portal_properties')
        secret = ppt.site_properties.getProperty(SECRET_KEY)
        if not secret:
            return {}

        if request.has_key(USER_ID_TOKEN):
            userid = member_id(request.get(USER_ID_TOKEN))
            if not userid:
                return {}
            creds['login'] = userid
            creds['password'] = password_hash(self, userid)
            creds['remote_host'] = request.get('REMOTE_HOST', '')
            creds['remote_address'] = request.get('REMOTE_ADDR', '')

        return creds


classImplements(MXitHelper,
                ILoginPasswordHostExtractionPlugin,
                interface.IMXitHelper)

InitializeClass(MXitHelper)
