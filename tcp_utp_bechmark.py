#--------------------
# tcp vs udp
# di Michele Danilo Pierri
# 08/08/2025
#--------------------


"""
What this measures (no synthetic delays, no made-up data):
  - UDP: one datagram (request) -> echo (response) per transaction.
  - TCP: connect -> send -> recv -> close per transaction.
Why this is fair and didactic:
  - Many real apps perform short, sporadic exchanges. In those cases, UDP avoids the TCP handshake.
  - We DO NOT add fake jitter/latency; measurements are "as is".
Tip: Run once on localhost, then between two machines on the same LAN:
     python demo.py --host <server_ip_on_lan>
"""

import argparse
import socket
import threading
import time
from time import perf_counter
import statistics as stats
import matplotlib.pyplot as plt

# ---------------------------
# Defaults (tuneable via CLI)
# ---------------------------
DEFAULT_HOST = "127.0.0.1"
TCP_PORT = 57211
UDP_PORT = 57212

# Small payload accentuates handshake cost for TCP
DEFAULT_PAYLOAD = 32       # bytes
REPEAT = 400               # transactions per protocol
PACE = 0.001               # seconds between transactions to avoid bursts
TIMEOUT = 2.0              # seconds socket timeout

# ---------------------------
# Servers
# ---------------------------

def tcp_transaction_server(host: str, port: int):
    """
    Accepts connections in a loop.
    For each connection:
      - read exactly one payload (client sends once)
      - echo it back
      - close
    No artificial sleep; this stays 'real'.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(128)
        while True:
            conn, _ = s.accept()
            try:
                with conn:
                    # Read exactly one message; size unknown to server,
                    # so read once up to some reasonable amount
                    data = conn.recv(65536)
                    if data:
                        conn.sendall(data)
            except ConnectionError:
                continue


def udp_echo_server(host: str, port: int):
    """
    Stateless echo: for each datagram, send it back to sender.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        while True:
            data, addr = s.recvfrom(65536)
            if data:
                s.sendto(data, addr)

# ---------------------------
# Clients / Measurements
# ---------------------------

def measure_udp_transactions(host: str, port: int, payload: bytes, n: int):
    """
    For each transaction:
      - send one datagram
      - wait for echo
      - record transaction time (application-level RTT)
    """
    durations = []
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as c:
        c.settimeout(TIMEOUT)
        for _ in range(n):
            t0 = perf_counter()
            c.sendto(payload, (host, port))
            data, _ = c.recvfrom(65536)
            dt = perf_counter() - t0
            durations.append(dt)
            time.sleep(PACE)
    return durations


def measure_tcp_transactions(host: str, port: int, payload: bytes, n: int):
    """
    For each transaction:
      - connect()
      - send payload once
      - recv echo once
      - close
      - record full transaction time (includes handshake)
    """
    durations = []
    for _ in range(n):
        t0 = perf_counter()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.settimeout(TIMEOUT)
            # Optionally disable Nagle to avoid tiny writes coalescing
            c.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            c.connect((host, port))
            c.sendall(payload)
            # Expect a single echo; read once is typically enough on localhost/LAN
            data = c.recv(65536)
            # Close via context manager
        dt = perf_counter() - t0
        durations.append(dt)
        time.sleep(PACE)
    return durations

# ---------------------------
# Plot helpers
# ---------------------------

def summarize(name, arr):
    mean = stats.mean(arr)
    med = stats.median(arr)
    stdev = stats.pstdev(arr)
    return f"{name}: mean={mean:.6e}s, median={med:.6e}s, std={stdev:.6e}s, n={len(arr)}"

def plot_results(tcp, udp, payload_size):
    # 1) Boxplot for robust comparison
    plt.figure(figsize=(9,5))
    plt.boxplot([tcp, udp], labels=["TCP per-tx (handshake)", "UDP per-tx"])
    plt.title(f"Per-Transaction RTT (echo), payload={payload_size} bytes")
    plt.ylabel("Seconds")
    plt.tight_layout()

    # 2) Bar plot mean ± std
    plt.figure(figsize=(9,5))
    means = [stats.mean(tcp), stats.mean(udp)]
    stds  = [stats.pstdev(tcp), stats.pstdev(udp)]
    plt.bar(["TCP per-tx", "UDP per-tx"], means, yerr=stds)
    plt.title("Per-Transaction Mean ± Std")
    plt.ylabel("Seconds")
    plt.tight_layout()
    plt.show()

# ---------------------------
# Main
# ---------------------------

def main():
    ap = argparse.ArgumentParser(description="Real UDP vs TCP per-transaction benchmark")
    ap.add_argument("--host", default=DEFAULT_HOST, help="Server bind/target host (use LAN IP for cross-machine test)")
    ap.add_argument("--payload", type=int, default=DEFAULT_PAYLOAD, help="Payload size in bytes (default: 32)")
    ap.add_argument("--repeat", type=int, default=REPEAT, help="Transactions per protocol (default: 400)")
    args = ap.parse_args()

    host = args.host
    payload = b"A" * args.payload
    repeat = args.repeat

    # Start servers as daemons
    t_tcp = threading.Thread(target=tcp_transaction_server, args=(host, TCP_PORT), daemon=True)
    t_udp = threading.Thread(target=udp_echo_server,         args=(host, UDP_PORT), daemon=True)
    t_tcp.start()
    t_udp.start()
    time.sleep(0.3)  # give servers time to bind

    # Measure
    tcp_times = measure_tcp_transactions(host, TCP_PORT, payload, repeat)
    udp_times = measure_udp_transactions(host, UDP_PORT, payload, repeat)

    # Print summaries
    print(summarize("TCP per-transaction", tcp_times))
    print(summarize("UDP per-transaction", udp_times))

    # Plot
    plot_results(tcp_times, udp_times, len(payload))

if __name__ == "__main__":
    main()
