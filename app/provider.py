class ProviderNotConfigured(RuntimeError):
    pass

def fetch_segment_durations():
    """Interfaccia provider. Nessuna chiamata esterna finché provider/licenza non sono scelti."""
    from .config import TRAFFIC_PROVIDER
    if TRAFFIC_PROVIDER == "disabled":
        raise ProviderNotConfigured(
            "Provider disabilitato: scegliere una fonte e verificare licenza, storage e redistribuzione."
        )
    raise NotImplementedError(f"Provider non implementato: {TRAFFIC_PROVIDER}")
