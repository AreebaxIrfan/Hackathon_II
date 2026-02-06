import asyncio
from src.database import engine
from sqlmodel import select
from src.models.user import User
from sqlmodel.ext.asyncio.session import AsyncSession

async def check():
    async with AsyncSession(engine) as session:
        result = await session.exec(select(User))
        users = result.all()
        print(f"Total users: {len(users)}")
        for i, u in enumerate(users):
            print(f"{i+1}. User: {u.email} (ID: {u.id})")

if __name__ == "__main__":
    asyncio.run(check())
