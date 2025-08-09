#--------------------
# async udp messages
# di Michele Danilo Pierri
# 08/08/2025
#--------------------

import asyncio
import time
import matplotlib.pyplot as plt

REPEAT = 1000
HOST = '127.0.0.1'
PORT = 6000
MESSAGE = b"Async UDP message"
async_durations = []

class EchoServerProtocol(asyncio.DatagramProtocol):
    def datagram_received(self, data, addr):
        pass  # No response needed

async def run_async_server():
    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(), local_addr=(HOST, PORT))
    await asyncio.sleep(2)  # Wait for messages
    transport.close()

async def run_async_client():
    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(
        lambda: asyncio.DatagramProtocol(), remote_addr=(HOST, PORT))
    for _ in range(REPEAT):
        start = time.time()
        transport.sendto(MESSAGE)
        async_durations.append(time.time() - start)
        await asyncio.sleep(0.01)
    transport.close()

async def main_async():
    server = asyncio.create_task(run_async_server())
    await asyncio.sleep(0.5)
    await run_async_client()
    await server

asyncio.run(main_async())

plt.plot(async_durations, label="Async UDP")
plt.title("Async UDP Transmission Times")
plt.xlabel("Message Index")
plt.ylabel("Duration (s)")
plt.grid(True)
plt.legend()
plt.show()
