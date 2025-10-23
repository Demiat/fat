import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column


class IDMixin:
    """Добавляет кастомное поле id."""

    # as_uuid=True -  хранит идентификатор в базе данных в виде строки,
    # но возвращает его в виде Python-объекта uuid
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
