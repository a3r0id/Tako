from nagging import Nagging
from os import path
from json import load

class Config:

    @staticmethod
    def check():
        configLocation = "config.json"
        if path.isfile(configLocation):
            pass
        
        else:
            # CHECK FOR config_location.txt
            if not path.isfile("config_location.txt"):
                Nagging("Missing File", f"Couldn't locate config_location.txt.").error()
                exit(0)

            # GET PATH OF CONFIG FILE FROM config_location.txt
            with open("config_location.txt", "r") as f:
                configLocation = f.read()


        # CHECK IF PATH EXISTS
        if not path.isfile(configLocation):
            Nagging("Invalid Path", f"{configLocation} does not exist.\nChange path in config_location.txt.").error()
            exit(0)

        # TRY TO OPEN THE FILE
        with open(configLocation, "r") as f:
            t = f.read()
            if len(t) < 280:
                Nagging("Invalid Config", f"Config file ({configLocation}) is invalid,\nplease check your configuration.").error()
                exit(0)

        try:
            with open(configLocation, "r") as f:
                _ = load(f)
        except:
            Nagging("Invalid Config", f"Config file ({configLocation}) contains invalid JSON,\nplease check your configuration.").error()
            exit(0)         
        
        return configLocation
        


            

