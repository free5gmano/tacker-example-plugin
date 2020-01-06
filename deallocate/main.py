from service_mapping_plugin_framework.deallocate_nssi_abc import DeallocateNSSIabc


class NFVOPlugin(DeallocateNSSIabc):
    def __init__(self, nm_host, nfvo_host):
        super().__init__(nm_host, nfvo_host)

    def terminate_network_service_instance(self):
        pass

    def delete_network_service_instance(self):
        pass

    def update_network_service_descriptor(self):
        pass

    def delete_network_service_descriptor(self):
        pass

    def update_vnf_package(self):
        pass

    def delete_vnf_package(self):
        pass


def main():
    nfvo_plugin = NFVOPlugin('',  # nm ip
                             '')  # os-ma-nfvo ip
    nfvo_plugin.deallocate_nssi()


if __name__ == '__main__':
    main()
