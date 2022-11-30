from nagging import Nagging
from os import path
from json import load

class Config:

    @staticmethod
    def check():
        configLocation = "config.json"
        if not path.isfile(configLocation):
            Nagging("Missing File", f"Couldn't locate config.json.").error()
            exit(0)
            
        with open(configLocation, "r") as f:
            t = f.read()
            if len(t) < 100:
                Nagging("Invalid Config", f"Config file ({configLocation}) is invalid,\nplease check your configuration.").error()
                exit(0)
        try:
            with open(configLocation, "r") as f:
                _ = load(f)
        except:
            Nagging("Invalid Config", f"Config file ({configLocation}) contains invalid JSON,\nplease check your configuration.").error()
            exit(0)         
        
        return configLocation
        


            

