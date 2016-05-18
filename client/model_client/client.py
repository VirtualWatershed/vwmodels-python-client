import json
import urllib3

from ..swagger_client.api_client import ApiClient


class ModelApiClient(ApiClient):

    def __init__(self, api_key, auth_host, model_host, **super_kwargs):
        """
        Important super_kwarg is host
        """
        super_kwargs['host'] = model_host
        super(ModelApiClient, self).__init__(**super_kwargs)

        self.auth_host = auth_host

        self.jwt = api_key
        if api_key is not None:
            self.set_default_header('Authorization', 'JWT ' + self.jwt)

    @classmethod
    def from_username_password(cls, username, password,
                               auth_host, model_host):

        url = auth_host + '/v1/auth'
        ret = None

        try:
            http = urllib3.PoolManager()
            ret = http.request(
                "POST", url,
                headers={'Content-Type': 'application/json'},
                body=dict(username=username, password=password)
            )

            jwt = json.loads(ret.data)['access_token']

            return cls(api_key=jwt, auth_host=auth_host)
            cls.set_default_header('Authorization', 'JWT ' + self.jwt)

        except Exception as e:
            print "authentication failed!"
            print e.message

        return ret
