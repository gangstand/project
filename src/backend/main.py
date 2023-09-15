import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from auth.admin import UserAdmin, AdminAuth, RoleAdmin, UserRoleAdmin
from auth.router import router as auth_router
from customers.router import router as customers_router
from customers.admin import CustomersAdmin
from database import engine

load_dotenv()

app = FastAPI(
    title="API",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)
authentication_backend = AdminAuth(secret_key=os.getenv('SECRET'))

app.mount("/media", StaticFiles(directory='media'), name="media")


admin = Admin(
    app, engine, authentication_backend=authentication_backend, title="Администрация", templates_dir="./templates"
)

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://flagman-support.kulpinov.site/",
    "http://flagman-support.kulpinov.site/",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

admin.add_view(UserAdmin)
admin.add_view(RoleAdmin)
admin.add_view(UserRoleAdmin)
admin.add_view(CustomersAdmin)

app.include_router(auth_router)
app.include_router(customers_router)
