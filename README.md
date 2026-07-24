# Secure Real-Time Auction Engine

## Overview

This project is a secure client-server auction system developed in Python. It allows multiple clients to participate in real-time bidding over encrypted SSL/TLS connections. The server manages auction items, validates bids, broadcasts updates to all connected clients, and maintains auction statistics.

## Features

- Secure communication using SSL/TLS
- Multi-threaded server supporting multiple clients
- Real-time bid updates
- Multiple auction items
- Admin-controlled auction switching
- GUI-based client using Tkinter
- Automatic SSL certificate generation
- Auction statistics

## Technologies Used

- Python 3
- Socket Programming
- SSL/TLS
- Threading
- JSON
- Tkinter
- Cryptography

## Project Structure

```
Auction-Engine/
│── client.py
│── server.py
│── generate_cert.py
│── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Maneesh36/Auction-Engine.git
cd Auction-Engine
```

Install the required package:

```bash
pip install cryptography
```

## Running the Project

### Step 1: Generate SSL Certificates

```bash
python generate_cert.py
```

This creates the required `cert.pem` and `key.pem` files.

### Step 2: Start the Server

```bash
python server.py
```

### Step 3: Start the Client

```bash
python client.py
```

Enter a username and start placing bids.

## System Architecture

```
Client 1  ----\
               \
Client 2  ------>  Server
               /
Client 3  ----/
```

All communication between clients and the server is secured using SSL/TLS.

## Application Screenshot

<img src="Auction.png" alt="Auction GUI" width="800"/>

## Future Improvements

- User authentication
- Database integration
- Persistent auction history
- Web-based interface
- Real-time analytics dashboard
- Multiple auction rooms

## Author

Maneesh

B.Tech Artificial Intelligence & Machine Learning

PES University
