# -*- coding: utf-8 -*-

import requests, json, time

class AdhocTracker(object):
    """ Get flags and upload track data.

    The methods in this class will request data through network, so they maybe
    slow and block the whole thread. Wrap them into async calls or use thread
    pooling to speed things up.

    Attributes:
        app_key (str): App key from AppAdhoc website.
        timeout (int): Timeout for requests.
        exp_url (str): URL to request flags.
        tracker_url (str): URL to upload track data.

    """

    def __init__(self, app_key, https = False, timeout = 10):
        """ Init AdhocTracker.

        Args:
            app_key (str): App key from AppAdhoc website.
            https (boolean): If True, use https. Use http otherwise.
            timeout (Optional[int]): Timeout for requests. Defaults 10 seconds.
        """
        self.app_key = app_key
        self.timeout = timeout
        proto = "https" if https else "http"
        self.exp_url = "%s://experiment.appadhoc.com/get_flags" % (proto)
        self.tracker_url = "%s://tracker.appadhoc.com/tracker" % (proto)


    def get_flags(self, client_id, custom = {}):
        """ Get flags for a client.

        Args:
            client_id (str): Unique identification for a client. Could be user
                ID or something like that.
            custom (optional[dict]): Custom tags for the client. For example,
                you may tag the client's gender like this: custom =
                {"gender":"male"}. Defaults empty dict.
        """
        payload = {
                "app_key": self.app_key,
                "client_id": client_id,
                "custom": custom,
                "summary": {},
        }
        r = requests.post(self.exp_url, json = payload, timeout = self.timeout)
        return r.json()


    def inc_stat(self, client_id, stat_key, stat_value = 1.0, custom = {},
            timestamp = int(time.time())):
        """ Increase a stat by some value.

        Args:
            client_id (str): Unique identification for a client. Could be user
                ID or something like that.
            stat_key (str): The name of stat you want to increase.
            stat_value (optional[double]): The value you want to increase.
                Defaults to 1.0.
            custom (optional[dict]): Custom tags for the client. For example,
                you may tag the client's gender like this: custom =
                {"gender":"male"}. Defaults empty dict.
            timestamp (optional[long]): When the increasment is happenning?
                Unix timestamp by senond. It cannot be some time in the future.
                Defaults the current time.
        """
        payload = {
                "app_key": self.app_key,
                "client_id": client_id,
                "summary": {},
                "custom": custom,
                "stats": [{
                    "key": stat_key,
                    "value": stat_value,
                    "timestamp": timestamp
                }]
        }
        r = requests.post(self.tracker_url, json = payload, timeout = self.timeout)
        assert(r.json().get("status") == "ok")
