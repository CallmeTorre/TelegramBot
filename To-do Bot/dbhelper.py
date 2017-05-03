import sqlite3

class DBHelper:
	def __init__(self,dbname="todo.sqlite"):
		"""Takes a database name (by default store our data in a file called todo.sqlite) and creates a database connection."""
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname)

	def setup(self):
		"""Creates a new table called items in the database. This table has one column (called description)"""
		tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
		itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
		ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
		self.conn.execute(tblstmt)
		self.conn.execute(itemidx)
		self.conn.execute(ownidx)
		self.conn.commit()

	def add_item(self, item_text, owner):
		"""Takes the text for the item and inserts it into the database table."""
		stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
		args = (item_text, owner)
		self.conn.execute(stmt, args)
		self.conn.commit()

	def delete_item(self, item_text, owner):
		"""Takes the text for an item and removes it from the database"""
		stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
		args = (item_text, owner)
		self.conn.execute(stmt, args)
		self.conn.commit()

	def get_items(self, owner):
		"""Returns a list of all the items in the database"""
		stmt = "SELECT description FROM items WHERE owner = (?)"
		args = (owner, )
		return [x[0] for x in self.conn.execute(stmt, args)]
