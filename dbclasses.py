from peewee import (
    Model,
    IntegerField,
    CharField,
    SqliteDatabase,
    ForeignKeyField,
    TextField,
)

# Пользователи
class users(Model):
    user_id = IntegerField(primary_key=True, unique=True)
    name = CharField(unique=True)
    password = CharField()
    last_session_id = CharField()

    class Meta:
        database = SqliteDatabase("users.db")


# Список задач
# M to 1
class todos(Model):
    todo_id = IntegerField(primary_key=True, unique=True)
    user_id = ForeignKeyField(model=users)
    text = TextField()

    class Meta:
        database = SqliteDatabase("todos.db")
