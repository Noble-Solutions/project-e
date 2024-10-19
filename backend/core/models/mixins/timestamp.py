from datetime import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import mapped_column, Mapped

action_time_at = Annotated[
    datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]


class TimestampMixin:
    created_at: Mapped[action_time_at]
    updated_at: Mapped[action_time_at]
