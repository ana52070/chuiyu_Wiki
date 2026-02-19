import requests

resp = requests.get(
    "https://generativelanguage.googleapis.com/v1beta/models?key=AIzaSyDmC78TNWJy_9F4KHzr_JOPDnLHgLjQtk0",
    proxies={"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
)
print(resp.json())