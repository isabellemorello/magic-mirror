import requests
import json
# import microsoft_to_do_list.ms_graph_token as gtk


def app_to_do(activities_path, routine_path, ricorda_path):
# def app_to_do(generate_access_token, activities_path, routine_path, ricorda_path):
    # APP_ID = "3cbbf696-950d-41d6-b1b6-b6e3ccbe4c86"
    # SCOPES = ["Tasks.ReadWrite"]

    # access_token = generate_access_token
    # print(access_token)

    # with open("api_token_access.json", "r") as data:
    #     access_token = json.load(data)

    access_token = "EwCAA8l6BAAUkj1NuJYtTVha+Mogk+HEiPbQo04AASLSo7EbAfTS542Un4jdABfutTHzy5iImTgor4sSNKFglfN8tWMs3lRQ1v3JEkCOp2FWCEmGU4fUFKi50V9jcxIUIwDdA1q8qCiKIKX1KGN29psxJN5wGhAJOrVzya1rPGmev4vpkJH2TqN+Y1QCOE6Bt+E3CXSL4rNTcx74Oco7QSd8b16B5ZvDw4nc5El0IKrr/JUUQaS04VYZg5b4n1ooCXkmPofJFVWFHbt1RgfPo+Q5FtsXqarawrLQrP4AAfvnszW99DU+MVTWWgOH5TIMeyd/NwhUyS0k7Fzd133kxDwzjV56F5Bdve/QGuTwODOcZxEwXPkpkaKHb9zRiy4DZgAACCbyNKCd8uweUALoDzhfbS1LmyLf9oOX4+S3jOZ9qcef0vnOlJMLPBN6kLQfIfW/9xGEF7hJkTbLsR6AKT9q3mupCitDDXQpg/smJnnakmjJKcbRGiot2NlGB7T1m7Qa37HT5L97nPUNKrS+8oEPG3XIPzp8ysK1FHDzCBCdYDb3D8OO34S5F4+MBmnXKr/pkh963Cm9OQyKUEOrKDeeVMTLfJSdz22AEBHocE6A6X4kCdwGxq/9p6VvNjbGHosOh82XU3OqjMftSbJ/Oxwzdi1TkPzRrm+NpHYfnSxett5/bzFltLdJQCGF3GQPgciE20zAge7Ns14Zj1M54WaI0NBUj0IaQ7rAESPykD9+bXZF7lQS6Xor+Mss7s48ikwqBrA1MS2JBov7pchbj7QR9duJ9JHKFRu+sWGPI7XngPcLg+dbhcnygaL1SadAhj4hTekAom8rBvtP41eaNSh0P+U5iCLCOicxgfAy1BooA/fw0WYN4juKKUfnm7iJBghh8muRkZ8W1PltqWWeoOQ1O7BXJD9Iv8H0+O5JCpCIlbqAy2hJR3KpSRCovNo1HpXflZGbbrsbeQy+DrXe4Kr0h0MIIV0vHTGlREiyz/yZq7qbbuRAYIUDf+k+ee/YQWotpXWvNpdY/qjxXnLYaKGePr+3NpawHNQoI7a6WlzT/PY4pug0r1vyoptgeBQHDzhe9YoushAgsgSzJaRREWLNUxW1R7MslwZ1s+N+YEPy192a0N+63ZoZD2cw+ePU4CB3d6V6lCeNxpTlHp2RTc6RV44eDlECmGoz4Df4kQI="

    headers = {
        "Authorization": "Bearer " + access_token
        # "Authorization": "Bearer " + access_token["access_token"]
    }
    # print(type(secret))

    GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0"
    endpoint = GRAPH_ENDPOINT + "/me/todo/lists"

    response = requests.get(url=endpoint, headers=headers)
    activities = response.json()
    if response.status_code == 200:
        with open(activities_path, "w") as _f:
            json.dump(activities, _f, indent=4)
    else:
        response.raise_for_status()


    # GET /me/todo/lists/{todoTaskListId}/tasks
    # GET /users/users('isabelle.morello%40hotmail.it')/todo/lists/{todoTaskListId}/tasks
    id_routine_task = "AQMkADAwATZiZmYAZC05ZjdhLTE0MDUtMDACLTAwCgAuAAADyoocA6ILdkibyhRV60QQSgEAnjhde16bqkSW8aNr2iTlhgAF5RnMJAAAAA=="
    endpoint_routine_task = f"https://graph.microsoft.com/v1.0/me/todo/lists/{id_routine_task}/tasks"
    response_routine = requests.get(url=endpoint_routine_task, headers=headers)
    print(f"Status: {response_routine.status_code}")
    if response_routine.status_code == 200:
        routine_task = response_routine.json()
        print(routine_task)
        with open(routine_path, "w") as _f:
            json.dump(routine_task, _f, indent=4)
    else:
        print(response_routine.raise_for_status())


    id_ricorda_task = "AQMkADAwATZiZmYAZC05ZjdhLTE0MDUtMDACLTAwCgAuAAADyoocA6ILdkibyhRV60QQSgEAnjhde16bqkSW8aNr2iTlhgAF5wjd2AAAAA=="
    endpoint_ricorda_task = f"https://graph.microsoft.com/v1.0/me/todo/lists/{id_ricorda_task}/tasks"
    response_ricorda = requests.get(url=endpoint_ricorda_task, headers=headers)
    print(f"Status: {response_ricorda.status_code}")
    if response_ricorda.status_code == 200:
        ricorda_task = response_ricorda.json()
        print(ricorda_task)
        with open(ricorda_path, "w") as _f:
            json.dump(ricorda_task, _f, indent=4)
    else:
        print(response_routine.raise_for_status())


if __name__ == "__main__":
    app_to_do("../static/activities.json", "../static/routine_task.json", "../static/ricorda_di_task.json")
    # app_to_do(gtk.generate_access_token("api_token_access.json"), "../static/activities.json", "../static/routine_task.json", "../static/ricorda_di_task.json")