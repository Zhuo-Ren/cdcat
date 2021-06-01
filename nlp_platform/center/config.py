import nlp_platform.center.config_log

class Config:
    _config_dict = {}

    @staticmethod
    def load_config(config_dir, config_name="center_config"):
        import json
        with open(config_dir, 'r', encoding='utf8') as f:
            Config._config_dict[config_name] = json.load(f)

    @staticmethod
    def get_config():
        return Config._config_dict