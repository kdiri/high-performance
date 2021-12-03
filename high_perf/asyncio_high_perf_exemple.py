"""
   :synopsis: Asyncio example from the book
"""
import random
import time
from typing import Generator
import asyncio
from concurrent.futures import ThreadPoolExecutor


executor = ThreadPoolExecutor(max_workers=3)


def wait_and_return(msg: str) -> str:
    time.sleep(1)
    print(msg)


def range_generator(n) -> Generator:
    i = 0
    while i < n:
        print(f"Generating value {i}")
        yield i
        i += 1


def parrot():
    """
    generator = parrot()
    generator.send(None)
    generator.send("Hello")
    generator.send("World")
    :return:
    """
    while True:
        message = yield
        print(f"Parrot says: {message}")


async def hello():
    print("Hello, async !")


async def wait_and_print(msg):
    await asyncio.sleep(3.0)
    print(f"Message: {msg}")


async def network_request(number):
    if number == 2:
        await asyncio.sleep(1)
    await asyncio.sleep(random.random())
    return {"success": True, "result": number ** 2}


async def fetch_square(number):
    res = await network_request(number)
    if res["success"]:
        print(f"Result is {res['result']}")


if __name__ == "__main__":
    """
    loop.run_until_complete(hello())
    loop.run_until_complete(wait_and_print("Hello"))
    
    Running tasks using run_until_complete is fine for testing and debugging. 
    However, our program will be started with loop.run_forever most of the times, 
    and we will need to submit our tasks while the loop is already running.
    """
    loop = asyncio.get_event_loop()
    try:
        fut = loop.run_in_executor(executor, wait_and_return, "hello asyncio executor")
        loop.run_until_complete(fut)
        """
        asyncio provides the ensure_future function, which schedules coroutines 
        (as well as futures) for execution. ensure_future can be used by simply
         passing the coroutine we want to schedule.
        """
        asyncio.ensure_future(fetch_square(2))
        asyncio.ensure_future(fetch_square(3))
        asyncio.ensure_future(fetch_square(4))
        loop.run_forever()
    except KeyboardInterrupt:
        print("Exiting")
    finally:
        loop.close()
