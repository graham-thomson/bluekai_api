from __future__ import print_function
import json
import requests
import hmac
import urllib
import hashlib
import base64


class Rule(object):

    def __init__(self, user_key, private_key):
        self.user_key = user_key
        self.private_key = private_key
        self.protocol = "https"
        self.endpoint = "services.bluekai.com/Services/WS/classificationRules"

    def create_signature(self, string):
        """
        Instance method that creates the HMAC authentication BlueKai Signature.
        :param string: HTTP_METHOD + URI_PATH + QUERY_ARG_VALUES + POST_DATA
        :return: Bluekai Signature String
        """
        return base64.b64encode(
            hmac.new(
                self.private_key,
                string,
                hashlib.sha256
            ).digest()
        )

    def list_rules(self, **kwargs):
        """
        This method returns a list of self-classificaton rules, which are used to map the self-classification
        categories in your private taxonomy with the user data extracted from your site. By default, this method will
        return all of your self-classificaton rules. Optionally, you can enter the following parameters to sort and
        filter the items returned by the GET request.
        :param kwargs:
        :return: Tuple of request HTTP status code and JSON response.
        """

        http_method = "GET"
        uri_path = "/Services/WS/classificationRules"
        query_arg_values = [str(v) for v in reversed(kwargs.values())]
        query_arg_keys = [str(v) for v in reversed(kwargs.keys())]


        bk_sig = self.create_signature(
            http_method + uri_path + "".join(query_arg_values)
        )

        payload_str = "&".join("{k}={v}".format(k=k, v=v) for k, v in zip(query_arg_keys, query_arg_values))
        payload_str += "&bkuid={user_key}".format(user_key=self.user_key)
        payload_str += "&" + urllib.urlencode({"bksig": bk_sig})

        headers = {"Accept": "application/json", "Content-type": "application/json",
                   "User_Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5"}

        request = requests.get("{p}://{e}?{q}".format(
            p=self.protocol,
            e=self.endpoint,
            q=payload_str
        ), headers=headers)

        try:
            return request.status_code, request.json()
        except ValueError:
            return request.status_code, request.content

    def read_rule(self, rule_id):
        """
        This method returns the self-classification rule specified by the rule_id.
        :param rule_id: ID of the rule.
        :return: Tuple of request HTTP status code and JSON response.
        """

        http_method = "GET"
        uri_path = "/Services/WS/classificationRules/"
        query_arg_values = str(rule_id)

        bk_sig = self.create_signature(
            http_method + uri_path + query_arg_values
        )

        request_params = {
            "bkuid": self.user_key
        }

        payload_str = "&".join("{k}={v}".format(k=k, v=v) for k, v in request_params.items())
        payload_str += "&" + urllib.urlencode({"bksig": bk_sig})

        request = requests.get("{p}://{e}/{id}?{q}".format(
            p=self.protocol,
            e=self.endpoint,
            id=rule_id,
            q=payload_str
        ))

        print(request.url)

        try:
            return request.status_code, request.json()
        except ValueError:
            return request.status_code, request.content

    def create_rule(self, body):
        """
        To add a new self-classification rule, copy the example, paste it into the body box, and then configure the parameters.

        JSON example for Phint-based self-classification rule
        {
        "name": "Phint Example",
        "type": "phint",
        "phints": [
        {
        "key": "x",
        "value": "123",
        "operator": "is"
        }
        ],
        "partner_id": 123,
        "site_ids": [1234],
        "category_ids": [12345]
        }

        JSON example for URL-based self-classiifcation rule
        {
        "name": "URL Example",
        "type": "url",
        "urls": ["http://shop.yoursite.com"],
        "referrer": false,
        "exact": false,
        "partner_id": 123,
        "site_ids": [1234],
        "category_ids": [123456]
        }
        :param body: Python dictionary or JSON string.
        :return: Tuple of request HTTP status code and JSON response.
        """

        http_method = "POST"
        uri_path = "/Services/WS/classificationRules"
        body = json.dumps(body) if isinstance(body, dict) else body
        bk_sig = self.create_signature(
            http_method + uri_path + body
        )

        request_params = {
            "bkuid": self.user_key
        }

        headers = {"Accept": "application/json", "Content-type": "application/json",
                   "User_Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5"}

        payload_str = "&".join("{k}={v}".format(k=k, v=v) for k, v in request_params.items())
        payload_str += "&" + urllib.urlencode({"bksig": bk_sig})

        request = requests.post("{p}://{e}?{q}".format(
            p=self.protocol,
            e=self.endpoint,
            q=payload_str
        ),
            headers=headers,
            data=body)

        try:
            return request.status_code, request.json()
        except ValueError:
            return request.status_code, request.content


    def update_rule(self, rule_id, body):
        """
        To update an existing self-classification rule, enter the ruleID, copy the example, paste it into the body box, and then configure the parameters.

        JSON example for Phint-based self-classification rule
        {
        "name": "Phint Example",
        "type": "phint",
        "phints": [
        {
        "key": "x",
        "value": "123",
        "operator": "is"
        }
        ],
        "partner_id": 123,
        "site_ids": [1234],
        "category_ids": [12345]
        }

        JSON example for URL-based self-classiifcation rule
        {
        "name": "URL Example",
        "type": "url",
        "urls": ["http://shop.yoursite.com"],
        "referrer": false,
        "exact": false,
        "partner_id": 123,
        "site_ids": [1234],
        "category_ids": [123456]
        }

        :param rule_id:
        :param body:
        :return:
        """
        # TODO implement the rest of this method.
        pass
