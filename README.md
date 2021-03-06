# vwmodels-python-client

This repository contains the Python client for the vwmodels api. It started
with a Swagger auto-generated client, shown here.

# Usage

First, clone the repository and install dependencies

```
git clone http://github.com/VirtualWatershed/vwmodels-python-client.git && \
python setup.py install
```

You will also need to start the Docker container with the modelserver and
authorization API. To set this up, reference the
[vw-deploy instructions](https://github.com/mtpain/vw-deploy/tree/4b4f8aacc650b1f2f3f268dc860282e0c4713ed5/v1.0/development).
Be sure to note the IP address of the Docker machine you set up.

Now we can use the client, which is a thin wrapper that inherits the
`swagger-codegen`'d client.


```python
from urllib import urlretrieve
from client.model_client.client import ModelApiClient
from client.swagger_client.default_api import DefaultApi

# 192.168.99.101 is the IP of the Docker host
auth_host = 'http://192.168.99.101:5005/api'
model_host = 'http://192.168.99.101:5000/api'

cl = ModelApiClient(auth_host=auth_host, model_host=model_host)
cl.authenticate_jwt(username='name@host.com', password='mypasswd')

api = DefaultApi(api_client=cl)

# initialize an isnobal modelrun
create_res =\
    api.create_modelrun(modelrun=dict(title='new modelrun', model='isnobal'))

api.upload_resource_to_modelrun(
    create_res.id, 'input', 'examples/data/twoweek_inputs_with_zlib.nc'
)

api.start_modelrun(create_res.id)

# download the output once the run has finished
run_is_not_finished = True

while run_is_not_finished:
    state = api.get_modelrun_by_id(create_res.id).progress_state
    run_is_not_finished = (state != 'FINISHED' and state != 'ERROR')

## save the output ##

mr1_resources = api.get_modelrun_by_id(1).resources
# isnobal has only one output; could iterate over all outputs instead of pop
# for multiple outputs
mr1_output = filter(lambda x: x.resource_type == 'output').pop()
urlretrieve(mr1_output.resource_url,'examples/local/isno_output_twoweek.nc')
```


# Autogenerate client via swagger

We use swagger-codegen to generate the client, which can be installed on OS X
using [Homebrew](http://brew.sh)

```
brew install swagger-codegen
```

If using another OS you can [follow the swagger-codegen installation
documentation](https://github.com/swagger-api/swagger-codegen/blob/master/README.md#prerequisites)
to get the swagger-codegen tool.

To auto-generate the REST API client, run the following command:

```
swagger-codegen generate -i https://github.com/VirtualWatershed/vwadaptor/raw/swagger/swagger.yaml -l python
```

If you are using the Java `.jar` file, you would equivalently run

```
java -jar /path/to/swagger-codegen-cli.jar generate -i https://github.com/VirtualWatershed/vwadaptor/raw/swagger/swagger.yaml -l python
```

If not using the Homebrew version, it may be useful to set
`alias swagger-codegen='java -jar /path/to/swagger-codegen-cli.jar'`


Now there will be a `swagger_client` directory along with a few other files
that `swagger-codegen` creates (`README.md`, `git_push.sh`, and `setup.py`).
There is a helper script, `regen_client.sh` to leave an existing `README.md`
unchanged and to remove `git_push.sh`, which we won't use. The user will have
the opportunity to merge the new README in with their existing README by
following the instructions. `regen_client.sh` will merge changes into the
current branch, so make sure to branch off master before using this tool.


