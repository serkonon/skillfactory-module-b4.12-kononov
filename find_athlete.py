# Импортируем библиотеку sqlalchemy и некоторые функции из нее
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    """
    Описывает структуру таблицы user
    """
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)


class Athelete(Base):
    """
    Описывает структуру таблицы athelete
    """
    __tablename__ = 'athelete'

    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы,
    если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def main():
    """
    Запрашивает id пользователя, если пользователь найден подбирает по базе 2х спортсменов:
     - ближайшего по дате рождения
     - ближайшего по росту
    Если пользователь не найден - сообщение
    """
    user_id = input("Введите id пользователя: ")

    session = connect_db()

    user = session.query(User).filter(User.id == user_id).first()
    if user:
        toInt = lambda val: int(str(val).replace("-", ""))

        athl_bd = min(session.query(Athelete).all(),
                     key=lambda athl: abs(toInt(athl.birthdate) - toInt(user.birthdate)))

        athl_h = min(session.query(Athelete).all(),
                     key=lambda athl: user.height if athl.height is None else
                     abs(athl.height - user.height))

        print("Ближайшие спортсмены к {} {}, {}, рост {}:".
              format(user.first_name, user.last_name, user.birthdate, user.height))
        print(" - по дате рождения: {}, {} (id={})".
              format(athl_bd.name, athl_bd.birthdate, athl_bd.id))
        print(" - по росту: {}, {} (id={})".
              format(athl_h.name, athl_h.height, athl_h.id))

    else:
        print("Пользователя с таким id нет")

if __name__ == "__main__":
    main()
