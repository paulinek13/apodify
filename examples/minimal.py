from apodify.common import init_apodify
from apodify.apod_api.apod_client import APODClient

init_apodify()

apod_client = APODClient(api_key="DEMO_KEY")
apod_data = apod_client.get_apod("2025-01-01")
