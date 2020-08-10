from service_mapping_plugin_framework.deallocate_nssi_abc import DeallocateNSSIabc
from .params import *
import json
import time
import os
import requests


class NFVOPlugin(DeallocateNSSIabc):
    def __init__(self, nm_host, nfvo_host, subscription_host, parameter):
        super().__init__(nm_host, nfvo_host, subscription_host, parameter)
        # Don't devstack environment OS_AUTH_URL can't add 'identity'.
        self.OS_AUTH_URL = 'http://{}/identity'.format(nfvo_host.split(':')[0])
        self.TACKER_URL = 'http://{}'.format(nfvo_host)
        self.OS_USER_DOMAIN_NAME = OS_USER_DOMAIN_NAME
        self.OS_USERNAME = OS_USERNAME
        self.OS_PASSWORD = OS_PASSWORD
        self.OS_PROJECT_DOMAIN_NAME = OS_PROJECT_DOMAIN_NAME
        self.OS_PROJECT_NAME = OS_PROJECT_NAME
        self.ary_data = list()
        self.nsd_id = str()
        self.nsd_name = str()
        self.get_token_result = str()
        self.project_id = str()

    def get_token(self):
        # print("\nGet token:")
        self.get_token_result = ''
        get_token_url = self.OS_AUTH_URL + '/v3/auth/tokens'
        get_token_body = {
            'auth': {
                'identity': {
                    'methods': [
                        'password'
                    ],
                    'password': {
                        'user': {
                            'domain': {
                                'name': self.OS_USER_DOMAIN_NAME
                            },
                            'name': self.OS_USERNAME,
                            'password': self.OS_PASSWORD
                        }
                    }
                },
                'scope': {
                    'project': {
                        'domain': {
                            'name': self.OS_PROJECT_DOMAIN_NAME
                        },
                        'name': self.OS_PROJECT_NAME
                    }
                }
            }
        }
        get_token_response = requests.post(get_token_url, data=json.dumps(get_token_body))
        # print("Get OpenStack token status: " + str(get_token_response.status_code))
        self.get_token_result = get_token_response.headers['X-Subject-Token']
        return self.get_token_result

    def get_project_id(self, project_name):
        # print("\nGet Project ID:")
        self.project_id = ''
        get_project_list_url = self.OS_AUTH_URL + '/v3/projects'
        token = self.get_token()
        headers = {'X-Auth-Token': token}
        get_project_list_response = requests.get(get_project_list_url, headers=headers)
        # print("Get OpenStack project list status: " + str(get_project_list_response.status_code))
        get_project_list_result = get_project_list_response.json()['projects']
        for project in get_project_list_result:
            if project['name'] == project_name:
                self.project_id = project['id']
            pass
        # print("Project ID:" + self.project_id)
        return self.project_id

    def json_to_array(self, json_data):
        self.ary_data = []
        if len(json_data) > 0:
            for key, value in json_data.items():
                self.ary_data.append(value)
        return self.ary_data

    def coordinate_tn_manager(self):
        pass

    def terminate_network_service_instance(self):
        pass

    def delete_network_service_instance(self):
        print('\nDelete NS: ' + self.ns_instance)
        terminate_ns_url = self.TACKER_URL + '/v1.0/nss/{}'.format(self.ns_instance)
        token = self.get_token()
        headers = {'X-Auth-Token': token}
        response = requests.delete(terminate_ns_url, headers=headers)
        print('Delete NS status: ' + str(response.status_code))
        count = 0
        while 1:
            show_ns_url = self.TACKER_URL + '/v1.0/nss'
            res_show_ns = requests.get(show_ns_url, headers=headers).json()
            existed_status = 0
            for _ in res_show_ns['nss']:
                if _['id'] == self.ns_instance:
                    existed_status = 1
            if existed_status != 1:
                break
            time.sleep(1)
            count = count + 1
            print('wait ' + str(count) + 's')
        self.delete_network_service_descriptor()
        self.delete_vnf_package()

    def delete_network_service_instance_subscriptions(self):
        pass

    def update_network_service_descriptor(self):
        pass

    def delete_network_service_descriptor(self):
        print('\nDelete NSD: ' + self.ns_descriptor)
        delete_nsd_url = self.TACKER_URL + '/v1.0/nsds/{}'.format(self.ns_descriptor)
        token = self.get_token()
        headers = {'X-Auth-Token': token}
        response = requests.delete(delete_nsd_url, headers=headers)
        print('Delete NSD status: ' + str(response.status_code))

    def delete_network_service_descriptor_subscriptions(self):
        pass

    def update_vnf_package(self):
        pass

    def delete_vnf_package(self):
        print('\nDelete VNFP...')
        get_nsd_url = self.TACKER_URL + '/v1.0/vnfds'
        token = self.get_token()
        headers = {'X-Auth-Token': token}
        response = requests.get(get_nsd_url, headers=headers)
        for vnfp in response.json()['vnfds']:
            delete_nsd_url = self.TACKER_URL + '/v1.0/vnfds/{}'.format(vnfp['id'])
            response = requests.delete(delete_nsd_url, headers=headers)
            print('Delete VNFP status: ' + str(response.status_code))

    def delete_vnf_package_subscriptions(self):
        pass
