from src.data_base.session_manager import Base
from sqlalchemy.orm import Mapped, mapped_column
from src.utils import fields


class Collection(Base):
    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    photo: Mapped[str] = mapped_column(nullable=True)

    created_at: Mapped[fields.created_at]
    updated_at: Mapped[fields.updated_at]

