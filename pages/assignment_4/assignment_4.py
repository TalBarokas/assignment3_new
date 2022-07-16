from flask import Blueprint, render_template, Flask, redirect, url_for, request, session, json , jsonify
import mysql.connector

assignment_4 = Blueprint('assignment_4', __name__, static_folder='static', template_folder='templates')


def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='myflaskappdb')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)


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

@assignment_4.route('/assignment_4')
def assignment_4_func():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template("assignment_4.html", users=users_list)

@assignment_4.route('/insert_user', methods=['POST'])
def insert_user():
    name = request.form['name']
    email = request.form['email']
    print(f'{name} {email} ')
    query = "INSERT INTO users(name, email) VALUES ('%s', '%s')" % (name, email)
    interact_db(query=query, query_type='commit')
    return redirect('/assignment_4')

@assignment_4.route('/update_user', methods=['POST'])
def update_user():
    name = request.form['name']
    age = request.form['age']
    query = "UPDATE users SET age='%s' WHERE name='%s'" % (age, name)
    interact_db(query=query, query_type='commit')
    return redirect('/assignment_4')

@assignment_4.route('/delete_user', methods=['POST'])
def delete_user_func():
    user_id = request.form['user_id']
    query = "DELETE FROM users WHERE id='%s';" % user_id
    # print(query)
    interact_db(query, query_type='commit')
    return redirect('/assignment_4')




