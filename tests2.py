from tornado.testing import AsyncHTTPTestCase
from tornado.escape import json_encode, json_decode

from sqlalchemy import create_engine
from sqlalchemy_utils.functions import drop_database

from app import app_loader as aloader
from app.service import WidgetService
from app.models import Widget


class ApiTest(AsyncHTTPTestCase):

    def get_app(self):
        self.testdb_url = "sqlite:///widgets_tests.db"
        try:
            drop_database(self.testdb_url)
        except Exception:
            pass

        self.sqlite_engine = create_engine(self.testdb_url)
        aloader.initDb(self.sqlite_engine)
        application = aloader.make_app(self.sqlite_engine)
        return application

    def test_homepage(self):
        response = self.fetch('/')
        assert response.code == 200

    def test_get_widgets(self):
        response = self.fetch('/widgets')
        assert response.code == 200
        retJson = json_decode(response.body.decode("utf-8"))
        assert len(retJson["data"]) > 0

    def test_create_widget(self):
        widgetObj = {
            "name" : "widget_being_created",
            "number_of_parts" : 11
        }

        response = self.fetch("/widgets", method="POST",
                              body=json_encode(widgetObj))
        assert response.code == 201

    def test_update_widget(self):
        widget = Widget(name="TobeUpdated", number_of_parts=11)
        widgetService = WidgetService(self.sqlite_engine)
        widgetId = widgetService.newWidgetSync(widget)

        widgetObj = {
            "name" : "widget_update",
            "number_of_parts" : 11
        }
        response = self.fetch("/widgets/{}".format(widgetId),
                              method="PUT",
                              body=json_encode(widgetObj))
        assert response.code == 200
        widgetJson = json_decode(response.body)
        assert widgetJson["name"] == "widget_update"
        assert widgetJson["number_of_parts"] == 11

    def test_delete_widget(self):
        widget = Widget(name="TobeUpdated", number_of_parts=11)
        widgetService = WidgetService(self.sqlite_engine)
        widgetId = widgetService.newWidgetSync(widget)

        response = self.fetch("/widgets/{}".format(widgetId),
                              method="DELETE")
        assert response.code == 204
