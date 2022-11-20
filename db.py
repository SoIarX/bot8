import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

class Database:

    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.c = self.conn.cursor()

    def exists_user(self, user_id):
        """Проверка существования пользователя в БД"""
        return bool(self.c.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone())
        
    def add_user(self, user_id, referrer_id=None):
      if referrer_id != None:
        self.c.execute("INSERT INTO users ('user_id', 'referrer_id') VALUES(?, ?)", (user_id, referrer_id,))
        self.conn.commit()
      else:
        self.c.execute("INSERT INTO users ('user_id') VALUES(?)", (user_id,))
        self.conn.commit()
        
    def count_referals(self, user_id):
      self.c.execute("SELECT COUNT('id') as count FROM users WHERE referrer_id=?", (user_id,)).fetchone()[0]
      
    def check_balance(self, user_id):
      self.c.execute("SELECT balance FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
      
    def set_active(self, user_id, active):
      with self.conn:
          return self.c.execute("UPDATE users SET active=? WHERE user_id=?", (active, user_id))
          self.conn.commit()
      
    def get_users(self):
      with self.conn:
          return self.c.execute("SELECT user_id, active FROM users").fetchall()
          
    def adm_or_no(self, user_id):
      with self.conn:
        return self.c.execute("SELECT admin FROM users WHERE user_id = ?", (user_id,)).fetchall()[0][0]

    def giveadm(self, admin, user_id):
      with self.conn:
        return self.c.execute("UPDATE users SET admin = ? WHERE user_id = ?", (admin, user_id,))
        self.conn.commit()
        
    def checkban(self, user_id):
      with self.conn:
        return self.c.execute("SELECT block FROM users WHERE user_id = ?", (user_id,)).fetchall()[0][0]
        
    def ban(self, user_id):
      self.c.execute("UPDATE users SET block = 1 WHERE user_id = ?", (user_id,))
      self.conn.commit()
      
    def unban(self, user_id):
      self.c.execute("UPDATE users SET block = 0 WHERE user_id = ?", (user_id,))
      self.conn.commit()
      
    def setb(self, balance, user_id):
      self.c.execute("UPDATE users SET balance = ? WHERE user_id = ?", (balance, user_id,))
      self.conn.commit()
