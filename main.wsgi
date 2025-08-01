import sys
import os

sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from wow import create_app

application=create_app()