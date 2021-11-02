import time
import threading
from concurrent.futures import Future


def network_request(number) -> dict:
    time.sleep()
    return {"success": True, "result": number ^ 2}


def fetch_square(number):
    resp = network_request(number)
    if resp["success"]:
        print(f"Result is: {resp['result']}")


def wait_and_print(msg):
    time.sleep(1.0)
    print(msg)


def wait_and_print_async(msg):
    def callback(msg):
        print(msg)

    timer = threading.Timer(1.0, callback, [msg])
    timer.start()


def network_request_async(number, on_done):
    def timer_done(number):
        on_done(
            {
                "success": True,
                "result": number ** 2,
            }
        )

    timer = threading.Timer(1.0, timer_done, [number])
    timer.start()


def on_done(result):
    print(result)


def fetch_square_async(number):
    def on_done(response):
        if response["success"]:
            print(f"Response is {response['result']}")

    network_request_async(number, on_done)


def network_request_async_future(number):
    future = Future()
    result = {"success": True, "result": number ** 2}
    timer = threading.Timer(1.0, lambda: future.set_result(result))
    timer.start()
    return future


def fetch_square_future(number):
    fut = network_request_async_future(number)

    def on_done_future(future):
        response = future.result()
        if response["success"]:
            print(f"Response is {response['result']}")

    fut.add_done_callback(on_done_future)


def process_future():
    """
    Response is 4
    Response is 9
    """
    fetch_square_future(2)
    fetch_square_future(3)


def process():
    """
    Expected print order (depending on interruption at OS level):

    First call
    Second call
    After submission
    After network submission
    First async call
    {'success': True, 'result': 9}
    {'success': True, 'result': 16}
    Second async call
    {'success': True, 'result': 4}

    :return:
    """
    wait_and_print("First call")
    wait_and_print("Second call")
    wait_and_print_async("First async call")
    wait_and_print_async("Second async call")
    print("After submission")
    network_request_async(2, on_done)
    network_request_async(3, on_done)
    network_request_async(4, on_done)
    print("After network submission")


if __name__ == "__main__":
    process_future()
