from settings import WALLET, LAVE, TONCENTER_API_TOKEN, LAVE_JETTON_ADDRESS
import asyncio

from utils.wallet_api import TonApi
from database.transaction_db import Transactions
from database.wallet_db import Wallet
from utils.converter import from_nano
from utils.checker import get_raw_address
from utils.checker import Cell

from create_bot import dp, _

import logging

lave_headers = {
    'accept': 'application/json'
    }
lave_params = {
    'account': f'{get_raw_address(WALLET)}',
    'jetton_master': f'{get_raw_address(LAVE)}',
    'limit': '1000'
}

ton_headers = {
    'accept': 'application/json',
    'X-API-Key': f'{TONCENTER_API_TOKEN}'
}
ton_params = {
    'address': f'{WALLET}',
    'limit': '1000',
    'to_lt': '0',
    'archival': 'false'
}

transactions_db = Transactions()
wallet_db = Wallet()

def logger(reason, jetton_date):
    logging.info(
        f"Reason: {reason}" + "\n" +
        f"Date: {jetton_date}"
        )

async def sleep():
    await asyncio.sleep(30)

async def start():
    while True:
        print("Withdraw updated")
        await get_lave_payment()
        await get_ton_payment()
        await sleep()

async def get_ton_payment():
    tonapi = TonApi('https://toncenter.com/api/v2/getTransactions', ton_params, ton_headers)
    data = tonapi.connect()
    
    if data is None:
        await sleep()
        return
    
    for message in data["result"]:
        value = message['in_msg']['value']
        hash = message['transaction_id']['hash']
        
        if value.isdigit() == False:
            logger("Value isn't int", hash)
            return

        value = int(value)

        if value >= 100:
            value = from_nano(value)
            
            if "in_msg" not in message:
                logger("No comment", hash)
                continue
            
            if "message" not in message["in_msg"]:
                logger("No comment", hash)
                continue
            
            comment = message["in_msg"]["message"]
            
            checker = await transactions_db.check_transaction(hash, comment)
            
            if checker is True:
                continue
            
            await transactions_db.add_transaction(hash, comment)
            
            if comment.isdigit() == False:
                logger("Comment not id", comment)
                continue

            checker = await wallet_db.get_lave(comment)

            if checker is None:
                logger("User wasn't found", hash)
                continue

            await wallet_db.set_ton(int(comment), value, True)

            await dp.send_message(int(comment), "💸 Успешное пополнение {} TON !".format(value), parse_mode='HTML')

async def get_lave_payment():
    tonapi = TonApi('https://tonapi.io/v1/jetton/getHistory', lave_params, lave_headers)
    events = tonapi.connect()

    if events is None:
        await sleep()
        return
    
    events = events["events"]

    for event in events:
        jetton_date = event['lt']
        
        for action in event["actions"]: # я знаю, что за цикл в цикле руки отрубают, но я не знаю, как сделать это лучше, простите
            
            if "JettonTransfer" not in action:
                logger("No jetton data", jetton_date)
                continue
            
            transfer = action["JettonTransfer"]
            
            jetton = transfer["jetton"] 
            if jetton["address"] != LAVE_JETTON_ADDRESS:
                logger("Jetton isn't LAVE", jetton["address"])
                continue
            
            amount = from_nano(transfer["amount"])
            
            if "comment" not in transfer:
                logger("No comment", jetton_date)
                continue
            
            comment = transfer["comment"]
            
            if comment.isdigit() == False:
                logger("Comment not id", jetton_date)
                continue 
            
            checker = await transactions_db.check_transaction(jetton_date, comment) # add comment, for more security cuz it can be that 2 lt will be the same

            if checker is True:
                continue
            
            await transactions_db.add_transaction(jetton_date, comment)

            checker = await wallet_db.get_lave(comment)

            if checker is None:
                logger("User wasn't found", jetton_date)
                continue

            await wallet_db.set_lave(int(comment), amount, True)
            
            print(f"User sended {amount} | {comment}")
            
            await dp.send_message(int(comment), "💸 Успешное пополнение {} LAVE !".format(amount), parse_mode='HTML')
            
    await asyncio.sleep(5)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="deposit_looper.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
    
    asyncio.run(start())