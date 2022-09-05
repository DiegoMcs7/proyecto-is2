import os
import psycopg2
from django.http import HttpResponseForbidden

USER_FIELDS = ['username', 'email']


def create_user(strategy, details, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    allowed_emails = get_whitelisted_emails()

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in strategy.setting('USER_FIELDS', USER_FIELDS))
    if not fields:
        return

    print(fields[('email')] in next(zip(*allowed_emails)))

    if fields[('email')] in next(zip(*allowed_emails)):

        return {
            'is_new': True,
            'user': strategy.create_user(**fields)
        }
    else:
        return HttpResponseForbidden("No estas registrado")


def get_whitelisted_emails():
    whitelisted_domains_emails = []
    try:

        connection = psycopg2.connect(user='postgres',
                                      password='admin',
                                      host='127.0.0.1',
                                      port='5432',
                                      database='gestorProyectos')
        cursor = connection.cursor()
        get_whitelisted_domains_emails = "SELECT email FROM auth_user WHERE is_active=True;"
        cursor.execute(get_whitelisted_domains_emails)
        whitelisted_domains_emails = cursor.fetchall()
        print(whitelisted_domains_emails)
        connection.close()

    except(Exception, psycopg2.Error) as error:

        print('Failed to connect to database...')

    return whitelisted_domains_emails