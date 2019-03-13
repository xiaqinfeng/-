import json
import requests
import sqlite3
import sql
import os
import time
import bs4
import watchdog
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 10.0; WOW64; Trident/8.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729))'}
from bs4 import BeautifulSoup
from watchdog.observers import Observer
from watchdog.events import *

filename1='E:/Microsoft VS Code/PythonWork/微信自动答题/题库/e553471481162.fengchuanba.com/service/explore/personalExploreDetail'
filename2='E:/Microsoft VS Code/PythonWork/微信自动答题/题库/e553471481162.fengchuanba.com/service/explore2/nextCheckPoint'
filename3='E:/Microsoft VS Code/PythonWork/微信自动答题/题库/e553471481162.fengchuanba.com/service/explore2/finishExplore'
filename4='E:/Microsoft VS Code/PythonWork/微信自动答题/题库/e553471481162.fengchuanba.com/service/explore2/startExplore'
def read_question():
    try:
        with open(filename2, encoding='utf-8') as f:
            response=json.load(f)
        question=response['question']['content']
        print(question)
        sql_result=sql_match_result('"%s"' % question)
        if sql_result:
            print('Question: '+question)
            print('绝对正确答案:%s' % sql_result)
        else:
            print('不知道答案，你先瞎填吧！')
    except Exception as e:
        print(e)
    finally:
        if f:
            f.close()

def read_start_question():
    try:
        with open(filename4, 'r',encoding='utf-8') as f:
            response=json.load(f)
        question=response['question']['content']
        print(question)
        sql_result=sql_match_result('"%s"' % question)
        if sql_result:
            print('Question: '+question)
            print('绝对正确答案:%s' % sql_result)
        else:
            print('不知道答案，你先瞎填吧！')
    except  Exception as e:
        print(e)
    finally:
        if f:
            f.close()


def save_question():
    try:
        with open(filename1,'r', encoding='utf-8') as f:
            response=json.load(f)
        for item in response['exploreList']:
            question=item['content']
            answer=item['correct']
            if item['detail']!="":
                detail=''
                answerdetail=item['detail']
                answerdetail=json.loads(answerdetail)
                choiceList=answerdetail['choiceList']
                for i in choiceList:
                    detail=detail+' '+str(i['tag'])+' '+i['content']
                wirte_sql(question,answer,detail)
            else:
                wirte_sql(question,answer,'')
    except Exception as e:   
        print(e)
    finally:
        if f:
            f.close()
def wirte_sql(question,answer,answerdetail):
    conn = sqlite3.connect("E:\Microsoft VS Code\PythonWork\微信自动答题\dati.db",check_same_thread=False)
    try:
        sql = "insert or ignore into tiku(question,answer,answerdetail)values('%s','%s','%s')" % (question,answer,answerdetail)
        print(sql)
        conn.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)

def sql_match_result(question):
    conn = sqlite3.connect("E:\Microsoft VS Code\PythonWork\微信自动答题\dati.db",check_same_thread=False)
    right_answer=''
    sql_cmd = 'select * from tiku where question=' + question
    cursor = conn.execute(sql_cmd)
    for row in cursor:
        right_answer = row[1]
    if not right_answer=='' :
        return right_answer
    else:
        return False

class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)
    def on_modified(self,event):
        if not event.is_directory:
            last_name=event.src_path.split('\\')[-1]
            print(last_name)
            try:
                if last_name == 'startExplore':
                    print("开始答题！")
                    read_start_question()
                elif last_name == 'personalExploreDetail':
                    save_question()
                elif last_name == 'nextCheckPoint':
                    read_question()
                elif last_name == 'finishExplore':
                    print("答题结束！")
            except:
                pass

if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler,'E:/Microsoft VS Code/PythonWork/微信自动答题/题库/e553471481162.fengchuanba.com/service',True)
    print('-----答题器已运行-----')
    observer.start()
    observer.join()