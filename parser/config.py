from dotenv import load_dotenv
import os

os.environ.pop("TAB", None)

load_dotenv()

TAB = os.getenv("TAB")
