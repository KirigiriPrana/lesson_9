import requests


class EmployeeApi:

    def __init__(self,url):
        self.url = url

    def get_token(self, user='flora', password='nature-fairy'):
        creds = {
            'username': user,
            'password': password
        }
        resp = requests.post(self.url+'/auth/login',json=creds)
        return resp.json()["userToken"]

    def create_company(self, name, description=""):
        company = {
            "name": name,
            "description": description
        }
        my_headers = {}
        my_headers["x-client-token"] = self.get_token()
        resp = requests.post(self.url + '/company',
                             json=company, headers=my_headers)
        return resp.json()

    def get_employee_list(self, params_to_add=None):
        resp = requests.get(self.url + '/employee' + params_to_add)
        return resp.json()

    def create_employee(self, id, firstName, lastName, middleName,  companyId, email, url, phone, birthdate, isActive):
        employer = {
            "id": id,
            "firstName": firstName,
            "lastName": lastName,
            "middleName": middleName,
            "companyId": companyId,
            "email": email,
            "url": url,
            "phone": phone,
            "birthdate": birthdate,
            "isActive": isActive
        }
        my_headers = {}
        my_headers["x-client-token"] = self.get_token()
        resp = requests.post(self.url+'/employee',
                             json=employer, headers=my_headers)
        return resp.json()

    def get_employer(self, id):
        resp = requests.get(self.url + f'/employee/{id}')
        return resp.json()

    def change_data(self, id, lastName, email, url, phone, isActive):
        employer = {
            "lastName": lastName,
            "email": email,
            "url": url,
            "phone": phone,
            "isActive": isActive
        }

        my_headers = {}
        my_headers["x-client-token"] = self.get_token()
        resp = requests.patch(self.url + f'/employee/{id}',
                              json=employer, headers=my_headers)
        return resp.json()
    
    def get_company_by_id(self, id):
        resp = requests.get(self.url + f'/company/{id}')
        return resp.json()