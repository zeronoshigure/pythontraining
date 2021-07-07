'''
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
    polls/
        __init__.py
        admin.py
        apps.py
        migrations/
            __init__.py
        models.py
        tests.py
        views.py
'''

from msvcrt import getch

def select():
    pass

def moveDown():
    print("↓")

def moveUp():
    print("↑")

def main3():
    while True:
        key = ord(getch())
        print(key)
        if key == 27: #エスケープ
            break
        elif key == 13:
            select()

        elif key == 0: #スペシャルキー（矢印、Fキー、ins、del、など）
            key = ord(getch())
            
            if key == 80: #上矢印
                moveDown()
            elif key == 72: #下矢印
                moveUp()

main3()