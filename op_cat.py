import nest_asyncio
nest_asyncio.apply()
import asyncio
from pathlib import Path
from bsv import PrivateKey, P2PKH, ARC, Transaction, TransactionInput, TransactionOutput, Script
from bsv.constants import OpCode
from bsv.utils import encode_pushdata
import requests
import json


moj_klucz = "KwVs88aLx6............"
klucz_prywatny = PrivateKey(moj_klucz)
address_testnet = klucz_prywatny.address(network = "testnet")


url = f"https://api.whatsonchain.com/v1/bsv/test/address/{address_testnet}/confirmed/balance"
response = requests.get(url)
data = response.json()
saldo = data['confirmed']
print(f"Adres testnet : {address_testnet}")
print(f"Saldo : {saldo} satoshi / {saldo / 100000000} BSV")

url = f"https://api.whatsonchain.com/v1/bsv/test/address/{address_testnet}/unspent/all"
response = requests.get(url)
data = response.json()
print(data)
        
txid = input("Wpisz txid:")
print(f"\nTransakcja z niewydanym UTXO: {txid}")
tx_pos = int(input("Wpisz tx_pos:"))
print(f"Indeks transakcji: {tx_pos}\n")


url = f"https://api.whatsonchain.com/v1/bsv/test/tx/{txid}/hex"
response = requests.get(url)
tx_hex = response.text
print(f"HEX : {tx_hex}\n")

do_wyslania = 1111

def locking_script():
    chunks = [
        OpCode.OP_CAT,
        encode_pushdata(b'hello world'),
        OpCode.OP_EQUAL
    ]

    return Script(b''.join(chunks))

input("Wyślij//")

async def create_and_broadcast_nft():
    
    
    source_tx = Transaction.from_hex(tx_hex)
    
    output = TransactionOutput(
        locking_script=locking_script(),
        satoshis=do_wyslania
    )
    
    change_output = TransactionOutput(
        locking_script=P2PKH().lock(address_testnet),
        change=True
    )
    tx_input = TransactionInput(
        source_transaction=source_tx,
        source_txid=source_tx.txid(),
        source_output_index=tx_pos,
        unlocking_script_template=P2PKH().unlock(klucz_prywatny),
        
    )

    tx = Transaction([tx_input], [output, change_output])

    tx.fee()
    tx.sign()
    api_key = 'testnet_2d...............'
    response = await tx.broadcast(ARC('https://api.taal.com/arc', api_key))
    print(f"Status rozgłoszenia: {response.status}")
    print(f"ID transakcji: {tx.txid()}")

    
if __name__ == "__main__":
    asyncio.run(create_and_broadcast_nft())

