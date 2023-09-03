from peewee import SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField

db = SqliteDatabase("history.db")


class User(Model):
	user_id = IntegerField(primary_key=True)
	username = CharField()

	class Meta:
		database = db


class Movies(Model):
	user = ForeignKeyField(User, related_name='movies')
	link = CharField()
	movie_name = CharField()
	year = IntegerField()
	category = CharField()

	class Meta:
		database = db


User.create_table()
Movies.create_table()
