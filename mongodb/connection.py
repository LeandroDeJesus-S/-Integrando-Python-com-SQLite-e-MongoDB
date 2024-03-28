"""
Modulo responsável pelos objetos que fazem a conexão com o MongoDB.
"""
import os
import pymongo
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from contextlib import AbstractContextManager


class MongoDB(AbstractContextManager):
    """Context manager para criar a conexão com o mongoDB
    """
    def __init__(self) -> None:
        self.__dbclient = None
        load_dotenv()

        _base_uri = 'mongodb+srv://<username>:<password>@<project>/?retryWrites=<retryWrites>&w=<w>&appName=<appName>'
        DB_USER = os.getenv('MONGODB_USER')
        DB_PASS = os.getenv('MONGODB_PASS')
        DB_PROJECT = os.getenv('DB_PROJECT')
        RETRYWRITES = os.getenv('retryWrites')
        W = os.getenv('w') 
        APPNAME = os.getenv('appName')

        _base_uri = _base_uri.replace('<username>', DB_USER)
        _base_uri = _base_uri.replace('<password>', DB_PASS)
        _base_uri = _base_uri.replace('<project>', DB_PROJECT)
        _base_uri = _base_uri.replace('<retryWrites>', RETRYWRITES)
        _base_uri = _base_uri.replace('<w>', W)
        _base_uri = _base_uri.replace('<appName>', APPNAME)

        self.DB_URI = _base_uri

    def __enter__(self) -> pymongo.MongoClient:
        self.__dbclient = pymongo.MongoClient(
            host=self.DB_URI, 
            server_api=ServerApi('1'), 
            connectTimeoutMS=60000
        )
        return self.__dbclient
    
    def  __exit__(self, *_) -> None:
        self.__dbclient.close()
