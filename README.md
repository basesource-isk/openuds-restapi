# Подключение к серверу

Для подключения к серверу используется функция `login()`, для отключения `logout()`.

В `rest.py` необходимо задать URL для обращения к API брокера:

```python
rest_url = 'http://vdi.broker.ip_or_fqdn/uds/rest/'
```

и реквизиты пользователя для подключения (имя аутентификатора, настроенного в брокере, пользователь и пароль), например для пользователя user, созданного в аутентификаторе internal:

```python
def login():
...
    parameters = '{ "auth": "internal", "username": "user", "password": "..." }'
...
```

Необходимо использовать учетную запись, отличную от встроенного администратора root.

Примеры возвращаемых результатов неудачной и удачной аутентификации:

```
{'result': 'error', 'token': None, 'version': '3.0.0', 'error': 'Invalid credentials'}
```

```
{'result': 'ok', 'token': 'token_value', 'version': '3.0.0', 'scrambler': 'scrambler_value'}
```

# Получение информации об объектах

## Пулы и базовые сервисы

* `request_pools()` - получение списка сервис-пулов и их параметров в формате JSON

Пример выдачи по сервис-пулу:

```
{
'id': '77b03fd5-4398-5fca-ac1c-36c4f9788a62', 
'name': 'AltLinux', 
'short_name': '', 
'tags': [], 
'parent': 'AltLinux', 
'parent_type': 'oVirtLinkedService', 
'comments': '', 
'state': 'A', 
'thumb': '', 
'account': '', 
'account_id': None, 
'service_id': 'ee27235f-59c3-5407-b897-d1c9a7ed84e0', 
'provider_id': 'e940cfb5-99ea-5c0b-b003-b932743bcfbc', 
'image_id': '6cde7570-9ed4-53d5-b6ce-1725ac016e90', 
'initial_srvs': 1, 
'cache_l1_srvs': 0, 
'cache_l2_srvs': 0, 
'max_srvs': 5, 
'show_transports': True, 
'visible': True, 
'allow_users_remove': False, 
'allow_users_reset': False, 
'ignores_unused': False, 
'fallbackAccess': 'ALLOW', 
'meta_member': [], 
'calendar_message': '', 
'user_services_count': 2, 
'user_services_in_preparation': 0, 
'restrained': False, 
'permission': 96, 
'info': {'icon': '', 
    'needs_publication': True, 
    'max_deployed': -1, 
    'uses_cache': True, 
    'uses_cache_l2': True, 
    'cache_tooltip': 'Number of desired machines to keep running waiting for a user', 
    'cache_tooltip_l2': 'Number of desired machines to keep suspended waiting for use', 
    'needs_manager': True, 
    'allowedProtocols': ['rdp', 'rgs', 'vnc', 'nx', 'x11', 'x2go', 'pcoip', 'other', 'spice'], 
    'servicesTypeProvided': ['vdi'], 
    'must_assign_manually': False, 
    'can_reset': True, 
    'can_list_assignables': False}, 
'pool_group_id': 'cd6310e3-681e-57bd-b70f-919bb7753dd5', 
'pool_group_name': 'Desktops', 
'pool_group_thumb': '', 
'usage': '40%', 
'osmanager_id': '6a2c5205-b888-5e7b-83eb-8fc32787e718'}
```

* `request_service_info(provider_id, service_id)` - получение списка базовых сервисов и их параметров в формате JSON, в качестве параметров передается id сервис-провайдера и соответствующего базового сервиса.

Пример выдачи по базовому сервису:

```
{'id': 'ee27235f-59c3-5407-b897-d1c9a7ed84e0', 
'name': 'AltLinux', 
'tags': [], 
'comments': '', 
'type': 'oVirtLinkedService', 
'type_name': 'oVirt/RHEV Linked Clone', 
'proxy_id': '-1', 
'proxy': '', 
'deployed_services_count': 1, 
'user_services_count': 2, 
'maintenance_mode': False, 
'permission': 96, 
'info': {'icon': '', 
    'needs_publication': True, 
    'max_deployed': -1, 
    'uses_cache': True, 
    'uses_cache_l2': True, 
    'cache_tooltip': 'Number of desired machines to keep running waiting for a user', 
    'cache_tooltip_l2': 'Number of desired machines to keep suspended waiting for use', 
    'needs_manager': True, 
    'allowedProtocols': ['rdp', 'rgs', 'vnc', 'nx', 'x11', 'x2go', 'pcoip', 'other', 'spice'], 
    'servicesTypeProvided': ['vdi'], 
    'must_assign_manually': False, 
    'can_reset': True, 
    'can_list_assignables': False}, 
'cluster': '2fc3ea8e-09fc-11eb-9975-00163e407f78', 
'datastore': 'f2fa7c22-5070-4697-9c90-3299b2d0f21e', 
'minSpaceGB': '20', 
'machine': '20e96e07-759a-4cb5-bbc5-76016573dece', 
'memory': '2048', 
'memoryGuaranteed': '2048', 
'usb': 'native', 
'display': 'spice', 
'baseName': 'vdi3-alt-', 
'lenName': '2', 
'ov': '', 
'ev': 't-provider-1'}
```

## Аутентификаторы, группы и пользователи

`get_auths()` - получение списка созданных аутентификаторов, пример выдачи:

```
{
'numeric_id': 1, 
'id': '5606e35b-ac7f-5dc3-898c-0530f015777a', 
'name': 'hostco.ru', 
'tags': [], 
'comments': '', 
'priority': 1, 
'visible': True, 
'small_name': 'ad', 
'users_count': 5, 
'type': 'ActiveDirectoryAuthenticator', 
'type_name': 'Active Directory Authenticator', 
'type_info': {'canSearchUsers': True, 'canSearchGroups': True, 'needsPassword': False, 'userNameLabel': 'User name', 'groupNameLabel': 'Group name', 'passwordLabel': 'Password', 'canCreateUsers': True, 'isExternal': True}, 
'permission': 96
}, 
```

`get_groups(auth_id)` - получение списка созданных групп в аутентификаторе, в качестве параметра передается id аутентификатора, пример выдачи:

```
{
'id': '5265d98e-6067-5c6d-b464-261717d6c0b7', 
'name': 'demo', 
'comments': '', 
'state': 'A', 
'type': 'group', 
'meta_if_any': False
}
```

`get_users(auth_id)` - получение списка созданных пользователей в аутентификаторе, в качестве параметра передается id аутентификатора, пример выдачи:

```
{
'name': 'vdiuser', 
'real_name': 'vdiuser', 
'comments': '', 
'state': 'A', 
'staff_member': False, 
'is_admin': False, 
'last_access': 1603712668, 
'parent': None, 
'id': 'e954f545-4870-5da2-8a95-271c0e930d3f', 
'role': 'User'
}
```

## Транспорты (протоколы подключения)

`get_transports()` - получение списка созданных транспортов, пример выдачи:

```
{
'id': '69a2a306-65da-5cc0-8f75-21345192872d', 
'name': 'SpiceDirect', 
'tags': [], 
'comments': '', 
'priority': 3, 
'nets_positive': True, 
'networks': [], 
'allowed_oss': [], 
'pools': [{'id': '77b03fd5-4398-5fca-ac1c-36c4f9788a62'}, {'id': '95e4c1bf-c4b4-59b8-9089-a05ab3140c56'}, {'id': '68d717be-8998-5bf0-afe5-9b5e8d1df9eb'}, {'id': '117349d8-3d79-58e2-bcef-52ba56c46734'}, {'id': '55be0bf2-a2d5-51b2-8da1-81e56de214e3'}, {'id': '019ad9f9-24fb-502b-9b71-e0e6557cbc32'}], 
'pools_count': 6, 
'deployed_count': 6, 
'type': 'SPICETransport', 
'type_name': 'SPICE', 
'protocol': 'spice', 
'permission': 96}, 
```

# Взаимодействие с сервис-пулами

## Создание пула

`create_pool(poolname, service_id, osmanager_id)` - создание нового пула, в качестве минимального набора параметров необходимо передать имя пула, id базового сервиса и менеджера ОС (должны быть заведены в через web-интерфейс брокера VDI).

Получить перечень базовых сервисов, менеджеров ОС и их id в формате JSON можно с помощью функций:

`request_base_services()`

Пример выдачи:

```
[
{
'id': 'ee27235f-59c3-5407-b897-d1c9a7ed84e0', 
'name': 'AltLinux', 
'tags': [], 
'comments': '', 
'type': 'oVirtLinkedService', 
'type_name': 'oVirt/RHEV Linked Clone', 
'proxy_id': '-1', 
'proxy': '', 
'deployed_services_count': 2, 
'user_services_count': 2, 
'maintenance_mode': False, 
'permission': 96, 
'info': {'icon': '...', 'needs_publication': True, 'max_deployed': -1, 'uses_cache': True, 'uses_cache_l2': True, 'cache_tooltip': 'Number of desired machines to keep running waiting for a user', 'cache_tooltip_l2': 'Number of desired machines to keep suspended waiting for use', 'needs_manager': True, 'allowedProtocols': ['rdp', 'rgs', 'vnc', 'nx', 'x11', 'x2go', 'pcoip', 'other', 'spice'], 'servicesTypeProvided': ['vdi'], 'must_assign_manually': False, 'can_reset': True, 'can_list_assignables': False}
}, 
... 
]
```

`request_osmanagers()`

Пример выдачи:

```
[
{'id': '6a2c5205-b888-5e7b-83eb-8fc32787e718', 'name': 'Linux', 'tags': [], 'deployed_count': 6, 'type': 'LinuxManager', 'type_name': 'Linux OS Manager', 'servicesTypes': ['vdi'], 'comments': '', 'permission': 96}, 
{'id': '05dc012f-1ab8-51f4-9fce-b321f5945b64', 'name': 'WinBasic', 'tags': [], 'deployed_count': 1, 'type': 'WindowsManager', 'type_name': 'Windows Basic OS Manager', 'servicesTypes': ['vdi'], 'comments': '', 'permission': 96}]

```

### Перечень передаваемых параметров при создании пула:

* обязательные

```
        'name': имя пула
        'service_id': id базового сервиса
        'osmanager_id': id менеджера ос
```

* необязательные (аналогичны параметрам в GUI на соответствующих вкладках)
```
#main:
        'short_name':'',
        'comments':'',
        'tags':[''],
#display:
        'image_id':None,
        'pool_group_id':None,
        'visible':True,
        'calendar_message':''
#advanced:
        'allow_users_remove':False,
        'allow_users_reset':False,
        'ignores_unused':False,
        'show_transports':True,
        'account_id':None,
#availability:
        'initial_srvs':'0',
        'cache_l1_srvs':'0',
        'cache_l2_srvs':'0',
        'max_srvs':'0',
```

## Удаление пула

`delete_pool(pool_id)` - удаление пула, в качестве параметра необходимо передать id пула.

Получить id пула можно с помощью описанной выше функции `request_pools()` либо при создании нового в выводе функции `create_pool`.

## Изменение параметров пула

`modify_pool(pool_id, max_services)` - изменение параметров пула, в качестве примера для демонстрации реализовано изменение максимального количества ВРС в пуле, передаваемые параметры - id пула и новое значение максимального количества ВРС в пуле.

Получить id пула можно с помощью описанной выше функции `request_pools()` либо при создании нового в выводе функции `create_pool`.

Перечень параметров для редактирования аналогичен списку при создании пула, за исключением:
- service_id
- osmanager_id

Данные параметры для созданного пула не редактируются.

## Публикация

`publish_pool(pool_id)` - публикация сервисов пула, требуется при изменении базового ("золотого") образа ВМ, для развертывания клонов на основе новой версии, в качестве параметра необходимо передать id пула.

Получить id пула можно с помощью описанной выше функции `request_pools()` либо при создании нового в выводе функции `create_pool`.

В случае успешного запуска процесса публикации функция возвращает ответ `ok`.

## Получение информации об объектах пула

`get_pool_groups(pool_id)` - получение списка добавленных в пул групп, в качестве параметра необходимо передать id пула, пример выдачи:

```
{
'id': '5265d98e-6067-5c6d-b464-261717d6c0b7', 
'auth_id': '8052211e-29a1-54b8-99e6-230dd715a61a', 
'name': 'demo', 
'group_name': 'demo@internal', 
'comments': '', 
'state': 'A', 
'type': 'group', 
'auth_name': 'internal'}
```

`get_pool_transports(pool_id)` - получение списка добавленных в пул транспортов (протоколов подключения), в качестве параметра необходимо передать id пула, пример выдачи:

```
{
'id': '69a2a306-65da-5cc0-8f75-21345192872d', 
'name': 'SpiceDirect', 
'type': {'name': 'SPICE', 'type': 'SPICETransport', 'description': 'SPICE Protocol. Direct connection.', 'icon': '', 'group': 'Direct'}, 
'comments': '', 
'priority': 3, 
'trans_type': 'SPICE'}
```

`get_pool_assigned_services(pool_id)` - получение списка сервисов пула (тонких клонов, виртуальных машин, и т.д.), назначенных пользователям (закрепленных за ними). В качестве параметра необходимо передать id пула, пример выдачи:

```
{
'id': '5fbf9f49-c852-5342-aa75-3238b83638ce', 
'id_deployed_service': '77b03fd5-4398-5fca-ac1c-36c4f9788a62', 
'unique_id': '52:54:00:00:00:4B', 
'friendly_name': 'vdi3-alt-66', 
'state': 'U', 
'os_state': 'U', 
'state_date': 1622222828, 
'creation_date': 1621607895, 
'revision': 3, 
'ip': '10.1.2.21', 
'actor_version': '2.2.0', 
'owner': 'user@hostco.ru', 
'owner_info': {'auth_id': '5606e35b-ac7f-5dc3-898c-0530f015777a', 'user_id': 'e7640c91-c1bc-58bc-8aeb-4fd77fdbf5cc'}, 
'in_use': False, 
'in_use_date': 1622224823, 
'source_host': '10.1.1.5', 
'source_ip': '10.1.1.5'
}
```

`get_pool_cached_services(pool_id)` - получение списка сервисов пула, находящихся в кэше (развернутые, но не назначенные пользователям экземпляры). В качестве параметра необходимо передать id пула, пример выдачи:

```
{
'id': 'b2b9c5ba-0943-58f3-ba06-05b0c2738028', 
'id_deployed_service': '9a801202-eb99-5f75-9137-c64aad365e1f', 
'unique_id': '52:54:00:00:00:01', 
'friendly_name': 'vdi3-alt-00', 
'state': 'U', 
'os_state': 'U', 
'state_date': 1631271805, 
'creation_date': 1631271750, 
'revision': 3, 
'ip': '10.1.2.13', 
'actor_version': '2.2.0', 
'cache_level': 1
}
```

## Добавление объектов в пул

`add_pool_groups(pool_id, group_id)` - добавление в пул группы доступа, в качестве параметров передаются id пула и группы.

`add_pool_transports(pool_id, transport_id)` - добавление в пул транспорта (протокола подключения), в качестве параметров передаются id пула и транспорта.

Получить id транспорта можно с помощью описанной выше функции `get_transports()`.

# Статус объектов

Перечень всех возможных статусов объектов VDI (параметр `state`).
Не все объекты поддерживают все статусы.

```
    'A' - Active
    'B' - Blocked
    'C' - Canceled
    'E' - Error
    'F' - Finished
    'H' - Balancing
    'I' - Inactive
    'J' - Too many preparing services
    'K' - Canceling
    'L' - Waiting publication
    'M' - Removing
    'P' - In preparation
    'R' - Removable
    'S' - Removed
    'T' - Restrained
    'U' - Valid
    'W' - Running
    'X' - Waiting execution
    'Y' - In maintenance
    'Z' - Waiting OS
    'V' - Meta member
```

# Примеры

В `rest.py` присутствуют примеры для следующего функционала:

- подключение к брокеру;
- получение списка сервис-пулов;
- получение списка базовых сервисов;
- получение списка менеджеров ОС;
- создание сервис пула;
- удаление сервис пула;
- редактирование пула, изменение максимального количества ВРС;
- публикация пула;
- отключение от брокера.
