import json

from swagger_client.api_client import ApiClient


class ModelApiClient(ApiClient):

    def __init__(self, username=None, password=None, auth_host=None,
                 model_host=None, **super_kwargs):
        """
        Important super_kwarg is host
        """
        self.username = username
        self.password = password

        super_kwargs['host'] = model_host
        self.auth_host = auth_host

        self.authenticated = False

        super(ModelApiClient, self).__init__(**super_kwargs)

    def authenticate_jwt(self, username=None, password=None):

        if username is None:
            if self.username is None:
                raise RuntimeError("No username has been provided")

            else:
                username = self.username

        if password is None:
            if self.password is None:
                raise RuntimeError("No password has been provided")

            else:
                password = self.password

        url = self.auth_host + '/v1/auth'
        ret = None

        try:
            ret = self.request(
                "POST", url,
                headers={'Content-Type': 'application/json'},
                body=dict(username=username, password=password)
            )

            self.authenticated = True
            self.jwt = json.loads(ret.data)['access_token']

        except:
            print "authentication failed!"

        return ret
