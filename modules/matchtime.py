from env import FLASK_ENUM, SQL
import pymysql
from flask import Flask, request, redirect, render_template, url_for, session
from modules.timetable import time_table_system

class matchsystem():

    def __init__(self) -> None:
        pass


    def search_friend(self):
        target_member = time_table_system()
        conn = pymysql.connect(
            host=SQL.HOST, port=SQL.PORT, user=SQL.ID, passwd=SQL.PASSWORD, db=SQL.DB_NAME, charset='utf8'
        )

        cursor = conn.cursor()

        sql = "SELECT id FROM kras_login"
        cursor.execute(sql)
        member = cursor.fetchall()

        print(member)

        data = []
        for i in range(len(member)):
            data.append(target_member.table_data(member[i]))
        print("matchtimedata",data[1][1])
        return data
    
    def phone_num(self, id):
    
        self.id = id 
        
        conn = pymysql.connect(
            host=SQL.HOST, port=SQL.PORT, user=SQL.ID, passwd=SQL.PASSWORD, db=SQL.DB_NAME, charset='utf8'
        )

        cursor = conn.cursor()

        sql = "SELECT phone_number FROM kras_login WHERE id = %s"
        cursor.execute(sql,(self.id))
        number = cursor.fetchall()

        return number

