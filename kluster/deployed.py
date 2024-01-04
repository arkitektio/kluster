from dokker import mirror,  Deployment
import os
from koil.composition import Composition
from rath.links.auth import ComposedAuthLink
from rath.links.aiohttp import AIOHttpLink
from rath.links.graphql_ws import GraphQLWSLink
from kluster.kluster import Kluster
from kluster.rath import (
    KlusterRath,
    SplitLink,
    KlusterRathLinkComposition,
)
from kluster.repository import Repository
from graphql import OperationType

test_path = os.path.join(os.path.dirname(__file__), "deployments", "test")


def build_deployment() -> Deployment:
    setup = mirror(test_path)
    setup.add_health_check(
        url="http://localhost:7766/graphql", service="kluster", timeout=5, max_retries=10
    )
    return setup


async def token_loader():
    """ Returns a token as defined in the static_token setting for omero_ark"""
    return "demo"


def build_deployed_kluster() -> Kluster:

    repo = Repository(
        endpoint="http://localhost:7744",
        token_loader=token_loader,
        token_refresher=token_loader,
    )

    y = KlusterRath(
        link=KlusterRathLinkComposition(
            auth=ComposedAuthLink(
                token_loader=token_loader,
                token_refresher=token_loader,
            ),
            split=SplitLink(
                left=AIOHttpLink(endpoint_url="http://localhost:7766/graphql"),
                right=GraphQLWSLink(ws_endpoint_url="ws://localhost:7766/graphql"),
                split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
            ),
        ),
    )

    omero_ark = Kluster(
        rath=y,
        repo=repo
    )
    return omero_ark


class DeployedKluster(Composition):
    """ A deployed omero_ark"""
    deployment: Deployment
    kluster: Kluster


def deployed() -> DeployedKluster:
    """Create a deployed omero_ark

    A deployed omero_ark is a composition of a deployment and a omero_ark.
    This means a fully functioning omero instance will be spun up when
    the context manager is entered.

    To inspect the deployment, use the `deployment` attribute.
    To interact with the omero_ark, use the `omero_ark` attribute.


    Returns
    -------
    DeployedOmeroArk
        _description_
    """
    return DeployedKluster(
        deployment=build_deployment(),
        kluster=build_deployed_kluster(),
    )
