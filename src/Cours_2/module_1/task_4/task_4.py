import random
import time

import redis


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    client = redis.StrictRedis(host="localhost", port=6377, db=0)

    def test(self) -> bool:
        current_time = time.time()
        self.client.zremrangebyscore("rate_limit_requests", 0, current_time - 3)
        print(self.client.zcard("rate_limit_requests"))
        if self.client.zcard("rate_limit_requests") > 5:
            return False
        self.client.zadd("rate_limit_requests", {current_time: current_time})
        return True


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        # какая-то бизнес логика
        pass


if __name__ == "__main__":
    rate_limiter = RateLimiter()

    for _ in range(50):
        time.sleep(random.randint(1, 4))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")
