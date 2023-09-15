from sqlalchemy import select, or_, func
from customers import models


async def get_customers(db, page: int = 1, per_page: int = 10, search: str = ''):
    stmt = select(models.Customers)

    if search:
        stmt = stmt.where(or_(
            models.Customers.name.ilike(f'%{search}%'),
            models.Customers.iin.ilike(f'%{search}%'),
            models.Customers.tag.ilike(f'%{search}%')
        ))
    stmt = stmt.limit(per_page).offset((page - 1) * per_page)
    result = await db.execute(stmt)
    customers = result.scalars().all()
    return customers


async def get_customers_count(db):
    stmt = select(func.count()).select_from(models.Customers)
    result = await db.execute(stmt)
    count = result.scalar()
    return count


async def get_customers_search_count(db, search: str = ''):
    stmt = select(models.Customers)
    if search:
        stmt = stmt.where(or_(
            models.Customers.name.ilike(f'%{search}%'),
            models.Customers.iin.ilike(f'%{search}%'),
            models.Customers.tag.ilike(f'%{search}%')
        ))
    result = await db.execute(stmt)
    count = len(result.fetchall())
    return count


async def add_customers(db, **kwargs):
    customers = models.Customers(name=kwargs['name'], iin=kwargs['iin'])
    db.add(customers)
    await db.commit()
