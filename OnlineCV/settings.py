# -*- coding: utf-8 -*-
"""Application configuration."""
import os
import boto3
import json
from datetime import timedelta
from botocore.exceptions import ClientError

class Config(object):
    """Base configuration."""
    SECRET_KEY = os.environ.get('FLASK_SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    # "MemcachedCache", "RedisCache", etc.
    CACHE_TYPE = 'SimpleCache'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGIN_WHITELIST = [
        'http://0.0.0.0:4100',
        'http://localhost:4100',
        'http://0.0.0.0:8000',
        'http://localhost:8000',
        'http://0.0.0.0:4200',
        'http://localhost:4200',
        'http://0.0.0.0:4000',
        'http://localhost:4000',
    ]
    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_AUTH_HEADER_PREFIX = 'Token'
    JWT_HEADER_TYPE = 'Token'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(10 ** 6)
    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    def get_db_config_obj(stage):
        secret_name = f'OnlineCV/{stage}/RDS_POSTGRES_PASSWORD'
        region_name = 'eu-west-1'
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e

        return json.loads(get_secret_value_response['SecretString'])

class ProdConfig(Config):
    """Production configuration."""
    ENV = 'production'
    DEBUG = False
    DB_CONFIG_OBJ = Config.get_db_config_obj(ENV)
    DB_HOSTNAME = DB_CONFIG_OBJ['host']
    DB_PORT = DB_CONFIG_OBJ['port']
    DB_USERNAME = DB_CONFIG_OBJ['username']
    DB_PASSWORD =  DB_CONFIG_OBJ['password']
    DB_INSTANCE_ID = DB_CONFIG_OBJ['dbInstanceIdentifier']
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_INSTANCE_ID}'

class DevConfig(Config):
    """Development configuration."""
    ENV = 'development'
    DEBUG = True
    DB_CONFIG_OBJ = Config.get_db_config_obj(ENV)
    DB_HOSTNAME = DB_CONFIG_OBJ['host']
    DB_PORT = DB_CONFIG_OBJ['port']
    DB_USERNAME = DB_CONFIG_OBJ['username']
    DB_PASSWORD = DB_CONFIG_OBJ['password']
    DB_INSTANCE_ID = DB_CONFIG_OBJ['dbInstanceIdentifier']
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_INSTANCE_ID}'

class TestConfig(Config):
    """Test configuration."""
    TESTING = True
    DEBUG = True
    DB_NAME = '../test.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
    # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    BCRYPT_LOG_ROUNDS = 4
