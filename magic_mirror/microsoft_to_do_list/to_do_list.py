import requests
import json
# import ms_graph_token as gtk
import microsoft_to_do_list.ms_graph_token as gtk


# def app_to_do(secrets_path, activities_path, routine_path, ricorda_path):
def app_to_do(generate_access_token, secrets_path, activities_path, routine_path, ricorda_path):

    access_token = generate_access_token

    with open(secrets_path, "r") as data:
        secrets = json.load(data)

    headers = {
        # "Authorization": "Bearer " + secrets["MS_ACCESS_TOKEN"]
        "Authorization": "Bearer " + access_token["access_token"]
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
    id_routine_task = secrets["ID_ROUTINE_TASK"]
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


    id_ricorda_task = secrets["ID_RICORDA_DI_TASK"]
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
    # app_to_do("../secrets.json", "../static/activities.json", "../static/routine_task.json", "../static/ricorda_di_task.json")
    app_to_do(gtk.generate_access_token("api_token_access.json"), "../secrets.json", "../static/activities.json", "../static/routine_task.json", "../static/ricorda_di_task.json")