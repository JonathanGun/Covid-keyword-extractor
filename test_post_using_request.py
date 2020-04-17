# import os
# import requests
# from typing import Dict, Any

# os.environ['NO_PROXY'] = '127.0.0.1'
# sent: Dict[str, Any] = {
#     "keywords": ["PDP", "ODP", "terkonfirmasi positif", "orang", "kasus positif"],
#     "texts": [],
#     "filenames": [],
#     "algorithm": "boyer-moore"  # or "kmp" or "regex" (default: "regex")
# }
# sent["texts"].append(requests.get('http://127.0.0.1:5000/sample/kompas1.txt').text)
# sent["texts"].append(requests.get('http://127.0.0.1:5000/sample/detik1.txt').text)
# r = requests.post('http://127.0.0.1:5000/extractor', data=sent)
# print(r.content.decode("utf-8"))
