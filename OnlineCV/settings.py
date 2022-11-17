# -*- coding: utf-8 -*-
"""Application configuration."""
import os
import boto3
import json
import secrets
from datetime import timedelta
from botocore.exceptions import ClientError


class Config(object):
    """Base configuration."""
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

    @staticmethod
    def get_secret(secret_name, region_name='eu-west-1'):
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
    SECRET_KEY = Config.get_secret('OnlineCV/FLASK_SECRET')
    # flask-caching
    CACHE_TYPE = 'MemcachedCache'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_MEMCACHED_SERVERS = (
        'onlinecvmemcached.0ne2f9.0001.euw1.cache.amazonaws.com:11211',
        'onlinecvmemcached.0ne2f9.0002.euw1.cache.amazonaws.com:11211',
        'onlinecvmemcached.0ne2f9.0003.euw1.cache.amazonaws.com:11211'
    )
    CACHE_OPTIONS = {}
    # SQLAlchemy
    DB_CONFIG_OBJ = Config.get_secret('OnlineCV/production/RDS_POSTGRES_PASSWORD')
    DB_HOSTNAME = DB_CONFIG_OBJ['host']
    DB_PORT = DB_CONFIG_OBJ['port']
    DB_USERNAME = DB_CONFIG_OBJ['username']
    DB_PASSWORD = DB_CONFIG_OBJ['password']
    DB_INSTANCE_ID = DB_CONFIG_OBJ['dbInstanceIdentifier']
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_INSTANCE_ID}'


class DevConfig(Config):
    """Development configuration."""
    ENV = 'development'
    DEBUG = True
    SECRET_KEY = Config.get_secret('OnlineCV/FLASK_SECRET')
    # flask-caching
    CACHE_TYPE = 'MemcachedCache'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_MEMCACHED_SERVERS = (
        'onlinecvmemcached-gamma.0ne2f9.0001.euw1.cache.amazonaws.com:11211',
        'onlinecvmemcached-gamma.0ne2f9.0002.euw1.cache.amazonaws.com:11211'
    )
    DB_CONFIG_OBJ = Config.get_secret('OnlineCV/development/RDS_POSTGRES_PASSWORD')
    DB_HOSTNAME = DB_CONFIG_OBJ['host']
    DB_PORT = DB_CONFIG_OBJ['port']
    DB_USERNAME = DB_CONFIG_OBJ['username']
    DB_PASSWORD = DB_CONFIG_OBJ['password']
    DB_INSTANCE_ID = DB_CONFIG_OBJ['dbInstanceIdentifier']
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_INSTANCE_ID}'


class TestConfig(Config):
    """Test configuration."""
    ENV = 'testing'
    TESTING = True
    DEBUG = True
    SECRET_KEY = os.environ.get('FLASK_SECRET') if os.environ.get('FLASK_SECRET') else secrets.token_hex(16)
    DB_NAME = '../test.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
    # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    BCRYPT_LOG_ROUNDS = 4
