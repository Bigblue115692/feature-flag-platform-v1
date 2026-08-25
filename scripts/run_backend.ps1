if (-not (Test-Path ".venv")) {
    python -m venv .venv
}
& .\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
}
python -m backend.scripts.seed
python -m uvicorn backend.app.main:app --reload
