import json
import requests
import hmac
import urllib
import hashlib
import base64

class Categories(object):

    def __init__(self, user_key, private_key):
        self.user_key = user_key
        self.private_key = private_key
        self.site_id = 40138
        self.protocol = "http"
        self.endpoint = "taxonomy.bluekai.com/taxonomy/categories"

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

    def list_categories(self, partner_id, view):
        """
        Method to retrieve a filtered set of categories based on query parameters.
        :param partner_id: (Required) The unique ID of the partner. This parameter is used with the view parameter.
        :param view: (Required) Filter's the response based on the following values:
                    -BUYER: Returns all first- and second-party categories in your taxonomy
                            and all third-party categories in the Audience Data Marketplace.
                    -OWNER: Returns all first-party categories in the owner's taxonomy.
                    -PUBLIC: Returns all third-party categories in the Audience Data Marketplace.
        :return: Tuple of request HTTP status code and JSON response.
        """
        http_method = "GET"
        uri_path = "/taxonomy/categories"
        query_arg_values = partner_id + view

        bk_sig = self.create_signature(
            http_method + uri_path + query_arg_values
        )

        request_params = {
            "bkuid": self.user_key,
            "partner.id": partner_id,
            "view": view
        }

        payload_str = "&".join("{k}={v}".format(k=k, v=v) for k, v in request_params.items())
        payload_str += "&" + urllib.urlencode({"bksig": bk_sig})

        request = requests.get("{p}://{e}?{q}".format(
            p=self.protocol,
            e=self.endpoint,
            q=payload_str
        ))

        try:
            return request.status_code, request.json()
        except ValueError:
            return request.status_code, request.content


    def read_category(self, id):
        """
        Retrieve information for a specific category (for example, reach, price)
        :param id: The unique ID (integer) assigned to the category to be retrieved
        :return: Tuple of request HTTP status code and JSON response.
        """

        http_method = "GET"
        uri_path = "/taxonomy/categories/"
        query_arg_values = id

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
            id=id,
            q=payload_str
        ))

        try:
            return request.status_code, request.json()
        except ValueError:
            return request.status_code, request.content

    def create_category(self, body):
        """
        To create a category, prepare a request body based on the category you want to create and paste it into the body box.

        JSON category Example

        {
        "name": "Example Category",
        "parentCategory": {
        "id": 410579
        },
        "partner": {
        "id": 2362
        }
        }
        :param body: Python dictionary or JSON string.
        :return: Tuple of request HTTP status code and JSON response.
        """

        http_method = "POST"
        uri_path = "/taxonomy/categories"
        body = json.dumps(body) if isinstance(body, dict) else body

        bk_sig = self.create_signature(
            http_method + uri_path + body
        )

        request_params = {
            "bkuid": self.user_key
        }

        payload_str = "&".join("{k}={v}".format(k=k, v=v) for k, v in request_params.items())
        payload_str += "&" + urllib.urlencode({"bksig": bk_sig})

        request = requests.post("{p}://{e}?{q}".format(
            p=self.protocol,
            e=self.endpoint,
            q=payload_str
        ),
        # data=json.loads(body),
        json=body
        )

        # bksig=t821GTAZXyKFQVVb8V0tETHG1uP72iHGYloYJvTzqf0%3D


        print request.url

        try:
            return request.status_code, request.json()
        except ValueError:
            return request.status_code, request.content

    def update_category(self, body):
        """
        To update a category, prepare a request body including the category's id, name, parentCategory, partner, and any other properties you want to update, then paste it into the body box.

        JSON category Example

        {
        "id": "420063",
        "name": "Self-classification Example Category",
        "parentCategory": {
        "id": 410579
        },
        "partner": {
        "id": 2362
        }
        }

        :param body: Python dictionary or JSON string.
        :return: Tuple of request HTTP status code and JSON response.
        """

        http_method = "PUT"
        url_path = "/taxonomy/categories"
        body = json.dumps(body) if isinstance(body, dict) else body
