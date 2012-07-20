from AccessControl.Permissions import manage_users
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService import registerMultiPlugin

import plugin

manage_add_mxit_form = PageTemplateFile('browser/add_plugin',
                            globals(), __name__='manage_add_mxit_form' )


def manage_add_mxit_helper( dispatcher, id, title=None, REQUEST=None ):
    """Add an mxit Helper to the PluggableAuthentication Service."""

    sp = plugin.MXitHelper( id, title )
    dispatcher._setObject( sp.getId(), sp )

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect( '%s/manage_workspace'
                                      '?manage_tabs_message='
                                      'mxitHelper+added.'
                                      % dispatcher.absolute_url() )


def register_mxit_plugin():
    try:
        registerMultiPlugin(plugin.MXitHelper.meta_type)
    except RuntimeError:
        # make refresh users happy
        pass


def register_mxit_plugin_class(context):
    context.registerClass(plugin.MXitHelper,
                          permission = manage_users,
                          constructors = (manage_add_mxit_form,
                                          manage_add_mxit_helper),
                          visibility = None,
                          icon='browser/icon.gif'
                         )
