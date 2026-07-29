"""Low-level shell wrappers used by the diagnostic tools."""


import subprocess


def shell_ping(host):
    return subprocess.call(f"ping -c 1 {host}", shell=True)


def safe_ping(host):
    return subprocess.call(["ping", "-c", "1", host], timeout=5)
