import pymongo

class CoreRepository:
    data_base: None

    def __init__(self, name_db: str):

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.data_base = myclient[name_db]

    def create_collection(self, name_col: str):

        table = self.data_base[name_col]
        return table

