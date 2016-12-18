import requests
import json

TX_API = "https://blockexplorer.com/api/txs/?address={}&pageNum={}"


def get_txs(address):
    try:
        resp = requests.get(TX_API.format(address, 0)).json()
        num_pages = resp["pagesTotal"]
        if num_pages > 10:
            return []
        txs = resp["txs"]
        for page in range(num_pages):
            txs.extend(
                requests.get(TX_API.format(address, page)).json()["txs"]
            )
        return txs
    except json.decoder.JSONDecodeError:
        return []
    except KeyError:
        return []
