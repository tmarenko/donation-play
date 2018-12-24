import socketio
import json


class DonationAlerts:
    """Class for working with DonationAlerts.ru events."""

    def __init__(self, host, port, token):
        """Class initialization.

        :param host: DonationAlerts.ru socket host
        :param port: DonationAlerts.ru socket port
        :param token: your token.
        """
        self.sio_client = socketio.Client()
        self.sio_client.connect("{host}:{port}".format(host=host, port=port))
        self.sio_client.emit("add-user", data={
            "token": token,
            "type": "minor"
        })

    def add_donation_callback(self, callback):
        """Add callback function to handle your donations.
        Callback function should take 5 arguments: username, message, amount, (bool) is_sib, months

        :param callback: callback function.
        """
        def donation_handler(data):
            json_data = json.loads(data)
            json_data['additional_data'] = json.loads(json_data['additional_data'])
            amount = json_data['amount']
            username = json_data['username']
            message = json_data['message']
            is_sub = 'event_data' in json_data['additional_data'] and\
                     'months' in json_data['additional_data']['event_data']
            months = json_data['additional_data']['event_data']['months'] if is_sub else None
            callback(username, message, amount, is_sub, months)

        self.sio_client.on(event="donation", handler=donation_handler)

    def wait(self):
        """Wait for events."""
        self.sio_client.wait()
