import mariadb
from flask import Flask, request, Response
import json
import dbcreds
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST', 'DELETE'])
def login():
    if request.method == 'POST':
        conn = None
        cursor = None
        user_username = request.json.get("username")
        user_password = request.json.get("password")
        users = None
        rows = None
        user = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", [user_username, user_password])
            users = cursor.fetchall()
            print(users)
            if users != None and users != []:
                user_id = users[0][0]
                print(user_id)
                token = random.randint(0, 10000000)
                cursor.execute("INSERT INTO user_login(token, user_id) VALUES(?, ?)", [token, user_id])
                conn.commit()
                rows = cursor.rowcount
                print(rows)
                user = {
                    "id": users[0][0],
                    "username": users[0][1],
                    "token": token
               }
        except Exception as error:
            print("Something went wrong (THIS IS LAZAY): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response(json.dumps(user, default=str), mimetype="text/html", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    if request.method == 'DELETE':
        conn = None
        cursor = None
        rows = None
        post_token = request.json.get("token")
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_login WHERE token=?", [post_token,])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong (THIS IS LAZAY): ")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if rows == 1:
                return Response("logout success!", mimetype="text/html", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)

@app.route('/post', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def posts():
    if request.method == 'GET':
        conn = None
        cursor = None
        posts = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM post")
            posts = cursor.fetchall()
        except Exception as error:
            print("Something went wrong (THIS IS LAZAY): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(posts != None):
                return Response(json.dumps(posts, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'POST':
        conn = None
        cursor = None
        post_username = request.json.get("username")
        post_content = request.json.get("content")
        post_token = request.json.get("token")
        rows = None

        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_login WHERE token=?", [post_token,])
            user = cursor.fetchone()
            print(user)
            if user != None and user != []:
                user_id = user[0]
                cursor.execute("INSERT INTO post(username, content, user_id) VALUES(?, ?, ?)", [post_username, post_content, user_id])
                conn.commit()
                rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong (THIS IS LAZAY): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("Post Inserted!", mimetype="text/html", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'PATCH':
        conn = None
        cursor = None
        post_token = request.json.get("token")
        post_content = request.json.get("content")
        post_id = request.json.get("postId")
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor() 
            cursor.execute("SELECT * FROM user_login WHERE token=?", [post_token,])
            user = cursor.fetchone()
            if user != None and user != []:
                user_id = user[0]
                if post_content != "" and post_content != None:
                    cursor.execute("UPDATE post SET content=? WHERE postId=? and user_id=?", [post_content, post_id, user_id])
                conn.commit()
                rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong (THIS IS LAZY)")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if rows == 1:
                return Response("Updated Success", mimetype="text/html", status=204)
            else:
                return Response("Updated failed", mimetype="text/html", status=500)
    
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        post_token = request.json.get("token")
        post_id = request.json.get("id")
        rows = None
        user = None
        try:
            conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, port=dbcreds.port, database=dbcreds.database, host=dbcreds.host)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_login WHERE token=?", [post_token,])
            user = cursor.fetchone()
            print(user)
            if user != None and user != []:
                user_id = user[0]
                print(user_id) 
                cursor.execute("DELETE FROM post WHERE postId=? AND user_id=?", [post_id, user_id])
                conn.commit()
                rows = cursor.rowcount

        except Exception as error:
            print("Something went wrong (THIS IS LAZY)")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if rows == 1:
                return Response("Delete Success", mimetype="text/html", status=204)
            else:
                return Response("Delete failed", mimetype="text/html", status=500)

    
