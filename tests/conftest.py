import pytest
from kluster.deployed import DeployedKluster, deployed
from typing import Iterator


@pytest.fixture(scope="session")
def deployed_app() -> Iterator[DeployedKluster]:
    """A deployed kluster"""
    app = deployed()
    app.deployment.project.overwrite = True
    app.deployment.health_on_enter = True
    app.deployment.down_on_exit = True
    with app:
        yield app
