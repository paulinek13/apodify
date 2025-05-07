from apodify.common import init_apodify
from apodify.apod_api import APODClient

init_apodify()

apod_client = APODClient()
apod_data = apod_client.get.date("2025-01-01")
