# Production server - раздача статических файлов фронтенда + API proxy
import os
import httpx
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import aiofiles
import subprocess

# Путь к фронтенду
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend", "dist")

app = FastAPI(title="PlusTim API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Backend API URL
BACKEND_URL = "http://localhost:8080"

# Mount static files from frontend
static_dir = os.path.join(FRONTEND_DIR, "assets")
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=static_dir), name="assets")

# Health check
@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "PlusTim Server Running"}

# Upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...), path: str = ""):
    """Загрузка файла на сервер"""
    try:
        if path:
            full_path = os.path.join(FRONTEND_DIR, path)
        else:
            full_path = os.path.join(FRONTEND_DIR, file.filename)
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        content = await file.read()
        with open(full_path, "wb") as f:
            f.write(content)
        
        return {"status": "ok", "path": full_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Deploy endpoint
@app.post("/deploy")
async def deploy_frontend():
    """Полный деплой фронтенда через git pull"""
    try:
        subprocess.run(["pkill", "-f", "python.*server.py"], capture_output=True)
        
        result = subprocess.run(
            ["git", "pull", "origin", "main"],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True
        )
        
        subprocess.Popen(
            ["nohup", "python", "server.py", ">", "server.log", "2>&1", "&"],
            cwd=os.path.dirname(__file__),
            shell=True
        )
        
        return {"status": "ok", "git_output": result.stdout + result.stderr}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# Generic proxy handler for all API requests
async def proxy_to_backend(request: Request):
    """Проксирование API запросов на backend"""
    path = request.url.path
    if path.startswith("/api/"):
        path = path[5:]
    
    backend_url = f"{BACKEND_URL}/{path}"
    body = await request.body()
    
    headers = {}
    for key, value in request.headers.items():
        if key.lower() != "host":
            headers[key] = value
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=request.method,
                url=backend_url,
                content=body,
                headers=headers,
                params=request.query_params
            )
            
            return JSONResponse(
                content=response.json() if response.content else {},
                status_code=response.status_code
            )
    except httpx.ConnectError:
        return JSONResponse(
            {"error": "Backend API not available", "detail": f"Cannot connect to {BACKEND_URL}"},
            status_code=503
        )
    except Exception as e:
        return JSONResponse(
            {"error": "API Proxy Error", "detail": str(e)},
            status_code=500
        )

app.add_route("/api/{path:path}", proxy_to_backend, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])

@app.get("/{path:path}")
async def serve_frontend(request: Request, path: str):
    file_path = os.path.join(FRONTEND_DIR, path)
    if path and os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    return HTMLResponse("""
    <html>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h1>PlusTim</h1>
            <p>Telegram Web App</p>
            <p>Frontend is loading...</p>
            <p><small>Server is running</small></p>
        </body>
    </html>
    """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)