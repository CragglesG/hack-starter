from slack_bolt import App
from requests import request
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        with open("views/home.json") as f:
            client.views_publish(
                user_id=event["user"],
                view=json.load(f)
            )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")
        print(e)


@app.action("start-hack")
def start_hack(ack, body, logger):
    ack()
    request("POST", "https://hackstarter-api.craigg.hackclub.app/start-hack", json={"user_id": body["user"]["id"], "username": body["user"]["username"], "project_name":
        body["view"]["state"]["values"][body["view"]["blocks"][3]["block_id"]]["project-name"]["value"], "password":
        body["view"]["state"]["values"][body["view"]["blocks"][4]["block_id"]]["password"]["value"]})

@app.command("/start-hack")
def start_hack_command(ack, body, logger, client):
    ack()
    with open("views/start-modal.json") as f:
        client.views_open(trigger_id=body["trigger_id"], view=json.load(f))

@app.view_submission("start-modal")
def start_hack_submission(ack, body, logger):
    ack()
    request("POST", "https://hackstarter-api.craigg.hackclub.app/start-hack", json={"user_id": body["user"]["id"], "username": body["user"]["username"], "project_name":
        body["view"]["state"]["values"][body["view"]["blocks"][3]["block_id"]]["project-name"]["value"], "password":
        body["view"]["state"]["values"][body["view"]["blocks"][4]["block_id"]]["password"]["value"]})

@app.command("/stop-hack")
def stop_hack_command(ack, body, logger, client):
    ack()
    with open("views/stop-modal.json") as f:
        client.views_open(trigger_id=body["trigger_id"], view=json.load(f))

@app.view_submission("stop-hack")
def stop_hack(ack, body, logger):
    ack()
    request("POST", "https://hackstarter-api.craigg.hackclub.app/stop-hack", json={"user_id": body["user"]["id"], "project_name": body["view"]["state"]["values"][body["view"]["blocks"][2]["block_id"]]["project-name"]["value"]})

@app.command("/resume-hack")
def resume_hack_command(ack, body, logger, client):
    ack()
    with open("views/resume-modal.json") as f:
        client.views_open(trigger_id=body["trigger_id"], view=json.load(f))

@app.view_submission("resume-hack")
def resume_hack(ack, body, logger):
    ack()
    request("POST", "https://hackstarter-api.craigg.hackclub.app/resume-hack", json={"user_id": body["user"]["id"], "project_name": body["view"]["state"]["values"][body["view"]["blocks"][2]["block_id"]]["project-name"]["value"]})

@app.command("/delete-hack")
def delete_hack_command(ack, body, logger, client):
    ack()
    with open("views/delete-modal.json") as f:
        client.views_open(trigger_id=body["trigger_id"], view=json.load(f))

@app.view_submission("delete-hack")
def delete_hack(ack, body, logger):
    ack()
    request("POST", "https://hackstarter-api.craigg.hackclub.app/delete-hack", json={"user_id": body["user"]["id"], "project_name": body["view"]["state"]["values"][body["view"]["blocks"][2]["block_id"]]["project-name"]["value"]})

if __name__ == "__main__":
    app.start(int(os.environ.get("PORT", 3000)))
