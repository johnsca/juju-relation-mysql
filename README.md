# Overview

This interface layer handles the communication with MySQL via the `mysql`
interface protocol.

# Usage

## Requires

The interface layer will set the following states, as appropriate:

  * `{relation_name}.connected`  The relation is established, but MySQL has not
    provided the information to use the database
  * `{relation_name}.available`  MySQL is ready for use.  You can get the
    connection information via the following methods:

    * `host()`
    * `port()`
    * `database()` (the database name)
    * `user()`
    * `password()`

For example:

```python
@when('mysql.available')
def setup(mysql):
    render(source='my.conf',
           target='/etc/app/app.conf',
           context={
               'db_host': mysql.host(),
               'db_port': mysql.port(),
               'db_name': mysql.database(),
               'db_user': mysql.user(),
               'db_pass': mysql.password(),
            })
```
