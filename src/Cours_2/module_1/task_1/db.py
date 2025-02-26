from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, sessionmaker
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    worker_id: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )


engine = create_engine("postgresql://admin:admin@localhost/dbTask1")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def create_tasks(n: int) -> None:
    for i in range(n):
        new_task = Task(task_name="Задача", status="pending")
        session.add(new_task)
        session.commit()
