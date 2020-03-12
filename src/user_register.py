import csv
import rest_connection
import database_connection
import uuid
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz

__author__ = 'paulgullett'


def add_user_data():

    with open('../res/ThinQStepsSchema.csv', 'r') as f:
        reader = csv.DictReader(f)

        data = {}
        userdata = {}

        for row in reader:

            data['email'] = row['email']
            data['password'] = row['password']
            data['logintype'] = row['logintype']
            data['loginidentifier'] = row['loginidentifier']

            userdata['firstname'] = row['firstname']
            userdata['secondname'] = row['secondname']
            userdata['gender'] = row['gender']
            userdata['dob'] = row['dob']
            userdata['age'] = row['age']
            userdata['weight'] = row['weight']
            userdata['height'] = row['height']
            userdata['identifier'] = row['identifier']
            userdata['lastlogin'] = row['lastlogin']

            data['stepstarget'] = row['stepstarget']
            data['distancetarget'] = row['distancetarget']
            data['minutestarget'] = row['minutestarget']
            data['caloriestarget'] = row['caloriestarget']
            data['linkedtargets'] = row['linkedtargets']
            data['linkedposition'] = row['linkedposition']
            data['metricimperial'] = row['metricimperial']

            data['devicename'] = row['devicename']
            data['deviceid'] = row['deviceid']
            data['devicesimplename'] = row['devicesimplename']
            data['deviceos'] = row['deviceos']

            data['userdata'] = userdata

            url = row['avatar']

            rest_connection.post_register_user(data, url, activate_and_subscribe_dummy_user)


def activate_and_subscribe_dummy_user(idaccounts):

    print("Active user: {}".format(idaccounts))

    database_connection.database_open()
    database_connection.activate_new_user(idaccounts)
    database_connection.database_close()

    data = {}
    subscription_data = {}
    now = datetime.now(pytz.UTC) + relativedelta(months=+12)

    subscription_number = rest_connection.get_subscription_number()
    subscription_data['ordernumber'] = "TQSD{}".format(subscription_number)
    subscription_data['reference'] = "Dummy Subscription"
    subscription_data['idaccounts'] = idaccounts
    subscription_data['recurring'] = 0
    subscription_data['months'] = 12
    subscription_data['gatewayresponse'] = uuid.uuid4().hex
    subscription_data['dateexpires'] = int(now.timestamp())

    data['data'] = subscription_data

    print(data)

    rest_connection.add_dummy_subscription(data)

if __name__ == "__main__":
    add_user_data()