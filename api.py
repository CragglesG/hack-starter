import fastapi
import uvicorn
import os
from dotenv import load_dotenv
import subprocess
import docker

load_dotenv()

client = docker.from_env()

app = fastapi.FastAPI()

@app.post("/start-hack")
def start_hack(data: dict):
    try:
        port = subprocess.run(["nest", "get_port"], capture_output=True).stdout.decode().strip().split(' ')[1]
        with open("start-hack") as f:
            client.containers.run(image="lscr.io/linuxserver/code-server:latest", detach=True,
                                  name=data["user_id"] + "-" + data["project_name"], ports={port: "8443"},
                                  volumes={"~/.config/code-server/config.yaml": {"bind": "/config/config.yaml", "mode": "rw"}},
                                  environment={"PASSWORD": data["password"], "TZ": "Etc/UTC", "PUID": "1000", "PGID": "1000"})
        subprocess.run(f"nest caddy add {data['project_name']}.{data['username']}.craigg.hackclub.app --proxy 0.0.0.0:{port}".split(" "))
        return {"url": f"https://{data['project_name']}.{data['username']}.craigg.hackclub.app"}
    except Exception as e:
        return fastapi.HTTPException(status_code=500, detail=str(e))

@app.post("/stop-hack")
def stop_hack(data: dict):
    subprocess.run(f'docker stop {data["user_id"] + "-" + data["project_name"]}'.split(" "))

@app.post("/resume-hack")
def restart_hack(data: dict):
    subprocess.run(f'docker start {data["user_id"] + "-" + data["project_name"]}'.split(" "))

@app.post("/delete-hack")
def delete_hack(data: dict):
    subprocess.run(f'docker stop {data["user_id"] + "-" + data["project_name"]}'.split(" "))
    subprocess.run(f'docker rm {data["user_id"] + "-" + data["project_name"]}'.split(" "))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
