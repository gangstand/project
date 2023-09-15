from sqladmin import ModelView

from customers.models import Customers


class CustomersAdmin(ModelView, model=Customers):
    name = "Клиент"
    name_plural = "Клиенты"
    icon = "fa-solid fa-address-book"

    column_list = [Customers.id, Customers.iin, Customers.name, Customers.tag]
    column_labels = {Customers.iin: "ИИН", Customers.name: "Имя", Customers.tag: "Сервисный тег"}
    column_searchable_list = [Customers.iin, Customers.name, Customers.tag]
