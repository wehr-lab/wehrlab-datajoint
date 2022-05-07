"""
Methods to fill the ``Session`` schema from ``element_schema``.

Two examples are given: a functional example and an object-oriented example.

The object-oriented example makes use of :mod:`wehrdj.interface.interface`, which seems
like a better way to do it to me than having a zillion disconnected functions.
"""

import re
from pathlib import Path
from datetime import datetime
from typing import List, TypedDict
from wehrdj.interface import SchemaInterface
from element_session.session import Session as Session_

# extract dates and ids from strings with pattern
# 2018-06-07_16-26-19_mouse-8580
SESSION_PATTERN = re.compile(r'(\d{4}-[\-_0-9]*)_mouse-(\d*)')

# --------------------------------------------------
# Session extraction -- functional example
# --------------------------------------------------

# container of individual session entries
class SessionDict(TypedDict):
    subject: str
    session_datetime: datetime

def extract_session(
        path:Path,
        pattern:re.Pattern=SESSION_PATTERN
    ) -> SessionDict:
    """
    Extract session metadata from filenames

    Args:
        path (:class:`pathlib.Path`): Directory of session data
        pattern (:class:`re.Pattern`):  Regular Expression pattern that parses datetime and subject from path names

    Returns:
        :class:`.SessionDict`
    """
    p = str(path)
    session = pattern.findall(p)

    # convert date string to datetime
    session_dt = datetime.strptime(
        session[0][0],
        '%Y-%m-%d_%H-%M-%S')

    return SessionDict(
        subject=session[0][1],
        session_datetime=session_dt
    )

def extract_sessions(
        basedir:Path, 
        pattern:re.Pattern=SESSION_PATTERN
    ) -> List[SessionDict]:
    """
    Extract many session metadata with :func:`.extract_session`

    Args:
        basedir (:class:`pathlib.Path`): Direcctory of session directories
        pattern (:class:`re.Pattern`): Regular Expression pattern that parses datetime and subject from path names

    Returns:
        List[:class:`.SessionDict`]
    """

    sessions = []
    for p in basedir.glob('*'):
        session = extract_session(p, pattern)
        if session:
            sessions.append(session)

    return sessions

# --------------------------------------------------
# session example -- object example
# --------------------------------------------------

class Session(SchemaInterface):
    schema = Session_

    def __init__(self, path:Path, pattern=SESSION_PATTERN):
        """
        Use :func:`.extract_session` to populate attributes to be inserted
        into the datajoint database.

        See :class:`~wehrdj.interface.interface.SchemaInterface` for details of intended
        usage.

        Args:
            path (:class:`pathlib.Path`): Directory of session data
            pattern (:class:`re.Pattern`):  Regular Expression pattern that parses datetime and subject from path names

        """
        super(Session, self).__init__()

        self.path = Path(path)
        self.pattern = pattern

        sessdict = extract_session(self.path, self.pattern)
        self.subject = sessdict['subject']
        self.session_datetime = sessdict['session_datetime']




