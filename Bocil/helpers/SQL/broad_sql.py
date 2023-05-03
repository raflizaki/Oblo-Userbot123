from sqlalchemy import Column, String

from Bocil.helpers.SQL import BASE, SESSION

# class set_req
# class get_req


class Blackchat(BASE):
    __tablename__ = "blackchat"
    user_id = Column(String(14), primary_key=True)
    chat_id = Column(String(15))

    def __init__(self, user_id, chat_id):
        self.user_id = user_id
        self.chat_id = chat_id


Blackchat.__table__.create(checkfirst=True)


def get_chat(user_id):
    try:
        return SESSION.query(Blackchat).filter(Blackchat.user_id == str(user_id)).all()
    finally:
        SESSION.close()


def add_chat(user_id, chat_id):
    add = Blackchat(int(user_id), int(chat_id))
    SESSION.add(add)
    SESSION.commit()


def del_chat(user_id, chat_id):
    to_check = SESSION.query(Blackchat).get(str(user_id), int(chat_id))
    if not to_check:
        return False
    rem = SESSION.query(Blackchat).get(str(user_id), int(chat_id))
    SESSION.delete(rem)
    SESSION.commit()
    return True
