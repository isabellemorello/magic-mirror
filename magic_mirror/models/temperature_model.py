import json

class Temperature:
    def __init__(self, temp_file):
        self.temp_file = temp_file
        self.temperature = self.get_temperature()

    def get_temperature(self):
        with open(self.temp_file, "r") as _f:
            temp = json.load(_f)
        return temp


# td = Temperature("../static/temperature.json")
# print(td.get_temperature())