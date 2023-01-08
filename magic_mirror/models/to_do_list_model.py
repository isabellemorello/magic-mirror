import json

class ToDoList:
    def __init__(self, to_do_file):
        self.to_do_file = to_do_file
        self.title_list = self.get_title()

    def get_title(self):
        with open(self.to_do_file, "r") as _f:
            tasks = json.load(_f)
        val = [value for key,value in tasks.items() if key == "value"]
        titles = val[0]
        title_list = [title["title"] for title in titles if title["status"] != "completed"]
        # print(title_list)
        return title_list


# td = ToDoList("../static/ricorda_di_task.json")
# td.get_title()