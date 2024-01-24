# Kluster

[![codecov](https://codecov.io/gh/jhnnsrs/kluster/branch/main/graph/badge.svg?token=UGXEA2THBV)](https://codecov.io/gh/jhnnsrs/kluster)
[![PyPI version](https://badge.fury.io/py/kluster.svg)](https://pypi.org/project/kluster/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://pypi.org/project/kluster/)
![Maintainer](https://img.shields.io/badge/maintainer-jhnnsrs-blue)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/kluster.svg)](https://pypi.python.org/pypi/kluster/)
[![PyPI status](https://img.shields.io/pypi/status/kluster.svg)](https://pypi.python.org/pypi/kluster/)
[![PyPI download month](https://img.shields.io/pypi/dm/kluster.svg)](https://pypi.python.org/pypi/kluster/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/jhnnsrs/kluster)


## Description

Kluster is a simple, lightweight, and easy to use dask-cluster management tool. It combines the efforts of
[dask-gateway](https://gateway.dask.org/) with the ease of use of the Arkitekt stack.

## Features

- Easy to use Cluster management on a per User basis
    - Create clusters
    - Scale clusters
    - Delete clusters
- Integrates tightly with Arkitekt
    - Use Lok to manage users, and permissions
    - Integrate easily into your existing Arkitekt stack and applicaions
- Easy transition from local testing development to production
    - Use the same code to managed clusters locally and in production
    - Just swap out the deployment backend, and you are good to go


## Standalone Installation

Even though Kluster is designed to be used with Arkitekt, it can be used as a standalone tool. In this
configuration, Kluster will use docker to spin up a dask-gateway container on your local machine, and then use that
gateway to spin up dask-clusters on your local machine.

Currently, Kluster only support single machine clusters, but (of course) support for multi-machine clusters is planned,
and will be added soon.

### Requirements

Kluster requires that you have docker installed on your machine. If you do not have docker installed, you can find
instructions for installing it [here](https://docs.docker.com/get-docker/). 
Also we require you to have at least Python3.9.

```bash
pip install kluster
```

### Usage

While you can use docker to spin up the gateway container yourself, it is easier to use the integrated python api.
    
```python
from kluster import deployed 
from kluster.api.schema import create_dask_cluster

with deployed():

    cluster = create_dask_cluster(name="test")

    # Do stuff with your cluster
    gateway = cluster.get_gateway()

    # Scale up your cluster
    gateway.adapt(minimum=1, maximum=10)

    # Do stuff with your gateway
    client = gateway.get_client()

    #// Do stuff with your client

```

In the above example, we use the `deployed` context manager to spin up a dask-gateway container on your local machine.
On entering the context manager, we create a docker-compose deployment and download the necessary containers. On exit,
we stop and remove the containers, all clusters, and all gateways.

The `create_dask_cluster` function creates a dask cluster on the gateway. It returns a `DaskCluster` object, which
contains a reference to the cluster, and a reference to the gateway. The gateway can be accessed using the
`get_gateway` you can then use the gateway to get a dask client, and do stuff with it, or scale up the cluster.




