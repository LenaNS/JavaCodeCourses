import json

import redis


class RedisQueue:
    client = redis.StrictRedis(host="localhost", port=6378, db=0)

    def __init__(self, queue_name: str = "default_queue"):
        self.queue_name = queue_name

    def publish(self, msg: dict):
        self.client.lpush(self.queue_name, json.dumps(msg))
        print()

    def consume(self) -> dict:
        msg = self.client.rpop(self.queue_name)
        if msg:
            return json.loads(msg)
        return None


if __name__ == "__main__":
    q = RedisQueue()

    q.publish({"a": 1})
    q.publish({"b": 2})
    q.publish({"c": 3})

    keys = q.client.keys("*")

    # Вывод значений для каждого ключа
    for key in keys:
        value = q.client.get(key)
        print(f"Key: {key} -> Value: {value}")

    assert q.consume() == {"a": 1}
    assert q.consume() == {"b": 2}
    assert q.consume() == {"c": 3}
