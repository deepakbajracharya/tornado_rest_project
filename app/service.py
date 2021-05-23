from typing import List

from .models import Widget

from sqlalchemy.orm import sessionmaker

Session = sessionmaker()


class WidgetService:
    def __init__(self, engine):
        self.engine = engine

    def widgetCountSync(self) -> int:
        with Session(bind=self.engine) as session:
            return session.query(Widget).count()

    async def widgetCount(self) :
        return self.widgetCountSync()

    def findWidgetByIdSync(self, widget_id: int) -> Widget:
        with Session(bind=self.engine) as session:
            return session.query(Widget).filter(Widget.id == widget_id).first()

    async def findWidgetById(self, widget_id: int) -> Widget:
        return self.findWidgetByIdSync(widget_id)

    def deleteWidgetByIdSync(self, widget_id: int) -> int:
        with Session(bind=self.engine) as session:
            widget = session.query(Widget).filter(Widget.id == widget_id).one()
            ret_id = widget.id
            session.delete(widget)
            session.commit()
            return ret_id

    async def deleteWidgetById(self, widget_id: int) -> int:
        return self.deleteWidgetByIdSync(widget_id)

    def updateWidgetSync(self, widget_id: int, data: {}) -> Widget:
        if data:
            with Session(bind=self.engine) as session:
                widget = session.query(Widget).filter(
                    Widget.id == widget_id).one()
                if widget:
                    for key in [
                            x for x in data.keys() if x in [
                                'name', 'number_of_parts']]:
                        setattr(widget, key, data[key])

                    session.commit()
                    widget = session.query(Widget).filter(
                        Widget.id == widget_id).one()
                    return widget

        return None

    async def updateWidget(self, widget_id: int, data: {}) -> Widget:
        return self.updateWidgetSync(widget_id, data = data)

    def listWidgetsSync(self, page_size: int = 50, page: int = 1) -> List:
        with Session(bind=self.engine) as session:
            return session.query(Widget).all(
            )[page_size * (page - 1) : page_size * page]

    async def listWidgets(self, page_size: int = 50, page: int = 1) -> List:
        return self.listWidgetsSync(page_size=page_size, page=page)

    def newWidgetSync(self, widget: Widget) -> int:
        with Session(bind=self.engine) as session:
            session.add(widget)
            session.commit()
            return widget.id

    async def newWidget(self, widget: Widget) -> int:
        return self.newWidgetSync(widget)

    async def deleteWidget(self, id):
        with Session(bind=self.engine) as session:
            widget = session.query(Widget).filter(Widget.id == id).first()
            if widget:
                ret_id = widget.id
                session.delete(widget)
                session.commit()
                return ret_id
        return None
