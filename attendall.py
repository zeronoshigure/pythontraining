########2021年度版出席登録出力プログラム#############
'''
仕様書：全員分の欠席日数と水金出席してるかどうか知りたい
1,月と名簿(idとロボットありかなしか。)
2,SQLにIDと月とA,Bどちらかを打ち込む。
3,カレンダーで水曜の日付と金曜の日付を取り出し
4,Bの場合は金曜日の日数分*4を用意、Aの場合も同様に水曜日の日数分*4を用意。
5,その月の出席日数と出席日を表示
+α祝日を表示

6,修正用の（日数に＋or-で）入力
7,水曜金曜の出席日数をカレンダーから取り出した日付で確認
8,学生の出席日数に*4、水曜の出席率を別で計算して出席日数*4加算、金曜も同様
9,出席率をデータ/A,B*100で算出
修正したデータをでexcelに入力

'''
import sqlite3
import calendar
from numpy.lib.ufunclike import fix
import pandas as pd
import numpy
from pandas.core.frame import DataFrame

import jpholiday
import datetime
import attend

year = "2021"
############データベース用意#############
dbname = 'attendance.db'
conn = sqlite3.connect(dbname)
c = conn.cursor()
#######################################
