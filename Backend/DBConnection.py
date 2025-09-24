import mysql.connector
import pymysql


class Database:

    def __init__(self):

        # conn = pymysql.connect(
        #     host="localhost",
        #     user="yourusername",
        #     password="yourpassword",
        #     database="yourdbname"
        # )

        # self.cnx = mysql.connector.connect(host="localhost",user="root",password="root",database="violence_detection")
        self.cnx = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="violence_detection",
            cursorclass=pymysql.cursors.DictCursor
        )

        self.cur = self.cnx.cursor()
        # self.cur = self.cnx.cursor(dictionary=True)


    def select(self, q):
        self.cur.execute(q)
        return self.cur.fetchall()

    def selectOne(self, q):
        self.cur.execute(q)
        return self.cur.fetchone()


    def insert(self, q):
        self.cur.execute(q)
        self.cnx.commit()
        return self.cur.lastrowid

    def update(self, q):
        self.cur.execute(q)
        self.cnx.commit()
        return self.cur.rowcount

    def delete(self, q):
        self.cur.execute(q)
        self.cnx.commit()
        return self.cur.rowcount

