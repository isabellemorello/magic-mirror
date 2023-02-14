import requests
import json
# from ..models.to_do_list_model import ToDoList
# import microsoft_to_do_list.ms_graph_token as gtk

def get_method(secrets_path, activities_path, path, task):
# def app_to_do(generate_access_token, activities_path, routine_path, ricorda_path):

    # access_token = generate_access_token

    with open(secrets_path, "r") as data:
        secrets = json.load(data)

    headers = {
        "Authorization": "Bearer " + secrets["MS_ACCESS_TOKEN"]
        # "Authorization": "Bearer " + access_token["access_token"]
    }

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
    id_task = secrets[task]
    endpoint_task = f"https://graph.microsoft.com/v1.0/me/todo/lists/{id_task}/tasks"
    response_task = requests.get(url=endpoint_task, headers=headers)
    print(f"Status: {response_task.status_code}")
    if response_task.status_code == 200:
        list_task = response_task.json()
        # print(list_task)
        with open(path, "w") as _f:
            json.dump(list_task, _f, indent=4)
        return list_task
    else:
        print(response_task.raise_for_status())



def patch_method(title, status_value, secrets_path, task, task_list):
    # access_token = generate_access_token(app_id=APP_ID, scopes=SCOPES)
    with open(secrets_path, "r") as data:
        secrets = json.load(data)
    task = task
    # with open(task_path, "r") as data:
    #     task = json.load(data)
    task_id = ""
    status = ""

    for k,v in task.items():
        if k == title:
            task_id = v[0]
            status = status_value
    print("ID:", task_id)
    headers = {
        "Authorization": "Bearer " + secrets["MS_ACCESS_TOKEN"],
        "Content-Type": "application/json"
    }
    data = {
        "status": status
    }
    id_task_list = secrets[task_list]
    endpoint_task = f"https://graph.microsoft.com/v1.0/me/todo/lists/{id_task_list}/tasks/{task_id}"
    response_task = requests.patch(url=endpoint_task, headers=headers, json=data )
    print(f"Status: {response_task.status_code}")

if __name__ == "__main__":
    pass
    # ricorda = get_method("../secrets.json", "../static/activities.json", "../static/ricorda_di_task.json", "ID_RICORDA_DI_TASK")
    # print(ricorda)
    # ricorda = get_method("../secrets.json", "../static/activities.json", "../static/ricorda_di_task.json", "ID_RICORDA_DI_TASK")
    # print(ricorda)
    # patch_method(title="Aggiungere colore eventi Google", status_value="completed", secrets_path="../secrets.json", task=ricorda, task_list="ID_RICORDA_DI_TASK")

    # app_to_do(gtk.generate_access_token("api_token_access.json"), "../static/activities.json", "../static/routine_task.json", "../static/ricorda_di_task.json")
