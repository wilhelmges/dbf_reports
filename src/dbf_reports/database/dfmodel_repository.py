from sqlmodel import Session, SQLModel


class DfRowRepository():
    def __init__(self, session: Session, model:type[SQLModel]):
        self.session = session
        self.model = model
    def inc_or_create(self):
        pass