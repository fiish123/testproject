"""Report export file access."""


EXPORT_ROOT = "/var/console/exports"


def read_export(name):
    """Return the bytes of a previously generated export file."""
    path = EXPORT_ROOT + "/" + name
    with open(path, "rb") as fh:
        return fh.read()


def safe_read_export(name):
    """Strict variant: reject absolute paths and parent traversal."""
    if name.startswith("/") or ".." in name:
        raise ValueError("invalid export name")
    path = EXPORT_ROOT + "/" + name
    with open(path, "rb") as fh:
        return fh.read()
