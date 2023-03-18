from dotenv import load_dotenv
import os

load_dotenv()

INFURA_WS_URL = os.getenv("INFURA_WS_URL")
TEST_ADDRESS = os.getenv("TEST_ADDRESS")
TEST_PRIVATE_KEY = os.getenv("TEST_ADDRESS_PRIVATE_KEY")
MM_ADDRESS = os.getenv("MM_ADDRESS")
MM_PRIVATE_KEY = os.getenv("MM_PRIVATE_KEY")
