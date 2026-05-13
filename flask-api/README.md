# DevOps Flask Exam Template

This folder contains a ready Flask API template for open-book DevOps exam practice.

Files:
- `app.py` - complete Flask CRUD API template
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker container setup
- `curl_commands.sh` - useful test commands

Run locally:
```bash
pip3 install -r requirements.txt
python3 app.py
```

Run with Docker:
```bash
docker build -t flask-api:v1 .
docker run -d -p 5000:5000 --restart=always --name flask-api flask-api:v1
```

Test:
```bash
curl -i http://localhost:5000/api/health
curl -i http://localhost:5000/api/students
```
