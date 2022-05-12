"""
Tools for ingesting data into a datajoint database.

Model a datajoint schema, tagging properties of the model as needed
"""

from abc import ABC, abstractmethod
import typing
from typing import Dict, Any, Optional

from datajoint_babel.model.table import Table
from datajoint_babel.model.attribute import Dependency
from wehrdj.exceptions import ValidationError

if typing.TYPE_CHECKING:
    from datajoint.user_tables import UserTable
    from datajoint.connection import Connection


class SchemaInterface:
    """
    Metaclass for making interfaces from existing data structures
    to datajoint schema.

    To use:

    * Assign the relevant schema as a ``schema`` class attribute
    * Write code to either assign values from your particular data structure
      as attributes or properties with the same names as the fields in the database
    * Connect and hopefully it will be able to insert your row!

    For an example, see :class:`~wehrdj.ingest.session.Session`
    """

    _fields: Dict[str, Any] = dict()
    """
    The properties and attributes marked as fields to be inserted into the model
    """

    def __init__(self):
        self._table = None

    @property
    @abstractmethod
    def schema(self) -> 'UserTable':
        """
        The schema that this class models.

        (Should be overridden as a class attribute rather than a property,
        this is just how the abc interface works)
        """

    @property
    def name(self) -> str:
        """
        Name of this schema (gotten from the schema's __name__ attr)

        Returns:
            str
        """
        return self.schema.__name__

    @property
    def table(self) -> Table:
        """
        The abstract representation of the datajoint model in the :attr:`~datajoint.Schema.definition`

        eg. for session::

            Table(
              name='Session',
              tier='Manual',
              comment=None,
              keys=[
                Dependency(dependency='Subject'),
                Attribute(
                  name='session_datetime',
                  datatype=DJ_Type(datatype='datetime', args=3, unsigned=False),
                  comment='',
                  default=None
                )
              ],
              attributes=[]
            )


        Returns:
            :class:`~datajoint_babel.model.table.Table`
        """
        if self._table is None:
            self._table = Table.from_definition(name=self.name, definition=self.schema.definition)
        return self._table

    @property
    def field_names(self) -> typing.List[str]:
        """
        List of fields that must be defined for this schema

        Returns:
            list[str] = list of field names
        """
        fields = []
        t_fields = self.table.keys
        if self.table.attributes is not None:
            t_fields.extend(self.table.attributes)

        for field in t_fields:
            if isinstance(field, Dependency):
                fields.extend(field.resolve_keys())
            else:
                fields.append(field.name)

        return fields

    @property
    def field_values(self) -> typing.Dict[str, typing.Any]:
        """
        Values that have been given, either as attrs or properties, for all the
        items in the schema

        Returns:
            dict[str, Any]
        """
        return {
            k:getattr(self, k) for k in self.field_names
        }

    def validate(self) -> bool:
        """
        Validate that all the required fields of this schema have been provided

        Returns:
            bool: ``True`` if they have all been declared
        """
        return all([field in self.__dict__.keys() for field in self.field_names])

    def insert(self, **kwargs):
        """
        Insert this schema entry into the table. You must have already
        called :func:`wehrcj.connect` or else datajoint will prompt you.

        Args:
            **kwargs: passed on to :meth:`~datajoint.user_tables.UserTable.insert`

        Raises:
            :class:`wehrdj.exceptions.ValidationError` if contents failed to validate
        """
        if not self.validate():
            raise ValidationError('Missing required field!')

        self.schema.insert(self.field_values, **kwargs)





