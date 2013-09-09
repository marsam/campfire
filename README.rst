Campfire
========
A simple `campfire api <https://github.com/37signals/campfire-api>`_ implementation.

Examples
--------

Mentions notifications:

.. code:: python

    import re

    # You can replace with growl.
    from gi.repository import Notify

    TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    MENTIONS = re.compile('(?:marsam|all|everybody|help)', flags=re.IGNORECASE | re.UNICODE)
    campfire = Campfire('lucuma', TOKEN)
    Notify.init('Campfire mentions')
    for msg in campfire.stream('433622'):
        msg_body = msg['body']
        if msg_body and re.match(MENTIONS, msg_body):
            Notify.Notification.new(self.name, msg_body, 'dialog-information').show()
