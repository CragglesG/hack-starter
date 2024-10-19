import fastapi
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = fastapi.FastAPI()

@app.post("/start-hack")
def start_hack(data: dict):
    try:
        port = os.system("nest get_port")
        with open("start-hack") as f:
            os.system(f.read().replace("[PORT]", str(port))
                      .replace("[NAME]", data["user_id"] + "-" + data["project_name"])
                      .replace("[PASSWORD]", data["password"]))
        os.system(f"nest caddy add {data['project_name']}.{data['username']}.craigg.hackclub.app --proxy 0.0.0.0:{port}")
        return {"url": f"https://{data['project_name']}.{data['username']}.craigg.hackclub.app"}
    except Exception as e:
        return fastapi.HTTPException(status_code=500, detail=str(e))

@app.post("/stop-hack")
def stop_hack(data: dict):
    os.system(f'docker stop {data["user_id"] + "-" + data["project_name"]}')

@app.post("/resume-hack")
def restart_hack(data: dict):
    os.system(f'docker start {data["user_id"] + "-" + data["project_name"]}')

@app.post("/delete-hack")
def delete_hack(data: dict):
    os.system(f'docker stop {data["user_id"] + "-" + data["project_name"]}')
    os.system(f'docker rm {data["user_id"] + "-" + data["project_name"]}')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.environ.get("PORT", 8000))