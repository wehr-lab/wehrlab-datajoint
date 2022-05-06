"""
Tools for ingesting data into a datajoint database.

Model a datajoint schema, tagging properties of the model as needed
"""

from abc import ABC, abstractmethod
import typing
from typing import Dict, Any, Optional

from datajoint_babel.model.table import Table
from wehrdj.exceptions import ValidationError

if typing.TYPE_CHECKING:
    from datajoint.user_tables import UserTable
    from datajoint.connection import Connection

class SchemaInterface:

    _fields: Dict[str, Any] = dict()
    """
    The properties and attributes marked as fields to be inserted into the model
    """

    @property
    @abstractmethod
    def schema(self) -> 'UserTable':
        """
        The schema that this class models.

        (Can be overridden as a class attribute rather than a property,
        this is just how the abc interface works)
        """

    @property
    def name(self) -> str:
        """
        Name of this schema

        Returns:
            str
        """
        return self.schema.__name__

    @property
    def table(self) -> Table:
        """
        The abstract representation of the datajoint model in the :attr:`~datajoint.Schema.definition`

        Returns:
            :class:`~datajoint_babel.model.table.Table`
        """
        return Table.from_definition(name=self.name, definition=self.schema.definition)


    def validate(self) -> bool:
        """
        Validate that all the required fields of this schema have been provided

        Returns:
            bool: ``True`` if they have
        """

    def insert(self, conn: 'Connection', **kwargs):
        """
        Insert this schema entry into the table

        Args:
            conn (:class:`datajoint.connection.Connection`): Active connection to a database.
            **kwargs: passed on to :meth:`~datajoint.user_tables.UserTable.insert`

        Raises:
            :class:`wehrdj.exceptions.ValidationError` if contents failed to validate
        """
        if not self.validate():
            raise ValidationError('Missing required field!')

        self.schema.insert(self._fields, **kwargs)





