try:
    from Bocil.helpers.SQL import BASE, SESSION
except ImportError:
    raise AttributeError

from sqlalchemy import Column, Integer, String, UnicodeText


class Userbot(BASE):
    __tablename__ = "userbot"
    user_id = Column(String(14), primary_key=True)
    api_id = Column(Integer)
    api_hash = Column(UnicodeText)
    session_string = Column(UnicodeText)

    def __init__(self, user_id, api_id, api_hash, session_string):
        self.user_id = str(user_id)
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_string = session_string


Userbot.__table__.create(checkfirst=True)


class Habisnya(BASE):
    __tablename__ = "habisnya"
    user_id = Column(String(14), primary_key=True)
    habis = Column(UnicodeText)

    def __init__(self, user_id, habis):
        self.user_id = str(user_id)
        self.habis = habis


Habisnya.__table__.create(checkfirst=True)


def add_ubot(user_id, api_id, api_hash, session_string):
    user = SESSION.query(Userbot).get(str(user_id))
    if not user:
        adder = Userbot(str(user_id), int(api_id), api_hash, session_string)
        SESSION.add(adder)
        SESSION.commit()
        return True
    rem = SESSION.query(Userbot).get(str(user_id))
    SESSION.delete(rem)
    SESSION.commit()
    adder = Userbot(str(user_id), int(api_id), api_hash, session_string)
    SESSION.add(adder)
    SESSION.commit()
    return False


def remove_ubot(user_id):
    to_check = SESSION.query(Userbot).get(str(user_id))
    if not to_check:
        return False
    rem = SESSION.query(Userbot).get(str(user_id))
    SESSION.delete(rem)
    SESSION.commit()
    return True


def get_userbots():
    data = []
    ubots = SESSION.query(Userbot)
    for ubot in ubots:
        data.append(
            dict(
                name=ubot.user_id,
                api_id=ubot.api_id,
                api_hash=ubot.api_hash,
                session_string=ubot.session_string,
            )
        )
    SESSION.close()
    return data


def save_habis(user_id, habis):
    user = SESSION.query(Habisnya).get(str(user_id))
    if not user:
        adder = Habisnya(str(user_id), habis)
        SESSION.add(adder)
        SESSION.commit()
        return True
    rem = SESSION.query(Habisnya).get(str(user_id))
    SESSION.delete(rem)
    SESSION.commit()
    adder = Habisnya(str(user_id), habis)
    SESSION.add(adder)
    SESSION.commit()
    return False


def get_habis(user_id):
    try:
        _result = SESSION.query(Habisnya).filter(Habisnya.user_id == str(user_id)).all()
        if _result:
            return _result
        return None
    finally:
        SESSION.close()
