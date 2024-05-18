
from google.maps import routing_v2


async def sample_compute_routes():
    # Create a client
    client = routing_v2.RoutesAsyncClient()

    # Initialize request argument(s)
    request = routing_v2.ComputeRoutesRequest(
    )

    # Make the request
    response = await client.compute_routes(request=request)

    # Handle the response
    print(response)


sample_compute_routes()
