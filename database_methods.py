import hashlib
import hashlib
import uuid
import datetime as dt
import mysql.connector

class DatabaseConnector():

    def __init__(self, *, username, userpassword, hostname, databasename):
        self.connector = mysql.connector.connect(user=username,
                                    password=userpassword,
                                    host=hostname,
                                    database=databasename)

    def get_hashed_password(self, password):
        """
        >>> DatabaseConnector(username='vitali', userpassword= '1', hostname='localhost', databasename= 'chat').get_hashed_password("pip")
        '612a6832e385695721e4'
        >>> DatabaseConnector(username='vitali', userpassword= '1', hostname='localhost', databasename= 'chat').get_hashed_password("mice")
        'f57eabe484a190852587'
        >>> DatabaseConnector(username='vitali', userpassword= '1', hostname='localhost', databasename= 'chat').get_hashed_password("owl")
        '58605353ca2a56d0ddbd'
        >>> DatabaseConnector(username='vitali', userpassword= '1', hostname='localhost', databasename= 'chat').get_hashed_password("puppy")
        'a750504eb2d68869c750'
        >>> DatabaseConnector(username='vitali', userpassword= '1', hostname='localhost', databasename= 'chat').get_hashed_password("rat")
        '7b66a7e952dcc7e936dc'
        >>> DatabaseConnector(username='vitali', userpassword= '1', hostname='localhost', databasename= 'chat').get_hashed_password("rafic")
        '9c9771af941ba160af32'

        """
        return str(hashlib.sha512(password.encode('utf-8')).hexdigest())[:20]

    def check_password(self, hashed_password, user_password):
        return hashed_password == str(hashlib.sha512(user_password.encode('utf-8')).hexdigest())[:20]

    def save_post(self, author, text):
        try:
            cursor = self.connector.cursor()
            sql_stmt = "INSERT INTO post (AUTHOR, TEXT, CREATED_AT)  VALUES (%s, %s, %s)"
            cursor.execute(sql_stmt, (author.strip(), text.strip(), dt.datetime.now()))
            self.connector.commit()
            return True
        except:
            return False

    def tail_posts(self):
        try:
            cursor = self.connector.cursor()
            sql_stmt = "SELECT CREATED_AT, AUTHOR, TEXT  from post ORDER BY CREATED_AT DESC LIMIT 10"
            cursor.execute(sql_stmt)
            posts = cursor.fetchall()
            return posts
        except:
            return False

    def check_user(self, name, password):
        cursor = self.connector.cursor()
        sql_stmt = "SELECT *  FROM  chat_user WHERE name=%s"
        cursor.execute(sql_stmt, (name,))
        row = cursor.fetchone()
        if row:
            name, hashed_password = row
            return self.check_password(hashed_password, password)
        return False

    def create_user(self, name, password):
        if self.is_username_used(name):
            return False
        try:
            cursor = self.connector.cursor()
            sql_stmt = "INSERT INTO chat_user (NAME, PASSWORD)  VALUES (%s, %s)"
            cursor.execute(sql_stmt, (name, self.get_hashed_password(password)))
            self.connector.commit()
        except:
            return False
        return True

    def is_username_used(self, name):
        cursor = self.connector.cursor()
        sql_stmt = "SELECT *  FROM  chat_user WHERE name=%s"
        cursor.execute(sql_stmt, (name,))
        row = cursor.fetchone()
        return True if row or name == 'GUEST' else False

if __name__ == "__main__":
    import doctest
    doctest.testmod()