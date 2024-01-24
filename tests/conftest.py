import pytest
from kluster.deployed import DeployedKluster, deployed
from typing import Iterator
from koil import unkoil
import logging


@pytest.fixture(scope="session")
def deployed_app() -> Iterator[DeployedKluster]:
    """A deployed kluster"""
    app = deployed()
    app.deployment.project.overwrite = True
    app.deployment.down_on_exit = True
    with app:
        logging.warning("Deploying app")
        app.deployment.down()
        app.deployment.up()
        logging.warning("Deployed app. Waiting for healthz")
        app.deployment.wait_for_healthz()
        logging.warning("Deployment is healthy")

        yield app

        logging.warning("Tearing down Deployment")
