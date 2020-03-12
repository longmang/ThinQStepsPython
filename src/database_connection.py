from mysql import connector
from mysql.connector import errorcode

cnx = connector.connect()


def database_open():
    try:
        global cnx
        cnx = connector.connect(user='tfmember', password='tr41n3R', host='192.168.1.22',
                                database='tdmstep', port='3306')
    except connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print("Database connection seemed to work")


def database_close():
    cnx.close()


def activate_new_user(idaccounts):
    cursor = cnx.cursor()
    query = ("UPDATE accounts SET status = 1 WHERE logintype = 'DUMMY' AND idaccounts = {}".format(idaccounts))
    print("Query: " + query)
    cursor.execute(query)
    cnx.commit()


def set_gcm_notify_day_percentages():
    cursor = cnx.cursor()
    query = ("UPDATE gcmnotifycheck SET day25perc = 0, day50perc = 0, day75perc = 0, day100perc = 0")
    print("Query: " + query)
    cursor.execute(query)
    cnx.commit()
