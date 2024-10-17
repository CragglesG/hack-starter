import fastapi
import uvicorn
import os

app = fastapi.FastAPI()

@app.post("/start-hack")
def start_hack(data: dict):
    try:
        os.mkdir(f"hack-starter/{data['user_id']}/{data['project_name']}")
    finally:
        os.chdir(f"hack-starter/{data['user_id']}/{data['project_name']}")
        os.system("git init")
        port = os.system("nest get_port")
        os.system(f"nohup code-server --bind-addr 0.0.0.0:{port} &")
        os.system(f"nest caddy add {data['project_name']}.{data['username']}.craigg.hackclub.app --proxy 0.0.0.0:{port}")