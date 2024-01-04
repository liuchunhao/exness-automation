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
            send message to all connected clients when queue is not empty
        '''
        while True:
            if not self.__queue.empty():
                message = self.__queue.get()
                logging.debug(f"Received messages in queue: {message}")
                if type(message) is not str:
                    message = str(message)

                if self.__connected_clients:   
                    logging.debug(f"sending message ... {message}")
                    # await asyncio.wait([client.send(message) for client in self.__connected_clients]) 
                    # send message to all connected clients
                    [await client.send(message) for client in self.__connected_clients]
                    logging.info(f"WebSocket|Sent[{len(self.__connected_clients)}]: {message}")
                else:
                    logging.info(f"WebSocket|No client connected")
            else:
                await asyncio.sleep(0.1)   # check queue every 0.1 second 
        

    async def __server_time(self):
        '''
            send server time to clients every 10 seconds
        '''
        while True:
            res = {
                "eventType": "SERVER_TIME",
                "eventTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "serverTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            self.publish(json.dumps(res, indent=4));
            await asyncio.sleep(30)


    async def __client_handling(self, websocket, path):
        '''
            client connection handling
        '''
        logging.info(f"Client connected from: {websocket.remote_address}")
        client_ip, _ = websocket.remote_address
        self.__connected_clients.add(websocket)
        try: 
            async for message in websocket:
                logging.info(f"Received message from [{client_ip}]: [{message}]")
                await websocket.send(f"Hello! I've received your message from [{client_ip}]: [{message}]")
        except Exception as e:
            logging.error(e)
        finally:
            logging.info(f"Client disconnected")
            self.__connected_clients.remove(websocket)


    async def __start_server(self):
        '''
            no Future task will be completed so that it will run forever
            async with server.serve(self.__client_handling, host=self.host, port=self.port) as websocket:
        '''
        async with server.serve(self.__client_handling, port=self.port) as websocket:
            await asyncio.Future()      


    def publish(self, msg):
        '''
           add message to queue
        '''
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
            logging.info(f"done: {done}")
            return done, pending

        try:
            logging.info(f"server is up at ws://{self.host}:{self.port}")
            asyncio.run(tasks())   # run tasks forever
        except KeyboardInterrupt:
            logging.info(f"server is down at ws://{self.host}:{self.port}")
        except Exception as e:
            logging.error(e)
        finally:
            logging.info(f"server is down at ws://{self.host}:{self.port}")

