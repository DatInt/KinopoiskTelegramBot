from database.database import User, Movies


def create_tables():
	User.create_table()
	Movies.create_table()


def category_search(category, user_id):
	query = Movies.select().where(Movies.category == category, Movies.user == user_id)
	return query

def delete_history(callback_user_id):
	query = Movies.select().where(Movies.user == callback_user_id)
	return query

