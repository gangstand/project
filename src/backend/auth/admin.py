from auth_settings import AuthJWT
from sqladmin import ModelView
from fastapi.responses import RedirectResponse
from fastapi import Request, Depends
from sqladmin.authentication import AuthenticationBackend
from auth.models import Role, User, UserRoleAssociation
from auth.utils import auth, verify_password
from database import get_db


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request, authorize: AuthJWT = Depends()) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        async for session in get_db():
            data = await auth(session, email=username)

            if not data:
                return False

            if not data.is_superuser:
                return False

            if verify_password(password=password, hashed_password=data.hashed_password.encode()):
                access_token = AuthJWT(request).create_access_token(subject=username)
                request.session.update({"token": access_token})
            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | bool:
        token = request.session.get("token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        return True


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

    column_labels = {
        User.email: "Почта", User.roles: "Роли", User.last_name: "Фамилия", User.first_name: "Имя",
        User.middle_name: "Отчество", User.is_superuser: "Администратор", User.avatar: "Фотография",
        User.is_verified: "Подтвержнём"
    }

    column_list = [
        User.id, User.email, User.roles, User.last_name,
        User.first_name, User.middle_name,
        User.is_verified, User.is_superuser
    ]

    column_searchable_list = [User.email, User.last_name, User.first_name, User.middle_name]
    column_formatters = {User.roles: lambda m, a: [role.name for role in m.roles]}
    column_formatters_detail = {User.roles: lambda m, a: [role.name for role in m.roles]}

    form_excluded_columns = [User.hashed_password, User.roles]


class RoleAdmin(ModelView, model=Role):
    name = "Роль"
    name_plural = "Роли"
    icon = "fa-solid fa-marker"

    column_list = [Role.id, Role.name, Role.users]
    column_labels = {Role.name: "Название", Role.users: "Пользователи"}

    column_searchable_list = [Role.name]
    column_formatters = {Role.users: lambda m, a: [role.email for role in m.users]}
    column_formatters_detail = {Role.users: lambda m, a: [role.email for role in m.users]}

    form_excluded_columns = [Role.users]


class UserRoleAdmin(ModelView, model=UserRoleAssociation):
    name = "Связь роли"
    name_plural = "Связь ролей"
    icon = "fa-solid fa-paperclip"
    form_include_pk = True
    column_list = [UserRoleAssociation.user_id, UserRoleAssociation.role_id]
