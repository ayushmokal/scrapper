from dotenv import load_dotenv
import os

load_dotenv()

DEFAULT_ZIP_CODE = os.getenv('DEFAULT_ZIP_CODE', '10081')
BASE_URL = "https://health.usnews.com/doctors/search"
SEARCH_PARAMS = {
    'distance': '250',
    'np_pa': 'false',
    'specialty': 'Urology',
    'sort': 'distance'
}