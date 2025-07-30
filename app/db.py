import sqlite3


class DB:
    def __init__(self, db_name: str) -> None:
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS notes(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT)")

    def create_note(self, title: str, description: str):
        self.cur.execute("INSERT INTO notes (title, description) VALUES(?, ?)", (title, description))
        self.con.commit()

    def get_note(self, id: str):
        query = "SELECT id, title, description FROM notes WHERE id = ?"
        self.cur.execute(query, (id))
        note = self.cur.fetchone()
        return note
    
    def get_all_notes(self):
        query = "SELECT * FROM notes"
        self.cur.execute(query)
        notes = self.cur.fetchall()
        return notes
