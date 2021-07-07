########2021年度版出席登録出力プログラム#############
'''
仕様書
1,総合月単位数A,Bを入力。
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

year = "2021"
############データベース用意#############
dbname = 'attendance.db'
conn = sqlite3.connect(dbname)
c = conn.cursor()
#######################################
#データベースのテーブル確認用
'''
    c.execute("select * from sqlite_master where type='table'")
    for row in c.fetchall():
        print(row)
'''
################準備枠#################
def isBizDay(DATE):#祝日判定してくれる(1が平日0が祝日)
    Date = datetime.date(int(DATE[0:4]), int(DATE[4:6]), int(DATE[6:8]))
    if Date.weekday() >= 5 or jpholiday.is_holiday(Date):
        return 0
    else:
        return 1

def pulsezero(listc,mon,x,y):#日付修正orz 最初から0有り仕様が欲しかった…。
    if len(str(listc[x][y]))<2 and len(str(mon))>=2:#日付が1～9日の場合
       # print(year+mon+'0'+str(listc[x][y]))
        x=isBizDay(year+mon+'0'+str(listc[x][y]))
    elif len(str(listc[x][y]))<2 and len(str(mon))<2:#日付が1～9日かつ月が1~10の場合
       # print(year+'0'+mon+'0'+str(listc[x][y]))
        x=isBizDay(year+'0'+mon+str(listc[x][y]))
    elif len(str(listc[x][y]))>=2 and len(str(mon))<2:#日付が11～日かつ月が1～10の場合
       # print(year+'0'+mon+str(listc[x][y]))
        x=isBizDay(year+'0'+mon+str(listc[x][y]))
    else:
        x=isBizDay(year+mon+str(listc[x][y]))
    return x

######################################


def month():#1,総合月単位数A,Bを入力。
    numb = input("学生のIDをITorAIから入力してください：")#IT20001~
    mon = input("欲しいデータ月を入力してください：")#1~12
    A = input("ロボット有りの学生ならA、無しならBを入力してください：")#A or B
    online = input("この月のオンラインでの授業日数を教えてください。")
    if A == "A" or A == "B":
        pass
    else:
        numb,mon,A,online = month()
    return numb,mon,A,online


def sqlstart(num,year,mon):#2,SQLにIDと月とA,Bどちらかを打ち込む。
    df = pd.read_sql("SELECT date FROM record WHERE number=(?) AND date LIKE ?",conn,params=(num,year+'-'+mon+'%',))
    #print(df)#test
    print("合計",len(df),"日出席しています")
    return df
                


def wefrset(mon):#水曜日と金曜日の特殊処理
    listc=calendar.monthcalendar(int(year), int(mon))
    wed=[]
    fri=[]
    for i in range(len(listc)):#水曜日の数
        if listc[i][2] != 0 and pulsezero(listc,mon,i,2) == 1:
            
            if len(str(listc[i][2])) == 1:
                wed.append("0"+str(listc[i][2]))
            else:
                wed.append(str(listc[i][2]))
        if listc[i][4] != 0:
            if len(str(listc[i][4])) == 1:
                fri.append("0"+str(listc[i][4]))
            else:
                fri.append(str(listc[i][4]))
    return wed,fri



def alldays(mon,wed,fri,A):#出席可能日数算出
    listc=calendar.monthcalendar(int(year), int(mon))
    days=[]
    
    for i in range(len(listc)):
        for j in range(5):#月曜火曜水曜木曜金曜
            x=0
            if listc[i][j] != 0:
                if len(str(listc[i][j]))<2 and len(str(mon))>=2:#日付が1～9日の場合
                   # print(year+mon+'0'+str(listc[i][j]))
                    x=isBizDay(year+mon+'0'+str(listc[i][j]))
                elif len(str(listc[i][j]))<2 and len(str(mon))<2:#日付が1～9日かつ月が1~10の場合
                   # print(year+'0'+mon+'0'+str(listc[i][j]))
                    x=isBizDay(year+'0'+mon+str(listc[i][j]))
                elif len(str(listc[i][j]))>=2 and len(str(mon))<2:#日付が11～日かつ月が1～10の場合
                    #print(year+'0'+mon+str(listc[i][j]))
                    x=isBizDay(year+'0'+mon+str(listc[i][j]))
                else:
                    x=isBizDay(year+mon+str(listc[i][j]))
            if x == 1:
                      days.append(listc[i][j])
            else:
                pass
    date = (len(days))
    print("今月の出席可能日数は",date,"日です。")
    return date

def maching(attend,wf,mon):#水曜日と金曜日の日付分追加日数を返す。
    attendall=[]
    count=0
    for i in range(len(attend)):#ほんとはしたくない・・・。良案求！！！！！！！！！！！！！！！
        print([s.replace('-','') for s in attend[i]],end=' ')
        for j in range(len(wf)):
            wedlist=[year+mon+str(wf[j])]
            
            if [s.replace('-','') for s in attend[i]] == wedlist:
                count+=1 
                
                print("金曜")  
                #attend_list=[s.replace('-','') for s in attend[i]] 
            
            attend_list=[s.replace('-','') for s in attend[i]] 
        attendall.append(attend_list)
    print("end")
    return count
    #print("今月の",numb,"の出席時間数は",(len(attendall)+count+int(online))*4,"時間でした")

def main():
    numb,mon,A,online = month()#A or B ロボット有り　or 無し 月と学籍番号出す

    wed,fri = wefrset(mon)  #水曜日と金曜日の取り出し
    day = alldays(mon,wed,fri,A)      #出席可能日数呼び出し
    
    if len(mon) <2:#１～９月の場合の処理
         mon = "0"+mon
    #mon =year+"-"+mon
    
    df=sqlstart(numb,year,mon)  #SQLで確認、pdで取り出してる。
 #############水曜日判定#################################################
    attend=df.values.tolist()
    count=maching(attend,wed,mon)
    count2=maching(attend,fri,mon)
    print("出席日数は",len(df),"日、オンラインが",online,"日")
    print("日本語の授業は",count,"日間です、確認して下さい。")
    if A == "A":
        print("ロボットの授業は",len(fri),"日間です。確認して下さい")
        print("今月の",numb,"の出席時間数は",(len(df)+count+count2+int(online))*4,"時間でした")
    else:
        print("今月の",numb,"の出席時間数は",(len(df)+count+int(online))*4,"時間でした")
    #print("出席率は",maching(attend,wed,mon,online)/day*100,"%です。")
            
    #print(wed)
 #####################################################################
    
for i in range(17): 
    main()


conn.close()
