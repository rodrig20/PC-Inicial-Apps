import requests


def python_versions():
    url = "https://www.python.org/downloads/release/python-3[]0/"
    min_version = 8
    versions_list = []
    while True:
        response = requests.head(url.replace("[]", str(min_version)))
        if response.status_code == 200:
            versions_list.append(f"3.{min_version}")
        else:
            break

        min_version += 1
        
    return versions_list

        