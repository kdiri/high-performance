"""
   :synopsis: Asyncio initial setup example from
              https://www.roguelynn.com/words/asyncio-initial-setup/
"""

import asyncio
import random
import string
import logging
import attr
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)


@attr.s
class PubSubMessage:
    instance_name = attr.ib()
    messaged_id = attr.ib(repr=False)
    hostname = attr.ib(repr=False, init=False)
    restarted = attr.ib(repr=False, init=False)

    def __attrs_post_init__(self):
        self.hostname = f"{self.instance_name}.exemple.net"


async def publish(queue):
    """
    simulating an external publisher of events
    :param queue:
    :param n:
    :return:
    """
    choices = string.ascii_lowercase + string.digits
    msg_id = str(uuid.uuid4())
    while True:
        host_id = "".join(random.choices(choices, k=4))
        instance_name = f"cattle-{host_id}"
        msg = PubSubMessage(messaged_id=msg_id, instance_name=instance_name)
        asyncio.create_task(queue.put(msg))
        logging.info(f"Published messge: {msg}")
        await asyncio.sleep(random.random())


async def restart_host(msg):
    """
    Restart a given host
    :param msg:
    :return:
    """
    await asyncio.sleep(random.random())
    msg.restarted = True
    logging.info(f"Restarted {msg.hostname}")


async def consume(queue):
    while True:
        msg = await queue.get()
        # process the msg
        logging.info(f"Consumed {msg}")
        asyncio.create_task(restart_host(msg))


def main():
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(publish(queue))
        loop.create_task(consume(queue))
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Process interrupted")
    finally:
        loop.close()
        logging.info("Successfully shutdown the Mayhem service")


if __name__ == "__main__":
    main()
