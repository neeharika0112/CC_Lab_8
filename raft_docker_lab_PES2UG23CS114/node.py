import socket
import raftos
import asyncio
import sys
import logging

PORTS = {
    1: 8001,
    2: 8002,
    3: 8003,
    4: 8004,
    5: 8005
}

def resolve(name, port):
    return f"{socket.gethostbyname(name)}:{port}"


async def main(node_id):
    port = PORTS[node_id]

    # ✅ Use IP-based identity (CRITICAL FIX)
    ip = socket.gethostbyname(socket.gethostname())
    node_address = f"{ip}:{port}"

    print(f"Resolved IP for Node {node_id}: {ip}", flush=True)

    # ✅ Cluster also uses IPs (CRITICAL FIX)
    cluster = [
        resolve("node1", 8001),
        resolve("node2", 8002),
        resolve("node3", 8003),
        resolve("node4", 8004),
        resolve("node5", 8005),
    ]

    print(f"Starting Node {node_id} at {node_address}", flush=True)
    print(f"Cluster view: {cluster}", flush=True)

    # ✅ Register node
    await raftos.register(node_address, cluster=cluster)

    last_leader = None

    while True:
        leader = raftos.get_leader()

        if leader != last_leader:
            print(f"[Node {node_id}] Leader changed: {leader}", flush=True)
            last_leader = leader

        if leader == node_address:
            print(f"[LEADER Node {node_id}] I am the leader", flush=True)

        elif leader is None:
            print(f"[Node {node_id}] Waiting for leader election...", flush=True)

        else:
            print(f"[FOLLOWER Node {node_id}] Current leader: {leader}", flush=True)

        await asyncio.sleep(5)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python node.py <node_id>")
        sys.exit(1)

    node_id = int(sys.argv[1])

    logging.basicConfig(level=logging.INFO)

    asyncio.run(main(node_id))