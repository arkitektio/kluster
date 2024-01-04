import pytest
from kluster.api.schema import create_dask_cluster



@pytest.mark.integration
def test_create_cluster(deployed_app):
    x =  create_dask_cluster(name="mikro")
    assert x.id, "Was not able to create a cluster"

