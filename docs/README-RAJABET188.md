# Rajabet188 V2

Project Flask dark-gold premium dengan frontend responsif dan admin panel awal.

## Login admin awal
- Username: `admin`
- Password: `admin123`

Segera ganti password setelah deploy.

## Jalankan lokal
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## Deploy Render
Build Command:
```bash
pip install -r requirements.txt
```
Start Command:
```bash
gunicorn run:app
```
