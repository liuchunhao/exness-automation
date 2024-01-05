import asyncio
import logging
import queue
import json
from datetime import datetime
from websockets import server


class WebSocketServer:

    def __init__(self, host='0.0.0.0', port=8765):
        logging.basicConfig(level=logging.INFO)
        self.__connected_clients = set()
        self.__queue = queue.Queue()
        self.host = host
        self.port = port

    async def __queue_handling(self):
        '''
        Send message to all connected clients when queue is not empty
        '''
        while True:
            if not self.__queue.empty():
                message = self.__queue.get()
                logging.debug(f"Received messages in queue: {message}")
                if type(message) is not str:
                    message = str(message)

                if self.__connected_clients:   
                    # await asyncio.wait([client.send(message) for client in self.__connected_clients]) 
                    [await client.send(message) for client in self.__connected_clients]
                    logging.info(f"SND[{len(self.__connected_clients)}]: {message}")
                else:
                    logging.debug(f"No client connected")
            else:
                await asyncio.sleep(0.05)   # check queue every 0.1 second if it is empty
        

    async def __server_time(self):
        '''
        Send server time to clients every 10 seconds
        '''
        while True:
            res = {
                "event": "heartbeat",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data": {}
            }
            self.publish(res);
            await asyncio.sleep(30)


    async def __client_handling(self, websocket, path):
        '''
        Client connection handling
        '''
        logging.info(f"Client connected from: {websocket.remote_address}")
        client_ip, _ = websocket.remote_address
        self.__connected_clients.add(websocket)
        try: 
            async for message in websocket:
                logging.info(f"Received message from [{client_ip}]: [{message}]")
                await websocket.send(f"Hello! I've received your message from [{client_ip}]: [{message}]")
        except Exception as e:
            logging.exception(f"Exception from [{client_ip}]: [{e}]")
        finally:
            logging.info(f"Client disconnected from: {websocket.remote_address}")
            self.__connected_clients.remove(websocket)


    async def __start_server(self):
        '''
            no Future task will be completed so that it will run forever
            async with server.serve(self.__client_handling, host=self.host, port=self.port) as websocket:
        '''
        async with server.serve(self.__client_handling, port=self.port) as websocket:
            await asyncio.Future()      


    def publish(self, msg):
        self.__queue.put(msg)


    def start(self):
        '''
        start server
        '''
        async def tasks():
            '''
            all tasks that you want to run concurrently
            '''
            task_list = [
                asyncio.create_task(self.__start_server(), name='start_server'),
                asyncio.create_task(self.__server_time(),  name='server_time'),
                asyncio.create_task(self.__queue_handling(), name='queue_handling'),
            ]
            done, pending = await asyncio.wait(task_list)
            logging.info(f"Tasks done: {done}")
            return done, pending

        try:
            logging.info(f"Server is up at ws://{self.host}:{self.port}")
            asyncio.run(tasks())   # run tasks forever
        except KeyboardInterrupt:
            logging.info(f"Server is down at ws://{self.host}:{self.port}")
        except Exception as e:
            logging.exception(f"Exception: {e}")
        finally:
            logging.info(f"server is down at ws://{self.host}:{self.port}")


if __name__ == '__main__':
    import time
    import threading
    logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)s|%(message)s')

    ws_server = WebSocketServer(host='0.0.0.0', port=8765)
    threading.Thread(target=ws_server.start).start()
    
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break