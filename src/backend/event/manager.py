from typing import List, Callable, Dict, Any
from sqlalchemy import event
from database import get_db
from event import models


class ModelEventManager:
    def __init__(self, data_handlers: List[Callable] = None, exclude: List[str] = None):
        """
        Инициализирует менеджер событий модели.

        :param data_handlers: Список обработчиков данных.
        :param exclude: Список исключаемых полей при сериализации.
        """
        self.data_handlers = data_handlers or []
        self.exclude = exclude or []

    def register_event_listener(self, model, event_type: str):
        """
        Регистрирует слушателя событий для модели.

        :param model: Модель SQLAlchemy.
        :param event_type: Тип события (before_insert, before_update, before_delete).
        """

        @event.listens_for(model, event_type)
        def event_handler(mapper, connection, target):
            self.log_model_changes(event_type, target.__dict__)

    def register_event_listeners(self, model):
        """
        Регистрирует слушателей для нескольких типов событий модели.

        :param model: Модель SQLAlchemy.
        """
        event_types = ('before_insert', 'before_update', 'before_delete')
        for event_type in event_types:
            self.register_event_listener(model, event_type)

    def process_data_handlers(self, serialized_target: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обрабатывает данные с использованием списка обработчиков.

        :param serialized_target: Сериализованные данные.
        :return: Сериализованные данные после обработки.
        """
        for handler in self.data_handlers:
            serialized_target = handler(serialized_target)
        return serialized_target

    def log_model_changes(self, event_type: str, target: Dict[str, Any]):
        """
        Asynchronously log model changes.

        :param event_type: The type of event (before_insert, before_update, before_delete).
        :param target: The target of the change (dictionary of model fields).
        """
        excluded_keys = set(self.exclude)
        serialized_target = {key: value for key, value in target.items() if key not in excluded_keys}
        serialized_target = self.process_data_handlers(serialized_target)

        print(event_type, serialized_target)

        for db in get_db():
            models.EventHistory(type=event_type, data=serialized_target)
            db.add(event)
            db.commit()
