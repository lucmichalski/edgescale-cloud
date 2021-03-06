# SPDX-License-Identifier: Apache-2.0 OR MIT
# Copyright 2018-2019 NXP

import os
import psycopg2

import boto3
from DBUtils.PooledDB import PooledDB
from sqlalchemy import create_engine

from edgescale_pyutils.redis_utils import connect_redis
from edgescale_pymodels.base_model import session

# config data from postgres
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT","5432")
DATABASE = os.getenv("DATABASE","edgescale")
USER = os.getenv("DB_USER","root")
PASSWORD = os.getenv("DB_PASSWORD")

try:
    es_pool = PooledDB(
        creator=psycopg2,
        maxconnections=100,
        mincached=10,
        maxcached=10,
        maxusage=None,  # maximum number of reuses of a single connection
        host=DB_HOST,
        port=DB_PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    config_conn = es_pool.connection()
    config_cur = config_conn.cursor()
    sql = "select text from config"
    config_cur.execute(sql)
    config = config_cur.fetchone()[0].get("settings")
except Exception as e:
    print("Database connection failed. Error:", str(e))
    es_pool = None
finally:
    config_cur.close()
    config_conn.close()

HOST_SITE = config['HOST_SITE']

IS_DEBUG = config["DEBUG"]

# The k8s
_DNS = K8S_PUBLIC_DNS = config['APPSERVER_HOST']     # public DNS
K8S_PRIVATE_DNS = config['APPSERVER_HOST']
_PORT = APPSERVER_PORT = config['APPSERVER_PORT']

# The mqtt
MQTT_HOST = config['MQTT_HOST']

S3_LOG_URL = config['LOG_URL']

device_status_table = config['DEVICE_STATUS_TABLE']
HARBORPASSWD = config.get('HARBOR_ADMIN_PASS', 'Hharbor12345')

REDIS_HOST = config['REDIS_HOST']
REDIS_PORT = config['REDIS_PORT']
REDIS_PASSWD = config['REDIS_PASSWD']
REST_API_ID = config['REST_API_ID']
SHORT_REST_API_ID = config['REST_API_SHORT_ID']

engine_url = 'postgresql://{username}:{pwd}@{host}:{port}/{db}'.format(
    username=USER, pwd=PASSWORD, host=DB_HOST, port=DB_PORT, db=DATABASE
)

engine = create_engine(engine_url, pool_size=10)
session.configure(bind=engine)

redis_client = connect_redis(REDIS_HOST, port=REDIS_PORT, pwd=REDIS_PASSWD)
redis_client.rest_api_id = REST_API_ID
