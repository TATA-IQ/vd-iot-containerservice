import json
import os


class ParseConfig(object):
    config_data = None

    def __init__(self):
        self.config_data = None

    @staticmethod
    def readFile(config_path="./config/config.json"):
        with open(config_path) as f:
            print(os.listdir("./"))
            ParseConfig.config_data = json.load(f)

    @staticmethod
    def getapi():
        print("<=====Parsing DB COnfig=====>")
        if ParseConfig.config_data is None:
            ParseConfig.readFile()
        else:
            return ParseConfig.config_data["api_list"]
        return ParseConfig.config_data["api_list"]
