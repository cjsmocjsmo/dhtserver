import asyncio
import websockets
import json
import subprocess
import logging
import os

logging.basicConfig(level=logging.INFO)

# async def handle_message(websocket, path):
async def handle_message(websocket):
    try:
        async for message in websocket:
            data = json.loads(message)
            command = data.get("command")

            if command == "tempc":
                temp = subprocess.run(["dht11temp"])
                print("temp type {}", type(temp))
                await websocket.send(json.dumps({"temp": str(temp)}))
            elif command == "tempf":
                temp = subprocess.run(["dht11temp"])
                tempf = (temp * 9/5) + 32
                await websocket.send(json.dumps({"temp": str(tempf)}))
            elif command == "hum":
                hum = subprocess.run(["dht11hum"])
                await websocket.send(json.dumps({"hum": str(hum)}))

    except Exception as e:
        logging.error(f"Exception in handle_message: {e}")
    finally:
        logging.info("WebSocket connection closed")
async def servermain():
    async with websockets.serve(handle_message, "10.0.4.60", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(servermain())