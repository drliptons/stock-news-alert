import requests


def send_msg(discord_webhook: str, msg: str):

    data = {"content": msg}
    response = requests.post(discord_webhook, json=data)

    print(f"Status code: {response.status_code}")
