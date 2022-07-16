from flask import Flask, redirect, url_for, render_template, request, session, jsonify
from datetime import timedelta
import mysql.connector
import requests
import random

app = Flask(__name__,template_folder='templates')

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_PERMANENT_LIFETIME'] = timedelta(minutes=20)

from pages.assignment_4.assignment_4 import assignment_4
app.register_blueprint(assignment_4)

@app.route('/home')
@app.route('/')
def home_route():
    username = ''
    return render_template("homepage.html", username=username)

@app.route('/home')
def home_func():
    return redirect('/')

@app.route('/homepage')
def homepage_func():
    return redirect(url_for('home_route'))

@app.route('/contact')
def contact_func():
    return render_template("contact.html")


curr_user= {'firstname': "Tal", 'Lastname': "Barokas"}
#curr_user = ''
@app.route('/assignment3_1' )
def assignment3_1():
    return render_template("assignment3_1.html",
                           hobbies=['Dance', 'Sing', 'Reading Books', 'Watch movies', 'Traveling'], curr_user=curr_user)

users = {'Yossi': {'email': "yossi@gmail.com"}, 'Namma': {'email': "Namma@gmail.com"},
                                                         'Arseni': {'email': "Arseni@gmail.com"}, 'Rotem': {'email': "Rotem@gmail.com"},
                                                         'Moshe': {'email': 'Moshe@gmail.com'}}
users_dict ={'arseni':'1234', 'Yossi':'5678'}
@app.route('/assignment3_2', methods= ['GET','POST'])
def assignment3_2():
    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['password']
        session['username'] = username
        session['password'] = password
        if username in users_dict:
            pas_in_dict = users_dict[username]
            if pas_in_dict == password:
                session['username'] = username
                return render_template('assignment3_2.html', message='Wellcom', username=username)
            else:
                return render_template('assignment3_2.html', message='Wrong password')
        else:
            new_user={username: password}
            users_dict.update(new_user)
            return render_template('assignment3_2.html', message='registration Succeed')

    return render_template('assignment3_2.html')

@app.route('/friends')
def friends():
    return render_template("friends.html", hobbies=['Dance', 'Sing', 'Reading Books', 'Watch movies', 'Traveling'], curr_user=curr_user)

@app.route('/log_out')
def logout():
    session.clear()
    return redirect(url_for('assignment3_2'))

def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='myflaskappdb')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)
    #

    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value

@app.route('/assignment4/users')
def assignment4_users_func():
    query = 'SELECT * FROM users'
    users_list = interact_db(query, query_type='fetch')
    return jsonify(users_list)

@app.route('/assignment_4/outer_source', methods=['POST', 'GET'])
def outer_source():
    if request.method == 'POST':
        id = request.form['backend_id']
        reqres = "https://reqres.in/api/users/%s" % (str(id),)
        return redirect(reqres)
    else:
        return render_template('assignment4_outer_source.html')


@app.route('/assignment_4/restapi_users', defaults={'user_id': 1})
@app.route('/assignment_4/restapi_users/<int:user_id>')
def get_user(user_id):
    query = f'select * from users where id= {user_id}'
    users_list = interact_db(query, query_type='fetch')

    if len(users_list) == 0:
        return_dict = {
            'message': 'user not found'
        }
    else:
        user_list = users_list[0]
        return_dict = {'name': user_list.name,
                       'email': user_list.email
                       }
    return jsonify(return_dict)


if __name__ == '__main__':
    app.run(debug=True)
