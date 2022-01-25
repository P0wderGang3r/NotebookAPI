from peewee import *

#Пользователи
# 1 : 1
class users(Model):
    user_id = IntegerField(primary_key = True, unique = True)
    name = CharField(unique = True)
    password = CharField(unique = True)
    character_id = IntegerField()

    class Meta:
        database = SqliteDatabase('users.db')

#Персонажи пользователей
# 1 : 1
class characters(Model):
    character_id = IntegerField(primary_key = True, unique = True)
    hp = IntegerField(default = 100)
    stamina = IntegerField(default = 100)
    money = IntegerField(default = 0)
    inventory_id = IntegerField()
    weapon_id = IntegerField()
    global_coords_id = IntegerField()

    class Meta:
        database = SqliteDatabase('characters.db')

#Инвентари пользователей
# M : 1
class inventories(Model):
    inventory_id = IntegerField(primary_key = True)
    item_id = IntegerField()
    amount = IntegerField()

    class Meta:
        database = SqliteDatabase('inventories.db')

#Координаты на глобальной карте
# 1 : 1
class global_coords(Model):
    global_coords_id = IntegerField(primary_key = True, unique = True)
    x = IntegerField()
    y = IntegerField()

    class Meta:
        database = SqliteDatabase('global_coords.db')

# Описания оружий
# 1 : M
class weapons(Model):
    weapon_id = IntegerField(primary_key = True, unique = True)
    dmg = IntegerField()
    desc = TextField()

    class Meta:
        database = SqliteDatabase('weapons.db')

# Описания эффектов
# 1 : M
class item_effects(Model):
    item_effects_id = IntegerField(primary_key = True, unique = True)
    desc = TextField()

    class Meta:
        database = SqliteDatabase('item_effects.db')

# Поля классов по-умолчанию
# 1 : M
class character_default_types(Model):
    type_id = IntegerField(primary_key = True, unique = True)
    weapon_id = IntegerField()
    hp = IntegerField()
    stamina = IntegerField()

    class Meta:
        database = SqliteDatabase('character_default_types.db')
