from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import text


created_at = Annotated[
    datetime,
    mapped_column(server_default=text("TIMEZONE('utc', now())"))
]

updated_at = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow
    )]