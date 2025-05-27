import configparser

def get_all(category, main_dir):
    config = configparser.ConfigParser(interpolation=None)
    config.read(main_dir + "/config.ini")
    if category not in config:
        print(f"Error: Category {category} not found in configuration file")
        input("Press Enter to exit...")
        exit()
    config_values = config[category].items()
    return tuple(value for key, value in config_values)