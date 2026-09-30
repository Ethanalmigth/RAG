import uuid

from sqlalchemy import String, Uuid, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.engine import  Base
from app.enums.statusDocument import StatusDocument
from app.enums.type import TypeEnum


class Documents(Base):
    __tablename__ = 'document'
    id:Mapped[uuid.UUID] = mapped_column(Uuid,primary_key=True,default=uuid.uuid4)
    filename:Mapped[str] = mapped_column(String,nullable=False)
    url:Mapped[str] = mapped_column(String,nullable=False)
    type:Mapped[TypeEnum] = mapped_column(Enum(TypeEnum),nullable=False)
    status:Mapped[StatusDocument] = mapped_column(Enum(StatusDocument),nullable=False,default=StatusDocument.UPLOAD)
    error:Mapped[str] = mapped_column(String,nullable=True)