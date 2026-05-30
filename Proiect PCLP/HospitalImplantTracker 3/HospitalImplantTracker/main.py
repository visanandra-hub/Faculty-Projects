# Importăm obiectul `app` din pachetul nostru principal (unde e definită aplicația Flask)
from app import app  # noqa: F401
# noqa: F401 este un comentariu special pentru linters (ex: Flake8) ca să ignore faptul că "app" pare nefolosit.
# De fapt, este necesar ca aplicația să pornească.

# Verificăm dacă acest fișier este executat direct (nu importat din alt modul)
if __name__ == "__main__":
    # Pornim serverul Flask
    app.run(
        host="0.0.0.0",  # Face aplicația accesibilă din rețea (nu doar local)
        port=5050,       # Rulează pe portul 5000 (standard pentru Flask)
        debug=True,       # Activează modul debug (utile pentru dezvoltare)
        use_reloader=False   # Dezactivează reloader-ul automat
    )
