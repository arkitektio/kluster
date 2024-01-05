from kluster.deployed import deployed
from kluster.api.schema import acreate_dask_cluster
import asyncio

app = deployed()
app.deployment.project.overwrite = True
app.deployment.health_on_enter = True


async def main():
    async with app:
        async with app.deployment.logswatcher("kluster_gateway"):
            cluster = await acreate_dask_cluster("mikro")
            print(cluster)


asyncio.run(main())
