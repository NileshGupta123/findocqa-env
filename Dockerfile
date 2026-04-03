# ── Base Image ─────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ── Environment Variables ──────────────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860

# ── Working Directory ──────────────────────────────────────────────────────────
WORKDIR /app

# ── Install Dependencies ───────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Copy Project Files ─────────────────────────────────────────────────────────
COPY server/ ./server/
COPY openenv.yaml .
COPY inference.py .

# ── Expose Port (HuggingFace Spaces uses 7860) ─────────────────────────────────
EXPOSE 7860

# ── Start Server ───────────────────────────────────────────────────────────────
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "7860"]