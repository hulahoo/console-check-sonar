import inspect
import os

from django.db import connection

from console_api.settings.settings import BASE_DIR


def run_sql_file(file_name, module_name=None, sql_folder='sql', params=None):
    if not module_name:
        catalog = os.path.split(inspect.stack()[1].filename)[0]
    else:
        catalog = os.path.join(BASE_DIR, module_name, 'migrations')

    def load_data_from_sql(app, schema_editor):
        file_path = os.path.join(catalog, sql_folder, file_name)
        sql_statement = open(file_path, encoding='utf-8').read()
        if params:
            sql_statement = sql_statement.format(**params)
        with connection.cursor() as c:
            c.execute(sql_statement)
    return load_data_from_sql
