import os

class ResourcesPath:
    def __init__(self):
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
        self.path_to_audios = os.path.join(self.base_path, "Bot", "Resources", "Audios")
        self.path_to_images = os.path.join(self.base_path, "Bot", "Resources", "Images")
        self.path_to_databases = os.path.join(self.base_path, "Bot", "Resources", "DataBase")

        
    def __call__(self, type):
        match type.lower():
            case "audios" | "audio":
                return self.path_to_audios
            case "images" | "image":
                return self.path_to_images
            case "databases" | "database":
                return self.path_to_databases
            case _:
                raise ValueError(f"Resource type {type} is not recognized")