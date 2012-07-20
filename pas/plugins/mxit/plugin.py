"""Class: MXitHelper
"""
import os

from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import \
    ILoginPasswordHostExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import  \
    IAuthenticationPlugin

import interface
import plugins

class MXitHelper(BasePlugin):
    """ Authenticate MXit users as members
    """

    meta_type = 'MXit Helper'
    security = ClassSecurityInfo()

    def __init__( self, id, title=None ):
        self._setId( id )
        self.title = title

    def _password_hash(self):
        login = self.REQUEST.get('X-MXit-ID-R')
        internaluserid = self.REQUEST.get('X-MXit-USERID-R')
        secret = os.environ['MXIT_HASH']
        hstr = login + internaluserid + secret
        m = md5()
        m.update(hstr)
        return m.hexdigest()

    #
    #   ILoginPasswordExtractionPlugin implementation
    #
    security.declarePrivate('extractCredentials')
    def extractCredentials(self, request):
        """ Extract credentials from cookie or 'request'. """
        creds = {}

        if not os.environ.has_key('MXIT_HASH'):
            return {}

        if request.has_key('X-MXit-ID-R'):
            login = '_mxit_' % request.get('X-MXit-ID-R')
            creds['password'] = self._password_hash()

        if creds:
            creds['remote_host'] = request.get('REMOTE_HOST', '')

            try:
                creds['remote_address'] = request.getClientAddr()
            except AttributeError:
                creds['remote_address'] = request.get('REMOTE_ADDR', '')

        return creds

    #
    #   IAuthenticationPlugin implementation
    #
    security.declarePrivate( 'authenticateCredentials' )
    def authenticateCredentials(self, credentials):
        """ See IAuthenticationPlugin.

        o We expect the credentials to be those returned by
          ILoginPasswordExtractionPlugin.
        """
        login = credentials.get('login')
        password = credentials.get( 'password' )

        if login is None or password is None:
            return None

        if password == self._password_hash():
            return login, login


classImplements(MXitHelper,
                ILoginPasswordHostExtractionPlugin,
                IAuthenticationPlugin,
                interface.IMXitHelper)

InitializeClass(MXitHelper)
