from env import FLASK_ENUM, SQL
import pymysql
from flask import Flask, request, redirect, render_template, url_for, session



class friend_system():
    def __init__(self):
        pass
        
    def database(self):
        

        conn = pymysql.connect(
                host=SQL.HOST, port=SQL.PORT, user=SQL.ID, passwd=SQL.PASSWORD, db=SQL.DB_NAME, charset='utf8'
            )
        
        cursor = conn.cursor()

        sql_query = "SELECT name FROM kras_login "

        cursor.execute(sql_query)

        member = cursor.fetchall()
        self.member_number = len(member)

        print(self.member_number)

      
        conn.commit()
        conn.close()

        return member

    def recommend(self):
        data = friend_system.database(None)
        for i in range(self.member_number):
            recommend_friend = data[self.member_number-1+i]
            print(recommend_friend)


        return recommend_friend

        