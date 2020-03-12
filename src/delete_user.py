import rest_connection


def delete_user(idaccounts):

    rest_connection.delete_user_by_id(idaccounts)

#for i in range(46, 56, 1):
    #print(i)
    #delete_user(str(i))

delete_user('47')
