import socket
import threading
import json
import ssl
import tkinter as tk
from tkinter import scrolledtext

client = None
username = None
connected = False

# ---------- RECEIVE ----------
def receive(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break

            msg = json.loads(data)

            if msg["type"] == "NEW_ITEM":
                display(f"🔥 {msg['item']} | Start: ${msg['bid']} | Time: {msg['remaining']}s")

            elif msg["type"] == "UPDATE":
                display(f"💰 ${msg['bid']} by {msg['user']} | Time: {msg['remaining']}s")

            elif msg["type"] == "REJECT":
                display(f"❌ {msg['msg']}")

            elif msg["type"] == "END":
                display(f"🏆 Winner: {msg['winner']} | ${msg['bid']}")
                display(f"📊 {msg['metrics']}")

            elif msg["type"] == "WAIT":
                display(f"⏳ {msg['msg']}")

        except:
            break

# ---------- CONNECT ----------
def connect_to_server():
    global client, username, connected

    username = username_entry.get().strip()

    if not username:
        display("❌ Enter username")
        return

    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        raw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client = context.wrap_socket(raw, server_hostname='localhost')

        client.connect(('10.48.222.201', 5000))  # 🔥 replace

        connected = True
        display(f"✅ Connected as {username}")

        connect_btn.config(state=tk.DISABLED)

        threading.Thread(target=receive, args=(client,), daemon=True).start()

    except Exception as e:
        display(f"❌ Connection failed: {e}")

# ---------- SEND BID ----------
def send_bid():
    if not connected:
        display("❌ Not connected")
        return

    bid = entry.get().strip()

    if not bid.isdigit():
        display("❌ Enter valid number")
        return

    msg = {"type": "BID", "amount": bid, "user": username}
    client.send(json.dumps(msg).encode())

    entry.delete(0, tk.END)

# ---------- DISPLAY ----------
def display(text):
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, text + "\n")
    text_area.config(state=tk.DISABLED)
    text_area.see(tk.END)

# ---------- UI ----------
root = tk.Tk()
root.title("🔥 Auction Client")
root.geometry("500x520")
root.configure(bg="#1e1e2f")

# Title
title = tk.Label(root, text="Real-Time Auction", font=("Arial", 16, "bold"),
                 bg="#1e1e2f", fg="white")
title.pack(pady=10)

# Output area
text_area = scrolledtext.ScrolledText(
    root, width=55, height=18,
    bg="#2b2b3c", fg="#00ffcc", font=("Consolas", 10)
)
text_area.pack(pady=10)
text_area.config(state=tk.DISABLED)

# Username input
username_entry = tk.Entry(root, width=30, font=("Arial", 11))
username_entry.pack(pady=5)

# Connect button
connect_btn = tk.Button(
    root, text="Connect", command=connect_to_server,
    bg="#4CAF50", fg="white", width=15
)
connect_btn.pack(pady=5)

# Bid input
entry = tk.Entry(root, width=30, font=("Arial", 11))
entry.pack(pady=5)

# Bid button
btn = tk.Button(
    root, text="Place Bid", command=send_bid,
    bg="#2196F3", fg="white", width=15
)
btn.pack(pady=10)

root.mainloop()