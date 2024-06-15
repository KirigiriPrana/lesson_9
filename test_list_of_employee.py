import requests
import pytest
import psycopg2
from EmployeeApi import EmployeeApi
from EmployeDB import EmployerTable

api = EmployeeApi("https://x-clients-be.onrender.com")
db = EmployerTable("postgresql://x_clients_db_3fmx_user:mzoTw2Vp4Ox4NQH0XKN3KumdyAYE31uq@dpg-cour99g21fec73bsgvug-a.oregon-postgres.render.com/x_clients_db_3fmx")


def test_get_list():
    name = "My company"
    db.create_company(name)
    max_id = db.get_max_id_comp()

    api_result = api.get_employee_list(f'?company={max_id}')
    db_result = db.select_employers(max_id)
    db.delete_company(max_id)
    assert len(api_result) == len(db_result)


def test_add_new_employer():
    db.create_company('Моя компания')
    max_id_c = db.get_max_id_comp()

    api_result_b = api.get_employee_list(f'?company={max_id_c}')
    db_result_b = db.select_employers(max_id_c)

    f_name = 'Иван'
    l_name = 'Петров'
    phone = '+79969598584'

    db.create_employer(max_id_c, f_name, l_name, phone)

    api_result_a = api.get_employee_list(f'?company={max_id_c}')
    db_result_a = db.select_employers(max_id_c)

    assert len(api_result_b) == len(db_result_b)
    assert len(api_result_a) == len(db_result_a)
    assert len(db_result_a) - len(db_result_b) == 1
    for employee in api_result_a:
        if api_result_a == employee["id"]:
            assert employee["first_name"] == f_name
            assert employee["last_name"] == l_name
            assert employee["phone"] == phone
            assert employee["company_id"] == max_id_c

    db.clear_table_employers(max_id_c)
    db.delete_company(max_id_c)


def test_one_employer():
    db.create_company('Моя компания')
    max_id_c = db.get_max_id_comp()

    name_emp = 'Иван'
    la_name = 'Петров'
    phone_num = '+79969598584'

    db.create_employer(max_id_c, name_emp, la_name, phone_num)
    max_id_e = db.get_max_id_emp(max_id_c)
    db_result = db.get_employer_by_id(max_id_e)

    assert db_result["firstName"] == name_emp
    assert db_result["lastName"] == la_name
    assert db_result["companyId"] == max_id_c
    assert db_result["phone"] == phone_num

    db.clear_table_employers(max_id_c)
    db.delete_company(max_id_c)


def test_change_data():
    db.create_company('Моя компания')
    max_id_c = db.get_max_id_comp()

    name_emp = 'Иван'
    la_name = 'Петров'
    phone_num = '+79969598584'

    db.create_employer(max_id_c, name_emp, la_name, phone_num)
    max_id_e = db.get_max_id_emp(max_id_c)
    

    id = max_id_e
    last_name = 'Белов'
    email = 'test@mail.com'
    url = 'https://my_profile.com'
    phone = '89654789654'
    is_active = True
    my_headers = {"x-client-token": api.get_token()}
    resp = api.change_data(id, last_name, email, url, phone, is_active, headers=my_headers)

    employer_body = api.get_employer(max_id_e)

    assert employer_body["id"] == max_id_e
    assert employer_body["isActive"] == is_active
    assert employer_body["email"] == email
    assert employer_body["url"] == url

    db.clear_table_employers(max_id_c)
    db.delete_company(max_id_c)


def test_delete_company_and_employers():
    name = 'Моя компания'
    db.create_company(name)
    max_id_c = db.get_max_id_comp()

    name_emp = 'Иван'
    la_name = 'Петров'
    phone_num = '+79969598584'

    db.create_employer(max_id_c, name_emp, la_name, phone_num)
    db.clear_table_employers(max_id_c)
    api_result = api.get_employee_list(f'?company={max_id_c}')
    assert len(api_result) == 0
    deleted = db.delete_company(max_id_c)

    assert len(api_result) != 0
    assert deleted["id"] == max_id_c
    assert deleted["name"] == name
    assert deleted["isActive"] == True

    rows = api.get_company_by_id(max_id_c)
    assert len(rows) == 0