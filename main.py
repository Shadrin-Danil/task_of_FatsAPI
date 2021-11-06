from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData, Table, Column,\
    String, Integer, select, update
from sqlalchemy.orm import session
from task_add import Info


# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, connect

# Создание БД
# connection = psycopg2.connect(user="postgres", password="Aaa-slosno")
# connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#
# cursor = connection.cursor()
# sql_create_database = cursor.execute('CREATE DATABASE tasks')
#
# cursor.close()
# connection.close()

app = FastAPI()

metadata = MetaData()

# Подключение и соединение с БД
engine = create_engine("postgresql+psycopg2://postgres:Aaa-slosno@localhost/tasks")
engine.connect()
print(engine)

engine.autocommit = True

if engine:
    print("Подключение к БД прошло успешно")

# Создание таблицы
table = Table('blog', metadata,
              Column("sid", Integer, primary_key=True),
              Column("tusk_uuid", String(50), nullable=False),
              Column("description", String(50), nullable=False),
              Column("param_1", String(50), nullable=False),
              Column("param_2", Integer, nullable=False))

# metadata.create_all(engine)


@app.get("/")
def home():
    print("> Переход на Домашняя страница")
    return {"Massage": "Hello, world"}


@app.get("/task/")
def task():
    connect = engine.connect()
    s = select([table])
    record = connect.execute(s)
    print("> Переход на /task/")
    return record.fetchall()


@app.post("/task/add/")
def task_add(info: Info):
    ins = table.insert().values(
        tusk_uuid=info.get_uuid(),
        description=info.get_des(),
        param_1=info.get_par_1(),
        param_2=info.get_par_2()
    )
    con = engine.connect()
    record = con.execute(ins)
    print("> Переход на /task/add/")
    return info


@app.put("/task/<task_sid>")
def task_sid(task_sid: int, info: Info):
    upd = update(table).where(table.c.sid == task_sid).values(
        tusk_uuid=info.get_uuid(),
        description=info.get_des(),
        param_1=info.get_par_1(),
        param_2=info.get_par_2()
    )
    con = engine.connect()

    s = table.select().where(table.c.sid == task_sid)
    s_con = con.engine.connect()
    s_record = s_con.execute(s)

    results = s_record.fetchone()

    print("< Переход на task/<task_sid>/")
    return {"Данные обновлены": results}
