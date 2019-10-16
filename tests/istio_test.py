from krogon_istio import gateway_host
from tests.assert_diff import assert_same_dict


def test_will_create_default_template():
    external_host = "some-dns-host"
    service_name = "service-name"
    gateway_name = "cluster-gateway"

    template = gateway_host(service_name, external_host)
    results = template.run()

    assert_same_dict(results[0], {
        'apiVersion': 'networking.istio.io/v1alpha3',
        'kind': 'VirtualService',
        'metadata': {'name': service_name},
        'spec': {
            'hosts': [external_host],
            'gateways': [gateway_name],
            'http': [
                {'route': [{
                    'destination': {
                        'host': "{}.default.svc.cluster.local".format(service_name)
                    }
                }]},
            ]
        }
    })


def test_will_set_service_dns_suffix():
    external_host = "some-dns-host"
    service_name = "service-name"
    gateway_name = "cluster-gateway"

    template = gateway_host(service_name, external_host)\
        .with_dns_suffix('.cool-namespace.svc.cluster.local')

    results = template.run()

    assert_same_dict(results[0], {
        'apiVersion': 'networking.istio.io/v1alpha3',
        'kind': 'VirtualService',
        'metadata': {'name': service_name},
        'spec': {
            'hosts': [external_host],
            'gateways': [gateway_name],
            'http': [
                {'route': [{
                    'destination': {
                        'host': "{}.cool-namespace.svc.cluster.local".format(service_name),
                    }
                }]},
            ]
        }
    })


def test_will_set_service_port():
    external_host = "some-dns-host"
    service_name = "service-name"
    gateway_name = "cluster-gateway"
    port = 8000

    template = gateway_host(service_name, external_host).with_port(port)
    results = template.run()

    assert_same_dict(results[0], {
        'apiVersion': 'networking.istio.io/v1alpha3',
        'kind': 'VirtualService',
        'metadata': {'name': service_name},
        'spec': {
            'hosts': [external_host],
            'gateways': [gateway_name],
            'http': [
                {'route': [{
                    'destination': {
                        'host': "{}.default.svc.cluster.local".format(service_name),
                        'port': {'number': port}
                    }
                }]},
            ]
        }
    })


def test_can_set_default_retries():
    external_host = "some-dns-host"
    service_name = "service-name"
    gateway_name = "cluster-gateway"
    port = 8000

    template = gateway_host(service_name, external_host).with_port(port)\
        .with_retries()

    results = template.run()

    assert_same_dict(results[0], {
        'apiVersion': 'networking.istio.io/v1alpha3',
        'kind': 'VirtualService',
        'metadata': {'name': service_name},
        'spec': {
            'hosts': [external_host],
            'gateways': [gateway_name],
            'http': [
                {
                    'route': [{
                        'destination': {
                            'host': "{}.default.svc.cluster.local".format(service_name),
                            'port': {'number': port}
                        },
                    }],
                    'retries': {
                        'attempts': 1,
                        'perTryTimeout': '400ms',
                        'retryOn': 'gateway-error,connect-failure,refused-stream'
                    }
                },
            ]
        }
    })


def test_can_set_retries():
    external_host = "some-dns-host"
    service_name = "service-name"
    gateway_name = "cluster-gateway"
    port = 8000

    template = gateway_host(service_name, external_host).with_port(port) \
        .with_retries(attempts=2)

    results = template.run()

    assert_same_dict(results[0], {
        'apiVersion': 'networking.istio.io/v1alpha3',
        'kind': 'VirtualService',
        'metadata': {'name': service_name},
        'spec': {
            'hosts': [external_host],
            'gateways': [gateway_name],
            'http': [
                {
                    'route': [{
                        'destination': {
                            'host': "{}.default.svc.cluster.local".format(service_name),
                            'port': {'number': port}
                        },
                    }],
                    'retries': {
                        'attempts': 2,
                        'perTryTimeout': '400ms',
                        'retryOn': 'gateway-error,connect-failure,refused-stream'
                    }
                },
            ]
        }
    })
