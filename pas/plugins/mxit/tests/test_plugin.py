import os
import unittest2 as unittest

from base import INTEGRATION_TESTING

from pas.plugins.mxit import plugin

os.environ['MXIT_SECRET'] = 'secret'

class TestMXitHelper(unittest.TestCase):
    """ Test xmlfile module """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.plugin = plugin.MXitHelper('mxithelper')

    def test_extractCredentials_no_creds( self ):
        self.assertEquals(self.plugin.extractCredentials(self.request), {})

        self.request.set('X-MXit-ID-R', 'testuser1')
        self.assertEquals(self.plugin.extractCredentials(self.request), {})
