Requires: MySQLClient
=====================

Example Usage
-------------

This is what a charm using this relation would look like:

.. code-block:: python

    from charmhelpers.core import hookenv
    from charmhelpers.core.reactive import hook
    from charmhelpers.core.reactive import when
    from charmhelpers.core.reactive import when_file_changed
    from charmhelpers.core.reactive import set_state
    from charmhelpers.core.reactive import remove_state

    @hook('db-relation-joined')
    def request_db(mysql):
        mysql.change_database_name('mydb')
        mysql.request_roles('myrole', 'otherrole')

    @hook('config-changed')
    def check_admin_pass():
        admin_pass = hookenv.config('admin-pass')
        if admin_pass:
            set_state('admin-pass')
        else:
            remove_state('admin-pass')

    @when('db.database.available', 'admin-pass')
    def render_config(mysql):
        render_template('app-config.j2', '/etc/app.conf', {
            'db_conn': mysql.connection_string(),
            'admin_pass': hookenv.config('admin-pass'),
        })

    @when_file_changed('/etc/app.conf')
    def restart_service():
        hookenv.service_restart('myapp')


Reference
---------

.. autoclass::
    requires.MySQLClient
    :members:
