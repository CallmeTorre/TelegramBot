import sqlite3

class DBHelper:
	def __init__(self,dbname="todo.sqlite"):
		"""Takes a database name (by default store our data in a file called todo.sqlite) and creates a database connection."""
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname)

	def setup(self):
		"""Creates a new table called items in the database. This table has one column (called description)"""
		stmt = "CREATE TABLE IF NOT EXISTS items (description text)"
		self.conn.execute(stmt)
		self.conn.commit()
	
	def add_item(self, item_text):
		"""Takes the text for the item and inserts it into the database table."""
		stmt = "INSERT INTO items (description) VALUES (?)"
		args = (item_text, )
		self.conn.execute(stmt, args)
		self.conn.commit()

	def delete_item(self, item_text):
		"""Takes the text for an item and removes it from the database"""
		stmt = "DELETE FROM items WHERE description = (?)"
		args = (item_text, )
		self.conn.execute(stmt, args)
		self.conn.commit()

	def get_items(self):
		"""Returns a list of all the items in the database"""
		stmt = "SELECT description FROM items"
		return [x[0] for x in self.conn.execute(stmt)]
