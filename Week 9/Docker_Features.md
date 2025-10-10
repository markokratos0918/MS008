# 🐳 Docker Features — DelTorCarInc_Full

This document explains the key Docker features used (or available) in the **DelTorCarInc Car Rental System** project.  
It links each concept to how it applies to this project’s containerized setup.

---

## ⚙️ 1. Containerization

Docker packages your app, dependencies, and environment into a **container** — a portable, isolated runtime.

### 🔹 In DelTorCarInc:
- The app runs fully self-contained in a container built from `python:3.11-slim`.
- It ensures identical behavior across Windows, macOS, and Linux.
- No local Python setup required — only Docker.

---

## 🧱 2. Images and Layers

Each line in a `Dockerfile` builds an **image layer**.  
Docker caches unchanged layers for faster rebuilds.

### 🔹 In DelTorCarInc:
- Base image: `python:3.11-slim`
- Cached layers: `pip install`, `COPY . /app`
- Small code changes trigger fast incremental rebuilds.

---

## 🧩 3. Portability

“**Build once, run anywhere**.”  
Your container runs the same in development, testing, and production.

### 🔹 In DelTorCarInc:
- You can build on Windows and run on Linux servers with no code change.
- Image: `deltorcarinc:latest` works across all Docker environments.

---

## 💾 4. Volumes (Persistent Data)

Volumes keep your data outside the container so it survives rebuilds.

```bash
-v deltorcarinc_data:/data
```

### 🔹 In DelTorCarInc:
- Stores the SQLite DB (`deltorcarinc.sqlite`) and evidence artifacts under `/data`.
- Volume persists across container runs.

---

## 🌐 5. Networking

Docker provides isolated networks for containers to talk to each other.

### 🔹 Future Use:
When you add an analytics or REST service, they can connect over Docker’s internal network.

Example (in future `docker-compose.yml`):
```yaml
services:
  app:
    build: .
  analytics:
    image: some_dashboard
```

---

## 🔑 6. Environment Variables

Set configuration values dynamically without editing code.

### 🔹 In DelTorCarInc:
```bash
-e DELTORCARINC_DB_PATH=/data/deltorcarinc.sqlite
-e TZ=Pacific/Auckland
```
These configure your database and timezone cleanly.

---

## 📦 7. Docker Compose

Use `docker-compose.yml` to manage multi-service setups.

### 🔹 In DelTorCarInc:
Single command runs your CLI with persistent data:
```bash
docker compose up
```
Can later expand to include:
- Web dashboard container
- Background maintenance jobs

---

## 🔒 8. Isolation & Security

Each container:
- Has its own process space
- Doesn’t affect the host or other containers
- Runs under a non-root user (`appuser`)

### 🔹 In DelTorCarInc:
Securely runs as `appuser` (UID 10001) to avoid privilege escalation.

---

## ⚙️ 9. Resource Control

Limit CPU or memory usage when needed:
```bash
docker run --cpus=1 --memory=512m deltorcarinc:latest
```
Keeps testing environments stable.

---

## 🚀 10. Multi-Stage Builds

Used to build a compact final image by separating build & runtime stages.

### 🔹 Example future enhancement:
```dockerfile
FROM python:3.11 as builder
RUN pip install pyinstaller
RUN pyinstaller --onefile run.py

FROM python:3.11-slim
COPY --from=builder /app/dist/DelTorCarInc /usr/local/bin/
ENTRYPOINT ["DelTorCarInc"]
```

---

## ☁️ 11. Registries and Versioning

Tag, push, and share your images on Docker Hub or private registries.

```bash
docker tag deltorcarinc:latest deltorcarinc:v1.0
docker push username/deltorcarinc:v1.0
```

### 🔹 In DelTorCarInc:
Versioned images can track releases (`v1.0`, `v1.1`).

---

## 🧰 12. Build Automation (CI/CD)

Docker integrates into pipelines (GitHub Actions, Jenkins, etc.) to:
- Build/test images automatically
- Run unit tests inside containers
- Deploy consistent builds

---

## 🔍 13. Logging and Monitoring

View runtime logs:
```bash
docker logs deltorcarinc
```

Integrates with tools like:
- **Grafana** / **Prometheus** for metrics
- **ELK stack** for centralized logs

---

## 🧠 14. Developer Efficiency

- Standard environment for all contributors  
- No “works on my machine” issues  
- Easier rollback and dependency management

---

## 🧮 15. Summary Table

| Feature | Benefit | Used in Project |
|----------|----------|----------------|
| Containerization | Unified runtime | ✅ |
| Volumes | Persistent DB | ✅ |
| Environment Vars | Configurable DB path | ✅ |
| Compose | Multi-service orchestration | ⚙️ Future |
| Isolation | Safe sandboxed runtime | ✅ |
| Multi-stage Build | Compact exe builder | ⚙️ Future |
| Registry | Image version control | ⚙️ Optional |
| Logging | Debugging, monitoring | ✅ |
| CI/CD | Automated builds | ⚙️ Future |

---

### ✅ Example one-liner run
```bash
docker run -it --rm -e DELTORCARINC_DB_PATH=/data/deltorcarinc.sqlite -v deltorcarinc_data:/data deltorcarinc:latest
```

---

*Maintainer: DelTorCarInc Team (Dod / Aileen)*  
*Base image: python:3.11-slim*  
*License: MIT*
