import json

class ToDoList:
    def __init__(self, to_do_file):
        self.to_do_file = to_do_file
        self.title_list = self.get_title()
        self.status_list = self.get_status()
        self.task = self.get_task()

    def get_list(self):
        with open(self.to_do_file, "r") as _f:
            tasks = json.load(_f)
        val = [value for key, value in tasks.items() if key == "value"]
        titles = val[0]
        return titles

    def get_title(self):
        titles = self.get_list()
        title_list = [title["title"] for title in titles if title["status"]]
        # title_list = [title["title"] for title in titles if title["status"] != "completed"]
        # print(title_list)
        return title_list

    def get_status(self):
        bool_list = []
        titles = self.get_list()
        status_list = [status["status"] for status in titles]
        for complete in status_list:
            if complete == "notStarted":
                boolean = False
            else:
                boolean = True
            bool_list.append(boolean)
        # print(status_list)
        # print(bool_list)
        return status_list
        # return bool_list

    def get_task(self):
        # new_dic = dict(zip(self.title_list, self.status_list))
        # new_dic = {self.title_list[i] : self.status_list[i] for i in range(len(self.title_list))}
        new_dic = {key: value for (key, value) in zip(self.title_list, self.status_list)}

        return new_dic

# td = ToDoList("../static/ricorda_di_task.json")
# td.get_title()