from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import mysql.connector
from mysql.connector import errorcode
from datetime import date
app = Flask(__name__)

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
# Read the config 
# and use the values from config to connect

# This is local 
#db_connection = create_db_connection("localhost", "root", "PercyJackson18!", "dinnerPartyData")

db_server = "guestlist.cynpj4no4mcx.us-east-1.rds.amazonaws.com"
db_user= "admin"
db_pwd="PercyJackson18"

# This is at AWS
db_connection = create_db_connection( db_server, db_user, db_pwd, "dinnerPartyData")

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



# flask starts here
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

    print(retVal)
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

    updateQ = "UPDATE eligibleNumbers SET %s = %d WHERE phone_number = %s"
    execute_query(db_connection, updateQ, False)


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

@app.route("/start")
def startDef():
    connection = create_db_connection("localhost", "root", "PercyJackson18!", "dinnerPartyData")
    create_db_query = "CREATE DATABASE dinnerPartyData"
    create_database(connection, create_db_query)

    table_sql = """
    DROP TABLE IF EXISTS eligibleNumbers;
    CREATE TABLE eligibleNumbers (
    phone_number VARCHAR(12) PRIMARY KEY,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(40) NOT NULL,
    last_login DATETIME NULL,
    rsvp_1 BIT NOT NULL,
    rsvp_2 BIT NOT NULL,
    rsvp_3 BIT NOT NULL,
    rsvp_4 BIT NOT NULL,
    rsvp_5 BIT NOT NULL,
    rsvp_6 BIT NOT NULL,
    rsvp_7 BIT NOT NULL,
    rsvp_8 BIT NOT NULL,
    rsvp_9 BIT NOT NULL,
    rsvp_10 BIT NOT NULL,
    rsvp_11 BIT NOT NULL,
    rsvp_12 BIT NOT NULL,
    rsvp_13 BIT NOT NULL,
    rsvp_14 BIT NOT NULL,
    rsvp_15 BIT NOT NULL,
    rsvp_16 BIT NOT NULL
    );
    INSERT INTO eligibleNumbers VALUES
    ('2032909487', 'Srishti', 'Pithadia', NULL, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ('9087988587', 'Sai', 'Avula', NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ('2039885528', 'Alyssa', 'Lent', NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ('7745059573', 'Sahit', 'Bolla', NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ('9259170405', 'Amado', 'Uyehara', NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ('9082855004', 'Keerti', 'Sundaram', NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ('4082198058', 'Rishika', 'Jandhyala', NULL, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

    DROP TABLE IF EXISTS partyInfo;
    CREATE TABLE partyInfo (
    party_id INT PRIMARY KEY,
    theme VARCHAR(40) NOT NULL,
    date DATETIME NOT NULL
    );
    INSERT INTO partyInfo VALUES
    (1, 'Ocean', '2022-08-30'),
    (2, 'Mafia', '2022-09-06'),
    (3, 'Identity Theft', '2022-09-13'),
    (4, 'Sleepover', '2022-09-20'),
    (5, 'Rave', '2022-09-27'),
    (6, 'Midsommar', '2022-10-04'),
    (7, 'Red Carpet', '2022-10-11'),
    (8, 'Nursing Home', '2022-10-18'),
    (9, 'Halloween', '2022-10-25'),
    (10, 'Diwali', '2022-11-01'),
    (11, 'Red Flags', '2022-11-08'),
    (12, 'Decades', '2022-11-15'),
    (13, 'Friendsgiving', '2022-11-22'),
    (14, 'Emo Night', '2022-011-29'),
    (15, 'Alice In Wonderland', '2022-12-06'),
    (16, 'Holiday', '2022-12-13');

    DROP TABLE IF EXISTS contributionList;
    CREATE TABLE contributionList (
    contlist_id INT AUTO_INCREMENT PRIMARY KEY,
    sub_contlist_id INT NOT NULL,
    party_id INT NOT NULL,
    item VARCHAR(40) NOT NULL,
    quantity INT NOT NULL,
    value INT NOT NULL,
    claimed BIT NOT NULL,
    claimed_by VARCHAR(40) NULL
    );
    INSERT INTO contributionList VALUES
    (NULL, 1, 1, 'Spinach Dip', 1, 1, 0, NULL),
    (NULL, 2, 1, 'Baguette Bread', 1, 1, 0, NULL),
    (NULL, 3, 1, 'Sour Cream', 1, 1, 0, NULL),
    (NULL, 4, 1, 'Salsa', 1, 1, 0, NULL),
    (NULL, 5, 1, 'Gummy Lifesavers Pack', 1, 1, 0, NULL),
    (NULL, 6, 1, 'Airheads Sour Belt Pack', 1, 1, 0, NULL),
    (NULL, 7, 1, 'Lime', 3, 1, 0, NULL),
    (NULL, 1, 2, 'Extra Virgin Olive Oil', 1, 1, 0, NULL),
    (NULL, 2, 2, 'Baguette Bread', 1, 1, 0, NULL),
    (NULL, 3, 2, 'Basil Leave Pack', 5, 1, 0, NULL),
    (NULL, 4, 2, 'Ferrero Rocher Pack', 1, 1, 0, NULL),
    (NULL, 5, 2, 'Cherry Tomato Pack', 2, 1, 0, NULL),
    (NULL, 6, 2, 'Gold Coin Chocolate Pack', 2, 1, 0, NULL),
    (NULL, 1, 3, 'Croissant Pack', 1, 1, 0, NULL),
    (NULL, 2, 3, 'Raspberries', 1, 1, 0, NULL),
    (NULL, 3, 3, 'Blueberries', 1, 1, 0, NULL),
    (NULL, 4, 3, 'Strawberries', 2, 1, 0, NULL),
    (NULL, 5, 3, 'Banana', 2, 1, 0, NULL),
    (NULL, 6, 3, 'Grapefruit', 1, 1, 0, NULL),
    (NULL, 7, 3, 'Blackberries', 1, 1, 0, NULL),
    (NULL, 8, 3, 'Cheese', 1, 1, 0, NULL),
    (NULL, 9, 3, 'Crackers Pack', 1, 1, 0, NULL),
    (NULL, 10, 3, 'Pomogranate', 1, 1, 0, NULL),
    (NULL, 11, 3, 'Avocado', 3, 1, 0, NULL),
    (NULL, 12, 3, 'Champagne', 1, 2, 0, NULL);
    """
    execute_query(db_connection, table_sql)

@app.route("/createDB")
def createDB():
    return "creating DB now"