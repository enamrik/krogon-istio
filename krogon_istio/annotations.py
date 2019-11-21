from typing import Dict


def auto_inject_sidecar() -> Dict[str, str]:
    return {
        'traffic.sidecar.istio.io/excludeOutboundIPRanges': "0.0.0.0/0",
        "sidecar.istio.io/inject": "true"}

