from slack_bolt import App
from requests import request
import os
from dotenv import load_dotenv

load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        client.views_publish(
            user_id=event["user"],
            view={
                "type": "home",
                "callback_id": "home_view",

                # body of the view
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Start Your Hack!",
                            "emoji": True
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*IMPORTANT: Make sure that your project name is lowercase and excludes spaces and special characters (other than - and _)!*"
                        }
                    },
                    {
                        "type": "input",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "project-name"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Project Name",
                            "emoji": True
                        }
                    },
                    {
                        "type": "input",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "password"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Password",
                            "emoji": True
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Hack!",
                                    "emoji": True
                                },
                                "value": "start-hack-button",
                                "action_id": "start-hack"
                            }
                        ]
                    }
                ]
            }
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.action("start-hack")
def start_hack(ack, body, logger):
    ack()
    request("POST", "https://api.example.com/start-hack", data={"user_id": body["user"]["id"], "username": body["user"]["username"], "project_name":
        body["view"]["state"]["values"][body["view"]["blocks"][3]["block_id"]]["project-name"]["value"], "password":
        body["view"]["state"]["values"][body["view"]["blocks"][4]["block_id"]]["password"]["value"]})


if __name__ == "__main__":
    app.start(3000)