import sqlalchemy as db


class TrustpilotPipeline:
    def process_item(self, item):
        return item


class DataBase():
    def __init__(self, url):
        self.engine = db.create_engine(url)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.tables = self.get_all_tables()


    def create_table(self, name_table, **kwargs):
        colums = [db.Column(k, v, primary_key = True) if 'id_' in k else db.Column(k, v) for k,v in kwargs.items()]
        db.Table(name_table, self.metadata, *colums)
        self.metadata.create_all(self.engine)
        print(f"Table : '{name_table}' are created succesfully")

    def read_table(self, name_table, return_keys=False):
        table = db.Table(name_table, self.metadata, autoload=True, autoload_with=self.engine, extend_existing=True)
        if return_keys:table.columns.keys()
        else : return table


    def add_row(self, name_table, **kwarrgs):
        name_table = self.read_table(name_table)

        stmt = (
            db.insert(name_table).
            values(kwarrgs)
        )
        self.connection.execute(stmt)

    def get_all_tables(self):
        inspector = db.inspect(self.engine)
        self.tables = inspector.get_table_names()
        return inspector.get_table_names()

    def update_row_by_id(self, name_table, id_review, **kwargs):
        name_table = self.read_table(name_table)
        stmt = (
            db.update(name_table).
            where(name_table.c.id_review == id_review).
            values(**kwargs)
        )
        self.connection.execute(stmt)
