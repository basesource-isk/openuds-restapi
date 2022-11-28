# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from httplib2 import Http
import json
import sys

rest_url = ''

headers = {}

def login():
    global headers
    h = Http()
    parameters = '{ "auth": "", "username": "", "password": "" }'
    resp, content = h.request(rest_url + 'auth/login', method='POST', body=parameters)
    if resp['status'] != '200':  # Authentication error due to incorrect parameters, bad request, etc...
        print("Authentication error")
        return -1
    # resp contains the headers, content is json with the contents of response (in text format)
    res = json.loads(content)
    print(res)
    if res['result'] != 'ok':  # Authentication error
        print("Authentication error")
        return -1
    headers['X-Auth-Token'] = res['token']
    return 0

def logout():
    global headers
    h = Http()
    resp, content = h.request(rest_url + 'auth/logout', headers=headers)
    if resp['status'] != '200':  # Logout error due to incorrect parameters, bad request, etc...
        print("Error requesting logout")
        return -1
    return 0

# получение списка сервис-пулов и их параметров
def request_pools():
    h = Http()
    resp, content = h.request(rest_url + 'servicespools/overview', headers=headers)
    if resp['status'] != '200':  # error due to incorrect parameters, bad request, etc...
        print("Error requesting pools")
        return {}
    return json.loads(content)

# получение списка базовых сервисов и их параметров
# PATH: /rest/providers/[provider_id]/services/[service_id]
def request_service_info(provider_id, service_id):
    h = Http()
    resp, content = h.request(rest_url + 'providers/{0}/services/{1}'.format(provider_id, service_id), headers=headers)
    if resp['status'] != '200':  # error due to incorrect parameters, bad request, etc...
        print("Error requesting pools: response: {}, content: {}".format(resp, content))
        return None
    return json.loads(content)

# get service_id
def request_base_services():
    h = Http()
    resp, content = h.request(rest_url + 'providers/allservices', headers=headers)
    if resp['status'] != '200':  # error due to incorrect parameters, bad request, etc...
        print("Error requesting base services\nresp:{}\ncontent:{}".format(resp, content))
        return {}
    return json.loads(content)

# get osmanager_id
def request_osmanagers():
    h = Http()
    resp, content = h.request(rest_url + 'osmanagers', headers=headers)
    if resp['status'] != '200':  # error due to incorrect parameters, bad request, etc...
        print("Error requesting osmanagers\nresp:{}\ncontent:{}".format(resp, content))
        return {}
    return json.loads(content)

# создание нового пула
def create_pool(poolname: str, service_id, osmanager_id):
    h = Http()
    data = {'name':poolname,'short_name':poolname,'comments':'','tags':[''],'service_id':service_id,'osmanager_id':osmanager_id,'image_id':None,'pool_group_id':None,'initial_srvs':'0','cache_l1_srvs':'0','cache_l2_srvs':'0','max_srvs':'1','show_transports':True,'visible':True,'allow_users_remove':False,'allow_users_reset':False,'ignores_unused':False,'account_id':None,'calendar_message':''}
    resp, content = h.request(rest_url + 'servicespools','PUT', headers=headers, body=json.dumps(data))
    if resp['status'] != '200':
        print("Error in request: \n-------------------\n{}\n{}\n----------------".format(resp, content))
        sys.exit(1)
    r = json.loads(content)
    print("Correctly created {} with id {}".format(r['name'], r['id']))
    print("The record created was: {}".format(r))
    return r

def delete_pool(pool_id):
    h = Http()
    # Method MUST be DELETE
    resp, content = h.request(rest_url + 'servicespools/{}'.format(pool_id), 'DELETE', headers=headers)
    if resp['status'] != '200':
        print("Error in request: \n-------------------\n{}\n{}\n----------------".format(resp, content))
        sys.exit(1)
    print("Correctly deleted {}".format(pool_id))

def modify_pool(pool_id, max_services: int):
    h = Http()
    resp, content = h.request(rest_url + 'servicespools/{}'.format(pool_id), headers=headers)
    if resp['status'] != '200':
        print("Error in request: \n-------------------\n{}\n{}\n----------------".format(resp, content))
        sys.exit(1)
    data = json.loads(content)
    data['max_srvs'] = max_services
    resp, content = h.request(rest_url + 'servicespools/{}'.format(pool_id), 'PUT', headers=headers, body=json.dumps(data))
    if resp['status'] != '200':
        print("Error in request: \n-------------------\n{}\n{}\n----------------".format(resp, content))
        sys.exit(1)
    r = json.loads(content)
    print("Successfully modified pool id: {} with data:\n{}".format(pool_id, r))
    return r

# публикация пула
def publish_pool(pool_id):
    h = Http()
    resp, content = h.request(rest_url + 'servicespools/{}/publications/publish'.format(pool_id), headers=headers)
    if resp['status'] != '200':
        print("Error in request: \n-------------------\n{}\n{}\n----------------".format(resp, content))
        sys.exit(1)
    data = json.loads(content)
    print(data)
    return data

def get_auths():
    h = Http()
    resp, content = h.request(rest_url + 'authenticators', headers=headers)
    if resp['status'] != '200':
        print("Error in request: \n-------------------\n{}\n{}\n----------------".format(resp, content))
        sys.exit(1)
    r = json.loads(content)
    return r

def get_groups(auth_id):
    h = Http()
    resp, content = h.request(rest_url + 'authenticators/{}/groups'.format(auth_id), headers=headers)
    if resp['status'] != '200':
        print("Error in request: \n-------------------\n{}\n{}\n----------------".format(resp, content))
        sys.exit(1)
    r = json.loads(content)
    return r

def get_users(auth_id):
    h = Http()
    resp, content = h.request(rest_url + 'authenticators/{}/users'.format(auth_id), headers=headers)
    if resp['status'] != '200':
        print("Error in request: \n-------------------\n{}\n{}\n----------------".format(resp, content))
        sys.exit(1)
    r = json.loads(content)
    return r

def get_transports():
    h = Http()
    resp, content = h.request(rest_url + 'transports', headers=headers)
    if resp['status'] != '200':
        print("Error in request: \n-------------------\n{}\n{}\n----------------".format(resp, content))
        sys.exit(1)
    r = json.loads(content)
    return r

def get_pool_groups(pool_id):
    h = Http()
    resp, content = h.request(rest_url + 'servicespools/{}/groups'.format(pool_id), headers=headers)
    if resp['status'] != '200':
        print("Error in request: \n-------------------\n{}\n{}\n----------------".format(resp, content))
        sys.exit(1)
    r = json.loads(content)
    return r

def get_pool_transports(pool_id):
    h = Http()
    resp, content = h.request(rest_url + 'servicespools/{}/transports'.format(pool_id), headers=headers)
    if resp['status'] != '200':
        print("Error in request: \n-------------------\n{}\n{}\n----------------".format(resp, content))
        sys.exit(1)
    r = json.loads(content)
    return r

def add_pool_groups(pool_id, group_id):
    h = Http()
    data = {'id':group_id}
    resp, content = h.request(rest_url + 'servicespools/{}/groups'.format(pool_id), 'PUT', headers=headers, body=json.dumps(data))
    if resp['status'] != '200':
        print("Error in request: \n-------------------\n{}\n{}\n----------------".format(resp, content))
        sys.exit(1)
    print("Successfully added group {} for pool {}".format(group_id, pool_id))

def add_pool_transports(pool_id, transport_id):
    h = Http()
    data = {'id':transport_id}
    resp, content = h.request(rest_url + 'servicespools/{}/transports'.format(pool_id), 'PUT', headers=headers, body=json.dumps(data))
    if resp['status'] != '200':
        print("Error in request: \n-------------------\n{}\n{}\n----------------".format(resp, content))
        sys.exit(1)
    print("Successfully added transport {} for pool {}".format(transport_id, pool_id))

def get_pool_assigned_services(pool_id):
    h = Http()
    resp, content = h.request(rest_url + 'servicespools/{}/services'.format(pool_id), headers=headers)
    if resp['status'] != '200':
        print("Error in request: \n-------------------\n{}\n{}\n----------------".format(resp, content))
        sys.exit(1)
    r = json.loads(content)
    return r

def get_pool_cached_services(pool_id):
    h = Http()
    resp, content = h.request(rest_url + 'servicespools/{}/cache'.format(pool_id), headers=headers)
    if resp['status'] != '200':
        print("Error in request: \n-------------------\n{}\n{}\n----------------".format(resp, content))
        sys.exit(1)
    r = json.loads(content)
    return r



if __name__ == '__main__':
    if login() == 0:  # If we can log in

# получить перечень сервис пулов и базовых сервисов
#        res = request_pools()
#        print(res)
#        for r in res:
#            print("Base Service info for pool {}: ".format(r['name']))
#            res2 = request_service_info(r['provider_id'], r['service_id'])
#            if res2 is not None:
#                print(res2)
#            else:
#                print("Base service for pool {} is not accesible".format(r['name']))

# получить перечень базовых сервисов
#        res = request_base_services()
#        print(res)

# получить перечень менеджеров ОС
#        res = request_osmanagers()
#        print(res)

# создание нового пула
#        create_pool('test_pool', 'ee27235f-59c3-5407-b897-d1c9a7ed84e0', '6a2c5205-b888-5e7b-83eb-8fc32787e718')

# удаление пула
#        delete_pool('aecab40f-a1ef-5cce-aec5-1fb4355a97d1')

# редактирование пула, изменение максимального количества ВРС
#        modify_pool('9a801202-eb99-5f75-9137-c64aad365e1f', 3)

# публикация пула
#        publish_pool('9a801202-eb99-5f75-9137-c64aad365e1f')

        print(logout())  # This will success
