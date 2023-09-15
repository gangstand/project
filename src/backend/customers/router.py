from fastapi import HTTPException, Depends, APIRouter, Query
from auth_settings import AuthJWT
from sqlalchemy.orm import Session
from starlette import status
from customers.schemas import Customer
from customers.utils import get_customers, get_customers_count, get_customers_search_count, add_customers
from database import get_db

router = APIRouter(prefix="/api/customer", tags=["Customer"], responses={404: {"description": "Not found"}})


@router.get("/", status_code=status.HTTP_200_OK)
async def get_me_customer(
        page: int = Query(1, gt=0),
        per_page: int = Query(10, gt=0, le=100),
        search: str = Query('', alias='search'),
        authorize: AuthJWT = Depends(),
        db: Session = Depends(get_db)
):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from e
    customers = await get_customers(db, page=page, per_page=per_page, search=search)
    count = await get_customers_count(db)
    if search:
        count = await get_customers_search_count(db, search)
    result = {"customers": customers, "count": count}
    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_signup(customer: Customer, db: Session = Depends(get_db)):
    await add_customers(db, name=customer.name, iin=customer.iin)
    return {"message": "success"}
