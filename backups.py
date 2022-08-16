from imports import *
import global_vars

# conn - client, db_name = db, collections - use list collection names
# https://gist.github.com/Lh4cKg/939ce683e2876b314a205b3f8c6e8e9d
def dump(path):
    """
    MongoDB Dump
    :param collections: Database collections name
    :param conn: MongoDB client connection
    :param db_name: Database name
    :param path:
    :return:
    
    >>> DB_BACKUP_DIR = '/path/backups/'
    >>> conn = MongoClient("mongodb://admin:admin@127.0.0.1:27017", authSource="admin")
    >>> db_name = 'my_db'
    >>> collections = ['collection_name', 'collection_name1', 'collection_name2']
    >>> dump(collections, conn, db_name, DB_BACKUP_DIR)
    """
    database = global_vars.db
    collections_list = db.list_collection_names()
    for collection in collections_list:
        with open(os.path.join(path, f'{collection}.bson'), 'wb+') as f:
            for doc in db[collection].find():
                f.write(bson.BSON.encode(doc))


def restore(path):
    """
    MongoDB Restore
    :param path: Database dumped path
    :param conn: MongoDB client connection
    :param db_name: Database name
    :return:
    
    >>> DB_BACKUP_DIR = '/path/backups/'
    >>> conn = MongoClient("mongodb://admin:admin@127.0.0.1:27017", authSource="admin")
    >>> db_name = 'my_db'
    >>> restore(DB_BACKUP_DIR, conn, db_name)
    
    """
    db = global_vars.db
    for collection in os.listdir(path):
        if collection.endswith('.bson'):
            with open(os.path.join(path, collection), 'rb+') as f:
                db[collection.split('.')[0]].insert_many(bson.decode_all(f.read()))


#dump(path)

