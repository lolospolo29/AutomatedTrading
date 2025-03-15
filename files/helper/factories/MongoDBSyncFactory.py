from files.helper.observer.MongoDBSyncObserver import MongoDBSyncObserver


class MongoDBSyncFactory:
    @staticmethod
    def create_sync_watcher(client1_uri, client2_uri, db_name, collection_name):
        return MongoDBSyncObserver(client1_uri, client2_uri, db_name, collection_name)