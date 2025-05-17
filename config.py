import os
from typing import Dict, Any
from configparser import RawConfigParser

# 获取当前 Python 脚本所在的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 组合出配置文件的绝对路径
config_path = os.path.join(script_dir, "config.ini")

config = RawConfigParser()
config.read(config_path)
config_dict = {
    'tweepy': {
        "api_key": config.get('TWEEPY', 'API_KEY'),
        "api_secret": config.get('TWEEPY', 'API_SECRET'),
        "access_token": config.get('TWEEPY', 'ACCESS_TOKEN'),
        "access_token_secret": config.get('TWEEPY', 'ACCESS_TOKEN_SECRET'),
        "account_number": int(config.get('TWEEPY', 'ACCOUNT_NUMBER')),
        "bearer_token": [],
        "username": config.get('TWEEPY', 'USERNAME'),
        "target_user_id": config.get('TWEEPY', 'TARGET_USER_ID'),
        "target_username": config.get('TWEEPY', 'TARGET_USERNAME'),
        "state_file": config.get('TWEEPY', 'STATE_FILE')
    },
    'qywx': {
        "webhook_url_number": int(config.get('QYWX', "QYWX_WEBHOOK_NUMBER")),
        "webhook_url_list": []
    }
}

if config_dict['qywx']['webhook_url_number'] > 0:
    for i in range (1, config_dict['qywx']['webhook_url_number'] + 1):
        config_dict['qywx']['webhook_url_list'].append(config.get('QYWX', 'QYWX_WEBHOOK_' + str(i)))

if config_dict['tweepy']['account_number'] > 0:
    for i in range (1, config_dict['tweepy']['account_number'] + 1):
        config_dict['tweepy']['bearer_token'].append(config.get('TWEEPY', 'BEARER_TOKEN_' + str(i)))

def get_tweep_api_key() -> str:
    return config_dict['tweepy']['api_key']

def get_tweep_api_secret() -> str:
    return config_dict['tweepy']['api_secret']

def get_tweep_api_access_tokent() -> str:
    return config_dict['tweepy']['access_token']

def get_tweep_api_access_token_secret() -> str:
    return config_dict['tweepy']['access_token_secret']

def get_tweep_api_bearer_token() -> list():
    return config_dict['tweepy']['bearer_token']

def get_tweep_api_username() -> str:
    return config_dict['tweepy']['username']

def get_tweep_api_target_user_id() -> str:
    return config_dict['tweepy']['target_user_id']

def get_tweep_api_target_username() -> str:
    return config_dict['tweepy']['target_username']

def get_tweep_state_file() -> str:
    return config_dict['tweepy']['state_file']

def get_qywx_webhook_url_list() -> str:
    return config_dict['qywx']['webhook_url_list']