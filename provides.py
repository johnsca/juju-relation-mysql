#!/usr/bin/python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charms.reactive import RelationBase
from charms.reactive import scopes
from charms.reactive import hook
from charms.reactive import not_unless


class MySQL(RelationBase):
    # We expect multiple, separate services to be related, but all units of a
    # given service will share the same database name and connection info.
    # Thus, we use SERVICE scope and will have one converstaion per service.
    scope = scopes.SERVICE

    @hook('{provides:mysql}-relation-joined')
    def joined(self):
        """
        Handles the relation-joined hook.

        Depending on the state of the conversation, this can trigger the
        following state:

        * ``{relation_name}.database.requested`` This state will be activated
          if a remote service is awaiting a database.  This state should be
          resolved by calling :meth:`provide_database`.  See also
          :meth:`requested_databases`.
        """
        conversation = self.conversation()
        conversation.set_state('{relation_name}.database.requested')

    @hook('{provides:mysql}-relation-{broken,departed}')
    def departed(self):
        conversation = self.conversation()

        # if these were requested but not yet fulfilled, cancel the request
        conversation.remove_state('{relation_name}.database.requested')

    @not_unless('{provides:mysql}.database.requested')
    def provide_database(self, service, host, port, database, user, password):
        """
        Provide a database to a requesting service.

        :param str service: The service which requested the database, as
            returned by :meth:`~provides.MySQL.requested_databases`.
        :param str host: The host where the database can be reached (e.g.,
            the charm's private or public-address).
        :param int port: The port where the database can be reached.
        :param str database: The name of the database being provided.
        :param str user: The username to be used to access the database.
        :param str password: The password to be used to access the database.
        """
        conversation = self.conversation(scope=service)
        conversation.set_remote(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )
        conversation.set_local('database', database)
        conversation.remove_state('{relation_name}.database.requested')

    def requested_databases(self):
        """
        Return a list of services requesting databases.

        Example usage::

            for service in mysql.requested_databases():
                database = generate_dbname(service)
                mysql.provide_database(**create_database(database))
        """
        for conversation in self.conversations():
            service = conversation.scope
            yield service
