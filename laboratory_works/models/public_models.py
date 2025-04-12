from typing import Optional
from default_models import ProfileDefault, BookDefault, ShareRequestDefault

class ProfilePublic(ProfileDefault):
    id: int
    books: Optional[list[BookDefault]] = []
    sent_requests: Optional[list[ShareRequestDefault]] = []
    received_requests: Optional[list[ShareRequestDefault]] = []

class BookPublic(BookDefault):
    id: int
    owner: ProfileDefault | None = None
