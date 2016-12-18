from blockexplorer import get_txs
import sys


ADDRESS = "3QzYvaRFY6bakFBW4YBRrzmwzTnfZcaA6E"
DEPTH = 2
CONNECTION = '"{}" -> "{}" [label="{}"]'


def tx_is_out(tx, address):
    for v in tx['vin']:
        if v['addr'] == address:
            return True
    return False


def get_connections(address, depth, processed_addrs=[]):
    sys.stderr.write("Address: {}, depth: {}\n".format(address, depth))
    connections = []
    txs = get_txs(address)
    sys.stderr.write("Transactions: {}\n".format(len(txs)))
    processed_addrs.append(address)
    for tx in txs:
        if tx_is_out(tx, address):
            for v in tx['vout']:
                to_addr = v['scriptPubKey']['addresses'][0]
                connections.append(CONNECTION.format(
                    address,
                    to_addr,
                    v['value']
                ))
                if depth > 0 and to_addr not in processed_addrs:
                    connections.extend(
                        get_connections(
                            to_addr,
                            depth - 1
                        )
                    )
        else:
            for v in tx['vin']:
                from_addr = v['addr']
                connections.append(CONNECTION.format(
                    from_addr,
                    address,
                    v['value']
                ))
                if depth > 0 and from_addr not in processed_addrs:
                    connections.extend(
                        get_connections(
                            from_addr,
                            depth - 1
                        )
                    )
    return connections


if __name__ == '__main__':
    print("digraph g {")
    print("\n".join(get_connections(ADDRESS, DEPTH)))
    print("}")
