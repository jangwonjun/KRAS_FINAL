from env import FLASK_ENUM, SQL
import pymysql
from flask import Flask, request, redirect, render_template, url_for, session

class time_checker():

    def __init__(self):
        pass


    def time_list(self):
        
        conn = pymysql.connect(
            host=SQL.HOST, port=SQL.PORT, user=SQL.ID, passwd=SQL.PASSWORD, db=SQL.DB_NAME, charset='utf8'
        )
            
        print("DB연결 완료")

        cursor = conn.cursor()

        sql_query = "SELECT name FROM kras_list"

        cursor.execute(sql_query)

        list = cursor.fetchall()

        print(list)

        conn.commit()
        conn.close()


        return list
