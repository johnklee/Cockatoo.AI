import os
from dotenv import load_dotenv, find_dotenv


_ = load_dotenv(find_dotenv(os.path.expanduser('~/.env')))
