import yaml

# TODO добавить проверку на неверную конфигурацию
# TODO придумать еще конфигов

class Config:

    sync_paths = {}
    tokens = {}

    def __init__(self, config_filename: str = "config.yml"):
        self.config_filename = config_filename

    def load_config(self):
        config = self.__read_file()
        self.sync_paths = config["sync_path"]
        self.tokens = config["tokens"]

    # def get_services(self):
    #     services = []
    #     for i in self.sync_path:


    def __read_file(self):

        with open(self.config_filename, 'r') as file:
            config = yaml.safe_load(file)

        return config
