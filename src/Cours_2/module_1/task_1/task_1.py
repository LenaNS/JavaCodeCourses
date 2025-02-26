import random
import time
from concurrent.futures import ThreadPoolExecutor

from db import Session, Task, create_tasks


def fetch_task(worker_id: int) -> None:
    with Session() as session:
        task = (
            session.query(Task)
            .filter(Task.status == "pending", Task.worker_id.is_(None))
            .with_for_update(skip_locked=True)
            .first()
        )
        while task:
            task.status = "processing"
            task.worker_id = worker_id
            session.commit()
            print(task.status, task.worker_id)
            time.sleep(2)
            task.status = "completed"
            session.commit()
            print(task.status, task.worker_id)
            task = (
                session.query(Task)
                .filter(Task.status == "pending", Task.worker_id.is_(None))
                .with_for_update(skip_locked=True)
                .first()
            )


if __name__ == "__main__":
    create_tasks(random.randint(10, 40))
    worker_ids = range(1, 6)
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(fetch_task, worker_ids))
