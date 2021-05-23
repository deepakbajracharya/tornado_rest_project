import os
import swagger_ui
import tornado.web as tweb

from .handlers import WidgetListHandler, WidgetHandler
from .models import Base, Widget
from .app_swagger import generate_swagger_file

from sqlalchemy.orm import sessionmaker

SWAGGER_API_OUTPUT_FILE = os.path.join(
    os.path.dirname(__file__), "../swagger.yaml")


class MainHandler(tweb.RequestHandler):
    def get(self):
        self.write(
            """
            <b>Testing REST for Widget</b>
<ul>
<li>
    GET /widgets : Supports query parameters page and page_size for page no.
    and page size
</li>
<li>
    GET  /widgets/<id> Get widget by id
</li>
<li>
    DELETE /widgets/<id> Delete the widget
</li>
<li>
    POST /widgets: Create a new widget
    PUT   /widgets/<id>  Update the widget
    Expects name and number_of_parts in the Json object
    e.g. {"name": "Food Processor", "number_of_parts": 8685078}
</li>
</ul>
            """
        )


def make_app(engine):
    handlers = [
        (r"/", MainHandler),
        (r"/widgets", WidgetListHandler, {"engine": engine}),
        (r"/widgets/(\d+)", WidgetHandler, {"engine": engine}),
    ]
    app = tweb.Application(
        handlers
    )
    generate_swagger_file(SWAGGER_API_OUTPUT_FILE, handlers)
    swagger_ui.tornado_api_doc(
        app,
        config_path=SWAGGER_API_OUTPUT_FILE,
        url_prefix="/api/doc",
        title="Widget API",
    )
    return app


def initDb(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker()

    with Session(bind=engine) as session:
        session.add_all([
            Widget(name="widget0", number_of_parts=2),
            Widget(name="widget1", number_of_parts=5),
            Widget(name="widget2", number_of_parts=8),
            Widget(name="widget3", number_of_parts=2),
            Widget(name="widget4", number_of_parts=9),
            Widget(name="widget5", number_of_parts=12),
        ])
        session.commit()
