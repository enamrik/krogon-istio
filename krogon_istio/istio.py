import krogon_istio.maybe as M
from typing import List


def gateway_host(service_name: str, host: str):
    return IstioServiceTemplate(service_name, host)


class IstioServiceTemplate:
    def __init__(self, name: str, host: str):
        self.name = name
        self.service_name = name
        self.host = host
        self.port: M.Maybe[int] = M.nothing()
        self.gateway_name = 'cluster-gateway'
        self.dns_suffix = '.default.svc.cluster.local'
        self.retries: M.Maybe[dict] = M.nothing()

    def with_port(self, port: int):
        self.port = M.just(port)
        return self

    def with_service_name(self, service_name):
        self.service_name = service_name
        return self

    def with_dns_suffix(self, suffix):
        self.dns_suffix = suffix
        return self

    def with_retries(self,
                     attempts: int = 1,
                     per_try_timeout: str = '400ms',
                     retry_on: str = 'gateway-error,connect-failure,refused-stream'):
        self.retries = M.just({
            'attempts': attempts,
            'perTryTimeout': per_try_timeout,
            'retryOn': retry_on
        })
        return self

    def run(self) -> List[dict]:
        return [{
            'apiVersion': 'networking.istio.io/v1alpha3',
            'kind': 'VirtualService',
            'metadata': {'name': self.name},
            'spec': {
                'hosts': [self.host],
                'gateways': [self.gateway_name],
                'http': M.nlist([
                    M.nmap({
                        'route': [{
                            'destination': M.nmap({
                                'host': '{}{}'.format(self.service_name, self.dns_suffix)
                            }).append_if_value(
                                'port', M.map(self.port, (lambda x: {'number': x}))).to_map()
                        }]}).append_if_value(
                        'retries', self.retries).to_map(),
                ]).to_list()
            }
        }]
