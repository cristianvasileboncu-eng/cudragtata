# Cu drag, tata – publicare automată

Rulează singur, în fiecare zi, pe serverele GitHub (gratuit):
3 video-uri text + muzică și 3 poze, programate în Buffer pentru Instagram, TikTok și YouTube.

- Pornire manuală: tab-ul **Actions** → „Publicare zilnică Cu drag, tata” → **Run workflow**.
- Cheile se pun în **Settings → Secrets and variables → Actions**:
  `BUFFER_API_KEY`, `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`.
- Muzica (fișiere .mp3 cu licență liberă) se pune în `assets/muzica/`.
- Textele sunt în `app/continut_text.py`, orele în `config.json`.
