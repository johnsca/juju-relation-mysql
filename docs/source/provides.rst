Provides: MySQL
===============

Example Usage
-------------

This is what a charm using this relation would look like:

.. code-block:: python

    # in the postgres charm:
    from charmhelpers.core import hookenv  # noqa
    from charmhelpers.core import unitdata
    from charmhelpers.core.reactive import when
    from common import (
        user_name,
        create_user,
        ensure_database,
        get_service_port,
    )


    @when('db.database.requested')
    def provide_database(mysql):
        for service in mysql.requested_databases():
            database = service

            user = user_name(mysql.relation_name(), service)  # generate username
            password = create_user(user)  # get-or-create user

            ensure_database(user, schema_user, database)

            mysql.provide_database(
                service=service,
                host=hookenv.unit_private_ip(),
                port=get_service_port(),
                database=database,
                user=user,
                password=password,
            )


Reference
---------

.. autoclass::
    provides.MySQL
    :members:
