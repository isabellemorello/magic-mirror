import json

class ToDoList:
    def __init__(self, to_do_file):
        self.to_do_file = to_do_file
        self.title_list = self.get_title()
        self.status_list = self.get_status()
        self.id_list = self.get_id()
        self.id_status_list = self.get_id_status()
        self.task = self.get_task()

    def get_list(self):
        # with open(self.to_do_file, "r") as _f:
        #     tasks = json.load(_f)
        tasks = self.to_do_file
        val = [value for key, value in tasks.items() if key == "value"]
        titles = val[0]
        return titles

    def get_title(self):
        titles = self.get_list()
        title_list = [title["title"] for title in titles if title["status"]]
        # title_list = [title["title"] for title in titles if title["status"] != "completed"]
        return title_list

    def get_status(self):
        titles = self.get_list()
        status_list = [status["status"] for status in titles]
        return status_list

    def get_id(self):
        list = self.get_list()
        id_list = [id["id"] for id in list]
        return id_list

    def get_id_status(self):
        new_list = []
        id_list = self.get_id()
        status_list = self.get_status()
        for id in id_list:
            for status in status_list:
                new_list.append([id, status])
        return  new_list

    def get_task(self):
        # new_dic = dict(zip(self.title_list, self.status_list))
        # new_dic = {self.title_list[i] : self.status_list[i] for i in range(len(self.title_list))}
        new_dic = {key: value for (key, value) in zip(self.title_list, self.id_status_list)}

        return new_dic

# td = ToDoList("../static/routine_task.json")
# print(td.get_list())