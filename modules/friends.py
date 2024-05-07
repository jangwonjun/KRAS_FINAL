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
        print(member)

      
        conn.commit()
        conn.close()

        return member

    def recommend(self):
        final_data = []
        data = friend_system.database(None)
        print(len(data))
        for i in range(len(data)):
            recommend_friend = data[(len(data)-1)-i]
            print(len(recommend_friend))
            final_data.append(recommend_friend)

            #배열 형태로 정리가 됨.
        return data

        