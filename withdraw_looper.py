from tonsdk.contract.token.ft import JettonWallet
from tonsdk.utils import Address, to_nano
from tonsdk.contract.wallet import WalletVersionEnum, Wallets
from tonsdk.utils import bytes_to_b64str
from tonsdk.provider import ToncenterClient, prepare_address, address_state
from tonsdk.utils import TonCurrencyEnum, from_nano
from tonsdk.boc import Cell
from tonsdk.provider import parse_response
from database.withdraw_db import WithdrawHistory

import asyncio
import aiohttp
import requests
from abc import ABC, abstractmethod
from tvm_valuetypes import serialize_tvm_stack

from settings import wallet_mnemonics, TONCENTER_API_TOKEN, WALLET, LAVE
import nest_asyncio

nest_asyncio.apply()

class AbstractTonClient(ABC):
    @abstractmethod
    def _run(self, to_run, *, single_query=True):
        raise NotImplemented

    def get_address_information(self, address: str,
                                currency_to_show: TonCurrencyEnum = TonCurrencyEnum.ton):
        return self.get_addresses_information([address], currency_to_show)[0]

    def get_addresses_information(self, addresses,
                                  currency_to_show: TonCurrencyEnum = TonCurrencyEnum.ton):
        if not addresses:
            return []

        tasks = []
        for address in addresses:
            address = prepare_address(address)
            tasks.append(self.provider.raw_get_account_state(address))

        results = self._run(tasks, single_query=False)

        for result in results:
            result["state"] = address_state(result)
            if "balance" in result:
                if int(result["balance"]) < 0:
                    result["balance"] = 0
                else:
                    result["balance"] = from_nano(
                        int(result["balance"]), currency_to_show)

        return results
    
    def seqno(self, addr: str):
        addr = prepare_address(addr)
        result = self._run(self.provider.raw_run_method(addr, "seqno", []))

        if 'stack' in result and ('@type' in result and result['@type'] == 'smc.runResult'):
            result['stack'] = serialize_tvm_stack(result['stack'])

        return result

    def send_boc(self, boc: Cell):
        return self._run(self.provider.raw_send_message(boc))


class TonCenterTonClient(AbstractTonClient):
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.provider = ToncenterClient(base_url="https://toncenter.com/api/v2/",
                                        api_key=TONCENTER_API_TOKEN)

    def _run(self, to_run, *, single_query=True):
        try:
            return self.loop.run_until_complete(
                self.__execute(to_run, single_query)
                )
        except Exception:  # ToncenterWrongResult, asyncio.exceptions.TimeoutError, aiohttp.client_exceptions.ClientConnectorError
            raise

    async def __execute(self, to_run, single_query):
        timeout = aiohttp.ClientTimeout(total=5)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            if single_query:
                to_run = [to_run]

            tasks = []
            for task in to_run:
                tasks.append(task["func"](
                    session, *task["args"], **task["kwargs"]))

            return await asyncio.gather(*tasks)

_, _, _, wallet = Wallets.from_mnemonics(
        wallet_mnemonics, 
        WalletVersionEnum.v4r2,
        0
    )

headers = {'accept': '*/*','Content-Type': 'application/json',}

client = TonCenterTonClient()
withdraw_db = WithdrawHistory()

async def withdraw_lave(user_id, address, count):
    jetton_data = JettonWallet().create_transfer_body(
            Address(address), # address where lave'll send
            to_nano(count, "ton") # jettons amount
        )

    query = wallet.create_transfer_message(
        to_addr=LAVE, # LAVE contract address
        amount=to_nano(0.1, "ton"), # TON amount for send
        seqno=parse_response(client.seqno(wallet.address.to_string())[0]), # seqno from seed phrase
        payload=jetton_data
    )

    data = {'boc': bytes_to_b64str(query["message"].to_boc(False))}

    response = requests.post('https://tonapi.io/v1/send/boc', headers=headers, json=data)

    if response.status_code == 200:
        print(f"💸 Вывод {count} LAVE на кошелёк {WALLET} прошел успешно | {user_id}")
    else:
        print(response.content)
        print(f"😢 Ошибка отпраки токенов на кошелёк: {WALLET} | {user_id}" + "\n" + 
                              "Сообщите в тех. поддержку")

async def main():
    while True:
        queue = await withdraw_db.get_all_addresses()

        if len(queue) == 0:
            await asyncio.sleep(30)

        for user in queue:
            await withdraw_lave(user[1], user[2], user[3])
            await withdraw_db.delete_withdraw(user[1])
            await asyncio.sleep(5)

        await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())