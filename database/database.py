from peewee import SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField

db = SqliteDatabase("database.db")


class User(Model):
	user_id = IntegerField()
	username = CharField()
	link = CharField()
	movie_name = CharField()
	year = IntegerField()

	class Meta:
		database = db


User.create_table()
