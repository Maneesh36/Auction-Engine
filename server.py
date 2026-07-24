import socket
import threading
import json
import time
import ssl

HOST = '0.0.0.0'
PORT = 5000

# Available items (server-controlled)
items = ["laptop", "phone", "watch"]

current_item = {
    "name": "laptop",
    "current_bid": 500,
    "winner": "None",
    "end_time": time.time() + 90,  # 🔥 90 sec now
    "active": True
}

lock = threading.Lock()
clients = []

metrics = {
    "total_bids": 0,
    "accepted_bids": 0,
    "rejected_bids": 0
}

# ---------------- BROADCAST ----------------
def broadcast(msg):
    data = json.dumps(msg).encode()
    for c in clients[:]:
        try:
            c.send(data)
        except:
            clients.remove(c)

# ---------------- ADMIN ----------------
def admin_commands():
    global current_item

    while True:
        try:
            cmd = input()

            if cmd.startswith("set"):
                item = cmd.split()[1]

                if item in items:
                    with lock:
                        current_item = {
                            "name": item,
                            "current_bid": 100,
                            "winner": "None",
                            "end_time": time.time() + 90,
                            "active": True
                        }

                    print(f"[ADMIN] Switched to item: {item}")

                    broadcast({
                        "type": "NEW_ITEM",
                        "item": item,
                        "bid": 100,
                        "remaining": 90
                    })
        except:
            continue

# ---------------- TIMER ----------------
def timer():
    global current_item

    while True:
        time.sleep(1)

        with lock:
            if current_item["active"] and time.time() > current_item["end_time"]:
                current_item["active"] = False

                broadcast({
                    "type": "END",
                    "item": current_item["name"],
                    "winner": current_item["winner"],
                    "bid": current_item["current_bid"],
                    "metrics": metrics
                })

# ---------------- CLIENT ----------------
def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    clients.append(conn)

    # send current item
    conn.send(json.dumps({
        "type": "NEW_ITEM",
        "item": current_item["name"],
        "bid": current_item["current_bid"],
        "remaining": int(current_item["end_time"] - time.time())
    }).encode())

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            msg = json.loads(data)

            if msg["type"] == "BID":
                user = msg["user"]

                try:
                    amount = int(msg["amount"])
                except:
                    continue

                metrics["total_bids"] += 1

                with lock:
                    if not current_item["active"]:
                        conn.send(json.dumps({"type": "REJECT", "msg": "Auction ended"}).encode())
                        continue

                    if amount > current_item["current_bid"]:
                        current_item["current_bid"] = amount
                        current_item["winner"] = user
                        metrics["accepted_bids"] += 1

                        remaining = int(current_item["end_time"] - time.time())

                        broadcast({
                            "type": "UPDATE",
                            "bid": amount,
                            "user": user,
                            "remaining": remaining
                        })
                    else:
                        metrics["rejected_bids"] += 1
                        conn.send(json.dumps({"type": "REJECT", "msg": "Bid too low"}).encode())

        except:
            break

    clients.remove(conn)
    conn.close()

# ---------------- MAIN ----------------
def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    server = context.wrap_socket(server, server_side=True)

    print("[SERVER RUNNING]")
    print("Use: set <item> (laptop/phone/watch)")

    threading.Thread(target=timer, daemon=True).start()
    threading.Thread(target=admin_commands, daemon=True).start()

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()