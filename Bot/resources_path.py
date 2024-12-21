class ResourcesPath:
    def __init__(self):
        self.path_to_audios = "./Bot/Resources/Audios"
        self.path_to_images = "./Bot/Resources/Images"
        self.path_to_databases = "./Bot/Resources/DataBase"
        
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
