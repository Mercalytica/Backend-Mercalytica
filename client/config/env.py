from dotenv import load_dotenv
import os

class EnvConfig:
     def __init__(self, env_file: str = ".env"):
          load_dotenv(env_file)
     
     def get(self, key: str):
          return os.getenv(key)