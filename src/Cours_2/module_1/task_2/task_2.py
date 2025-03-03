import datetime
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

import redis

r = redis.StrictRedis(host="localhost", port=6379, db=0)


def timeout_handler():
    raise TimeoutError("Превышен лимит времени.")


def single(max_processing_time: datetime.timedelta):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            lock_key = func.__name__
            lock_uuid = str(uuid.uuid4())
            lock_acquired = r.setnx(lock_key, lock_uuid)

            if not lock_acquired:
                current_lock = r.get(lock_key)
                if current_lock:
                    print(f"Функция '{lock_key}' уже запущена")
                    return

            r.expire(lock_key, int(max_processing_time.total_seconds()))
            timer = threading.Timer(
                max_processing_time.total_seconds(), timeout_handler
            )
            timer.start()
            try:
                result = func(*args, **kwargs)
                return result
            except TimeoutError as e:
                print(f"Ошибка: {e}")
                return None
            finally:
                timer.cancel()
                r.delete(lock_key)

        return wrapper

    return decorator


@single(max_processing_time=datetime.timedelta(seconds=5))
def process_transaction(thread_name):
    print(f"{thread_name} - поток: Обработка...")
    time.sleep(4)


@single(max_processing_time=datetime.timedelta(seconds=5))
def long_running_task(thread_name):
    print(f"{thread_name} - поток: Обработка...")
    time.sleep(7)


if __name__ == "__main__":
    worker_ids = range(1, 6)
    with ThreadPoolExecutor(max_workers=5) as executor:
        results1 = list(executor.map(process_transaction, worker_ids))

    with ThreadPoolExecutor(max_workers=5) as executor:
        results2 = list(executor.map(long_running_task, worker_ids))
