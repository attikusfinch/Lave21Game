import asyncio
from database.wallet_db import Wallet

wallet_db = Wallet()

async def create_wallet():
    await wallet_db.add_wallet(1, 1000000, 1000000, "Some_address")
    
    await wallet_db.set_lave(1, 100000, True)
    user = await wallet_db.get_lave(1)
    
    print(user)

if __name__ == "__main__":
    asyncio.run(create_wallet())