import tornado.ioloop as tloop
from sqlalchemy import create_engine

from app import app_loader as aloader

if __name__ == "__main__":
    print("starting.. at localhost:8888")
    sqlite_engine = create_engine("sqlite:///widgets.db")
    aloader.initDb(sqlite_engine)
    app = aloader.make_app(sqlite_engine)
    app.listen(8888)
    tloop.IOLoop.current().start()
