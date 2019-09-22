# Krogon-Istio

## Installation

```bash
pip install -e git+ssh://git@github.com/enamrik/krogon-istio.git#egg=krogon
```

## Usage

Example usage with a micro-service:

```python
from krogon import krogon
from krogon import config
from krogon.steps.k8s import run_in_cluster, micro_service
from krogon_istio import gateway_host

krogon(
    run_steps=[
        run_in_cluster(
            named='cool-cluster',
            templates=[
                micro_service(
                    name='cool-service',
                    image='gcr.io/prod-1/cool-service:1.0.0',
                    port=8000
                ),
                gateway_host(
                    'cool-service',
                    'coolness.sofree.com')
                    .with_dns_suffix('.cool-namespace.svc.cluster.local')
                    .with_port(8000)
            ])
    ],
    for_config=config()
)
```

