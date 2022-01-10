"""Config script for cmus_scrobbler."""

import os
import json
import lastfm

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "cmus-scrobbler")
CONFIG_JSON = os.path.join(CONFIG_DIR, "cmus_scrobbler_config.json")

def _setup_config() -> bool:
    """Creates the API config directory and file"""
    
    try:
        os.mkdir(CONFIG_DIR)
    except (IOError, PermissionError) as e:
        print(f"DEBUG: Failed to create config directory due to '{e}'")
        return False

    try:
        with open (CONFIG_JSON, "w") as cfg_f:
            json.dump({"api_key": "", "secret_key": "", "session_key": "", "api_token": ""}, cfg_f)
    except (IOError, PermissionError) as e:
        print(f"DEBUG: Failed to create config file due to '{e}'")
        return False

    return True

def read_config() -> dict:
    """Wrapper for opening CONFIG_JSON and returning it as a dictionary"""
    
    try:    
        with open (CONFIG_JSON) as cfg:
            cfg_json = json.load(cfg)
    except (json.decoder.JSONDecodeError, PermissionError, IOError) as e:
        print(f"DEBUG: Refusing to read config, encountered '{e}'")
        return None

    return cfg_json

def update_config(api_key: str = None, secret_key: str = None, session_key: str = None, api_token: str = None) -> bool:
    """Updates the values in the API config file"""

    if not os.path.exists(CONFIG_JSON):
        if not _setup_config():
            print("DEBUG: Refusing to update config, file/directory do not exist and were unable to be created")
            return False

    if not (cfg_json := read_config()):
        return False
    
    if api_key:
        cfg_json["api_key"] = api_key
    if secret_key:
        cfg_json["secret_key"] = secret_key
    if session_key:
        cfg_json["session_key"] = session_key
    if api_token:
        cfg_json["api_token"] = api_token
    
    try:
        with open(CONFIG_JSON, 'w') as cfg:
            json.dump(cfg_json, cfg)
    except PermissionError as e:
        print(f"DEBUG: Refusing to update config, encountered '{e}'")
        return False
    return True