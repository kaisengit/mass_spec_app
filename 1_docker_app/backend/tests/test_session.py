from sqlalchemy.orm import Session

from mass_spec_app.db.session import get_db


def test_get_db():
    """Test the session creation and lifecycle."""
    session = next(get_db())
    assert isinstance(session, Session)
    session.close()
