from ..swagger_client.apis.default_api import DefaultApi


class ModelApi(DefaultApi):

    def __init__(self, cl=None):

        super(ModelApi, self).__init__(api_client=cl)
