# Intermediate — a file-upload app — Hints

> [Back to the exercise](../README.md#ex-file_upload_app) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](file_upload_app_solution.md)

- [Hint 1 — one widget, bytes out](#hint-1)
- [Hint 2 — PDFs, and validating the upload](#hint-2)

## Hint 1 — one widget, bytes out {: #hint-1 }

Every framework's file input hands you bytes:

- **Streamlit:** `uploaded = st.file_uploader("File", type=["txt","pdf"])` returns a file-like object (or `None`); `uploaded.read()` → bytes.
- **FastAPI:** `async def upload(file: UploadFile): data = await file.read()` — plus `file.filename`.
- **Flask:** `request.files["file"].read()`.

For a `.txt`, `data.decode()` gives the text; feed it to your pipeline.

## Hint 2 — PDFs, and validating the upload {: #hint-2 }

A PDF isn't text — save the bytes to a temp file and use Doc08's loader:

```
import tempfile
from langchain_community.document_loaders import PyPDFLoader
with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
    tmp.write(uploaded.read()); path = tmp.name
pages = PyPDFLoader(path).load()   # then join page.page_content
```

Always validate first: check the filename extension (`name.lower().endswith((".txt",".pdf"))`) and reject anything else with a clear error — never process an unknown or empty upload. Test the FastAPI version with `TestClient` and `files={"file": ("note.txt", b"...", "text/plain")}`. The full code is in the [Solution](file_upload_app_solution.md).
