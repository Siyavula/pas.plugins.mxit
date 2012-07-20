Tests for pas.plugins.mxit

test setup
----------

    >>> from Testing.ZopeTestCase import user_password
    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()

Plugin setup
------------

    >>> acl_users_url = "%s/acl_users" % self.portal.absolute_url()
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % ('portal_owner', user_password))
    >>> browser.open("%s/manage_main" % acl_users_url)
    >>> browser.url
    'http://nohost/plone/acl_users/manage_main'
    >>> form = browser.getForm(index=0)
    >>> select = form.getControl(name=':action')

pas.plugins.mxit should be in the list of installable plugins:

    >>> 'Mxit Helper' in select.displayOptions
    True

and we can select it:

    >>> select.getControl('Mxit Helper').click()
    >>> select.displayValue
    ['Mxit Helper']
    >>> select.value
    ['manage_addProduct/pas.plugins.mxit/manage_add_mxit_helper_form']

we add 'Mxit Helper' to acl_users:

    >>> from pas.plugins.mxit.plugin import MxitHelper
    >>> myhelper = MxitHelper('myplugin', 'Mxit Helper')
    >>> self.portal.acl_users['myplugin'] = myhelper

and so on. Continue your tests here

    >>> 'ALL OK'
    'ALL OK'

