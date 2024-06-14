from env import FLASK_ENUM, SQL
import pymysql
from flask import Flask, request, redirect, render_template, url_for, session


class add_system():
    def __init__(self):
        pass
    
    def add_system(self,name,id, time_info):
        self.name = name
        self.id = id 
        self.time_info = time_info


        conn = pymysql.connect(
            host=SQL.HOST, port=SQL.PORT, user=SQL.ID, passwd=SQL.PASSWORD, db=SQL.DB_NAME, charset='utf8'
        )

        cursor = conn.cursor()

        # test = ["kras테스트 입니다.","1","영어3"]
        insert_query = "INSERT INTO kras_list (name, id, time_info) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (self.name, self.id, self.time_info))
    
        
        cursor.execute("SELECT * FROM kras_list")
        id_result = cursor.fetchall()

        print(id_result)


        conn.commit()
        conn.close()

        data = []
        

        #DB에 아이디 없을때 -> 예외처리완료

        return data


