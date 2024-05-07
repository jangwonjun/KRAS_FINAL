from env import FLASK_ENUM, SQL
import pymysql
from flask import Flask, request, redirect, render_template, url_for, session
import copy

class time_table_system():
    def __init__(self):
        
        pass
    
    def table_data(self,id):

        self.id = id
        print("id출력",id)

        conn = pymysql.connect(
            host=SQL.HOST, port=SQL.PORT, user=SQL.ID, passwd=SQL.PASSWORD, db=SQL.DB_NAME, charset='utf8'
        )

        cursor = conn.cursor()

        subject_sql = "SELECT subject FROM kras_login WHERE id = %s"
        cursor.execute(subject_sql,(self.id))
        subject_sql = cursor.fetchall()

        info_string = subject_sql[0][0]

        info_list = info_string.split(',')

        result = [info.split('-') for info in info_list]
        time = [info[5:8].split('/') for info in info_list]



        #6교시 까지 있다고 가정
        self.time = time


        print(self.time)
        print("남는 시간 출력완료")
        
        onetime = [1,2,3,4,5]
        twotime = [1,2,3,4,5]
        threetime = [1,2,3,4,5]
        fourtime = [1,2,3,4,5]
        fivetime = [1,2,3,4,5]

        # 초기 값 저장
        original_values = {
            "onetime": copy.deepcopy(onetime),
            "twotime": copy.deepcopy(twotime),
            "threetime": copy.deepcopy(threetime),
            "fourtime": copy.deepcopy(fourtime),
            "fivetime": copy.deepcopy(fivetime)
        }

        # 작업 수행
        onetime.remove(int(self.time[0][0]))
        onetime.remove(int(self.time[0][1]))

        twotime.remove(int(self.time[1][0]))
        twotime.remove(int(self.time[1][1]))

        threetime.remove(int(self.time[2][0]))
        threetime.remove(int(self.time[2][1]))

        fourtime.remove(int(self.time[3][0]))
        fourtime.remove(int(self.time[3][1]))

        fivetime.remove(int(self.time[4][0]))
        fivetime.remove(int(self.time[4][1]))

        final_rest_schedule = [onetime, twotime, threetime, fourtime, fivetime]
        
        print("최종남는시간",final_rest_schedule)
        # 변수 초기화
        onetime = original_values["onetime"]
        twotime = original_values["twotime"]
        threetime = original_values["threetime"]
        fourtime = original_values["fourtime"]
        fivetime = original_values["fivetime"]

        return (result,final_rest_schedule)
        




