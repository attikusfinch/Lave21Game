from tonsdk.contract.token.ft import JettonWallet
from tonsdk.utils import Address, to_nano
from tonsdk.contract.wallet import WalletVersionEnum, Wallets
from tonsdk.utils import bytes_to_b64str

from settings import wallet_mnemonics, TONCENTER_API_TOKEN, WALLET, LAVE

import requests
from abc import ABC, abstractmethod
import asyncio
import aiohttp
from tvm_valuetypes import serialize_tvm_stack

from tonsdk.provider import ToncenterClient, SyncTonlibClient, prepare_address, address_state
from tonsdk.utils import TonCurrencyEnum, from_nano
from tonsdk.boc import Cell
from tonsdk.provider import parse_response

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
                self.__execute(to_run, single_query))

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


class TonLibJsonTonClient(AbstractTonClient):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.provider = SyncTonlibClient(config="./.tonlibjson/testnet.json",
                                         keystore="./.tonlibjson/keystore",
                                         cdll_path="./.tonlibjson/linux_libtonlibjson.so")  # or macos_libtonlibjson.dylib
        self.provider.init()

    def _run(self, to_read, *, single_query=True):
        try:
            if not single_query:
                queries_order = {query_id: i for i,
                                 query_id in enumerate(to_read)}
                return self.provider.read_results(queries_order)

            else:
                return self.provider.read_result(to_read)

        except Exception:  # TonLibWrongResult, TimeoutError
            raise


lave_count = 10000

_mnemonics, _pub_k, _priv_k, wallet = Wallets.from_mnemonics(
    wallet_mnemonics, 
    WalletVersionEnum.v4r2,
    0
)

headers = {'accept': '*/*','Content-Type': 'application/json',}

client = TonCenterTonClient()

query = wallet.create_transfer_message(
    to_addr=LAVE,
    amount=to_nano(0.01, "ton"), 
    seqno=parse_response(client.seqno(wallet.address.to_string())[0]), 
    payload=JettonWallet().create_transfer_body(Address(WALLET), lave_count)
)

data = {'boc': bytes_to_b64str(query["message"].to_boc(False))}

response = requests.post('https://tonapi.io/v1/send/boc', headers=headers, json=data)

if response.status_code == 200:
    print(f"Отправили {lave_count} токенов на кошелёк: {WALLET}")
else:
    print(f"Ошибка отпраки токенов на кошелёк: {WALLET}")