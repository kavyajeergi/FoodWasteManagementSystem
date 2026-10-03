import sqllite3

DATABASE_NAME = "food_inventory.db"

def get_db_connection():
    return sqlite3.connect(DATABASE_NAME)

def create_table():
    conn =
