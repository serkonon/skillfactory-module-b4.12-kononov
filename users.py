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
    Запрашивает данные пользователя, ищет в базе по email.
    Если пользователь найден, оновляет его данные, иначе - добавляет нового
    """
    print("Введите данные пользователя:")
    first_name = input("Имя: ")
    last_name = input("Фамилия: ")
    gender = input("Пол (Male/Female): ")
    email = input("Email: ")
    birthdate = input("Дата рождения (ГГГГ-ММ-ДД): ")
    height = input("Рост: (М.СМ): ")

    session = connect_db()

    user = session.query(User).filter(User.email == email).first()

    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.gender = gender
        user.birthdate = birthdate
        user.height = height
        session.commit()
        print("Данные пользователя обновлены!")
    else:
        user = User(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            email=email,
            birthdate=birthdate,
            height=float(height)
        )
        session.add(user)
        session.commit()
        print("Данные пользователя добавлены!")

if __name__ == "__main__":
    main()

