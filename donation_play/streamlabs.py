import socketio


class StreamLabs:
    """Class for working with StreamLabs.com events."""

    def __init__(self, host, token):
        """Class initialization.

        :param host: StreamLabs.com socket host.
        :param token: your token.
        """
        self.sio_client = socketio.Client()
        self.sio_client.connect("{host}?token={token}".format(host=host, token=token))

    def add_follow_callback(self, callback):
        """Add callback function to handle user's follows.
        Callback function should take 1 argument: username.

        :param callback: callback function.
        """
        def follow_handler(data):
            if data['type'] == "follow":
                username = data['message'][0]['name']
                callback(username)

        self.sio_client.on(event="event", handler=follow_handler)

    def add_donation_callback(self, callback):
        """Add callback function to handle yours donations.
        Callback function should take 3 arguments: username, message and amount.

        :param callback: callback function.
        """
        def donation_handler(data):
            if data['type'] == "donation":
                data = data['message'][0]
                username = data['name']
                amount = data['amount']
                message = data['message']
                callback(username, message, amount)

        self.sio_client.on(event="event", handler=donation_handler)

    def add_subscription_callback(self, callback):
        """Add callback function to handle user's subscriptions.
        Callback function should take 3 arguments: username, message and months.

        :param callback: callback function.
        """
        def subscription_handler(data):
            if data['type'] == "subscription":
                data = data['message'][0]
                username = data['name']
                months = data['months']
                message = data['message']
                callback(username, message, months)

        self.sio_client.on(event="event", handler=subscription_handler)

    def add_hosting_callback(self, callback):
        """Add callback function to handle host events.
        Callback function should take 2 arguments: username and viewers.

        :param callback: callback function.
        """
        def host_handler(data):
            if data['type'] == "host":
                data = data['message'][0]
                username = data['name']
                viewers = data['viewers']
                callback(username, viewers)

        self.sio_client.on(event="event", handler=host_handler)

    def add_bits_callback(self, callback):
        """Add callback function to handle bits donation.
        Callback function should take 3 arguments: username, message and amount.

        :param callback: callback function.
        """
        def bits_handler(data):
            if data['type'] == "bits":
                data = data['message'][0]
                username = data['name']
                amount = data['amount']
                message = data['message']
                callback(username, message, amount)

        self.sio_client.on(event="event", handler=bits_handler)

    def add_raid_callback(self, callback):
        """Add callback function to handle raid events.
        Callback function should take 2 arguments: username and raiders.

        :param callback: callback function.
        """
        def raid_handler(data):
            if data['type'] == "raid":
                data = data['message'][0]
                username = data['name']
                raiders = data['raiders']
                callback(username, raiders)

        self.sio_client.on(event="event", handler=raid_handler)

    def add_merch_callback(self, callback):
        """Add callback function to handle merch events.
        Callback function should take 3 arguments: username, message and product.

        :param callback: callback function.
        """
        def merch_handler(data):
            if data['type'] == "merch":
                data = data['message'][0]
                username = data['name']
                message = data['message']
                product = data['product']
                callback(username, message, product)

        self.sio_client.on(event="event", handler=merch_handler)

    def wait(self):
        """Wait for events."""
        self.sio_client.wait()
