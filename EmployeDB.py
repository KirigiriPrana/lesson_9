from typing import Any
from sqlalchemy import create_engine
from sqlalchemy import text
import psycopg2
import sqlalchemy


class EmployerTable:
    scripts = {
        'insert_new': text('insert into company(name) values (:new_name)'),
        'get_max_id_company': text('select MAX(id) from company'),
        'max_id_employee': text('select MAX(id) from employee where company_id=(:id_comp)'),
        'select_employee': text('select * from employee where company_id =(:company_id)'),
        'delete_by_id': text('delete from company where id =(:id_to_delete)'),
        'create_employee': text(
            'insert into employee(company_id, first_name, last_name, phone) values(:company_id, :first_name, :last_name, :phone)'),
        'clear_table': text('DELETE FROM employee  where company_id =(:id_clear)'),
        'select_by_id': text('select * from employee where id =(:select_id)')
    }

    def __init__(self, connection_string):
        self.db = create_engine(connection_string)

    def create_company(self, name: str):
        with self.db.connect() as connection:
            result = connection.execute(self.scripts["insert_new"], {"new_name": name})

            return result

    def get_max_id_comp(self):
        with self.db.connect() as connection:
            result = connection.execute(self.scripts["get_max_id_company"]).fetchall()[0][0]

            return result

    def get_max_id_emp(self, id):
        with self.db.connect() as connection:
            result = connection.execute(self.scripts["max_id_employee"], {"id_comp": id}).fetchall()[0][0]

            return result

    def select_employers(self, id):
        with self.db.connect() as connection:
            result = connection.execute(self.scripts["select_employee"], {"company_id": id}).fetchall()

            return result

    def delete_company(self, id):
        with self.db.connect() as connection:
            result = connection.execute(self.scripts["delete_by_id"], {"id_to_delete": id})

            return result

    def create_employer(self, company_id: int, f_name: str, l_name: str, phone: str):
        with self.db.connect() as connection:
            result = connection.execute(self.scripts["create_employee"],
                                        {"company_id": company_id, "first_name": f_name, "last_name": l_name, "phone": phone})
            return result.fetchall()

    def clear_table_employers(self, id):
        with self.db.connect() as connection:
            result = connection.execute(self.scripts["clear_table"], {"id_clear": id})

            return result

    def get_employer_by_id(self, id):
        with self.db.connect() as connection:
            result = connection.execute(self.scripts["select_by_id"], {"select_id": id}).fetchone()

            return result
