from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from config import settings
from core.utils.camel_case import camel_case_to_snake_case


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей в приложении
    """

    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Generate the table name for the given class.

        This function is a directive declared attribute that is used to automatically generate the table name for a SQLAlchemy model. It takes a class as input and returns a string representing the table name.

        Parameters:
            cls (type): The class for which the table name is being generated.

        Returns:
            str: The table name generated based on the class name.

        Example:
            >>> class User(Base):
            >>>     pass
            >>> User.__tablename__()
            'users'
        """
        return f"{camel_case_to_snake_case(cls.__name__)}s"
