from dotenv import load_dotenv
import os

os.environ.pop("BOT_TOKEN", None)
os.environ.pop("PRODUCTS_PER_PAGE", None)
os.environ.pop("CURRENCY_API_URL", None)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PRODUCTS_PER_PAGE = int(os.getenv("PRODUCTS_PER_PAGE"))
CURRENCY_API_URL = os.getenv("CURRENCY_API_URL")
