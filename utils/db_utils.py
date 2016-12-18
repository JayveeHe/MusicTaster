import json
import pymongo

from utils.config_utils import get_db_config

__author__ = 'jayvee'

db_config = get_db_config()
DB_IP = db_config['db_ip']
DB_PORT = db_config['db_port']


def get_db_inst(db_name, collection_name):
    client = pymongo.MongoClient(DB_IP, DB_PORT)
    try:
        db_inst = client.get_database(db_name).get_collection(collection_name)
        return db_inst
    except Exception, e:
        print 'error, details=%s' % (e)


def create_index(db_name, collection_name, index_conf):
    db_inst = get_db_inst(db_name, collection_name)
    print db_inst.create_indexes(index_conf)


def find_all(find_filter, db_inst, sort_filter=None):
    MAX_COUNT = db_inst.find(find_filter).count()

    if not sort_filter:
        db_inst.find(find_filter)
