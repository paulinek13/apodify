from apodify.common import init_apodify
from apodify.apod_api import APODClient
from apodify.enhancer import enhance_apod

init_apodify()

apod_client = APODClient()
apod_data = apod_client.get.date("2025-01-01")

enhanced = enhance_apod(apod_data)
