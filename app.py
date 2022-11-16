from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from twilio.rest import Client
import mysql.connector
from mysql.connector import errorcode
from datetime import date

app = Flask(__name__)
app.config.from_object('config.Config')

#-------------------FUNCS FOR SQL STUFF--v------------------
db_server = os.environ.get('DB_SERVER')
db_user = os.environ.get('DB_USER')
db_pwd = os.environ.get('DB_PWD')

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
        print(connection)
    except mysql.connector.Error as err:
        print(f"Error: '{err}'")
    return connection

global db_connection
db_connection = create_db_connection(db_server, db_user, db_pwd, "dinnerPartyData")

def execute_query(connection, query, ret):
    cursor = connection.cursor()
    retVal = ''

    try:
        cursor.execute(query)
        if (ret and cursor):
            retVal = cursor.fetchall()
        connection.commit()
        print("Query successful")
        if (ret):
            return retVal
    except mysql.connector.Error as err:
        print(f"Error: '{err}'")
    cursor.close()
#-------------------FUNCS FOR SQL STUFF--^------------------

#-----------------------TWILIO STUFF--v---------------------
account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')
client = Client(account_sid, auth_token)

def signinConfirm(name, num):
    message = client.messages.create(
        body="Confirm login attempt for {}. Respond (y) or (n).".format(name),
        from_='+18509188050',
        to='+1{}'.format(num)
    )

    call = client.calls.get("message.sid")
    print(call.to)

    print(message.sid)
#-----------------------TWILIO STUFF--^---------------------

#--------------------SITE FLASK METHODS--v------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

@app.route("/")
def index():
    return render_template('loading-page.html')

@app.route("/checkPhone")
def numberValidate():
    inputtedNum = request.args.get('number')

    updateQ = "UPDATE eligibleNumbers SET last_login = current_timestamp() WHERE phone_number = %s;" % str(inputtedNum)
    nameQ = "SELECT first_name FROM eligibleNumbers WHERE %s = phone_number" % str(inputtedNum)

    execute_query(db_connection, updateQ, False)
    retVal = str(execute_query(db_connection, nameQ, True))[3:-4]

    if (retVal, inputtedNum):
        signinConfirm(retVal, inputtedNum)

    return jsonify({"result": retVal})

@app.route("/newPage")
def changePages():
    inputtedPage = request.args.get('page')
    return render_template(inputtedPage)

@app.route("/rsvpData")
def getRsvps():
    dates = ['rsvp_1', 'rsvp_2', 'rsvp_3', 'rsvp_4', 'rsvp_5', 'rsvp_6', 'rsvp_7', 'rsvp_8', 
             'rsvp_9', 'rsvp_10', 'rsvp_11', 'rsvp_12', 'rsvp_13', 'rsvp_14', 'rsvp_15', 'rsvp_16']
    rsvps = []

    name = request.args.get('name')
    number = request.args.get('number')

    maxDateQ = "SELECT party_id FROM partyInfo WHERE date < '2022-09-18' ORDER BY party_id DESC LIMIT 1" #CURDATE()
    maxDate = int(execute_query(db_connection, maxDateQ, True)[0][0])

    for i in range(maxDate):
        print(str(i) + ": " + dates[i])
        rsvpQ = "SELECT %s FROM eligibleNumbers WHERE phone_number = %s AND %s = 1" % (dates[i], str(number), dates[i])
        if execute_query(db_connection, rsvpQ, True):
            rsvps.append(i+1)

    print(rsvps)
    return rsvps

@app.route("/updateRsvp")
def updateRsvp():
    number = request.args.get('number')
    status = request.args.get('status')

    updateQ = "UPDATE eligibleNumbers SET %s = %d WHERE phone_number = %s" % (status, number)
    execute_query(db_connection, updateQ, False)
#--------------------SITE FLASK METHODS--^------------------


#-----------------------STUFF THATS NOT USED---v--------------------
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Server connection successful")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(f"Error: '{err}'")
    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

@app.route("/createDB")
def createDB():
    return "creating DB now"
