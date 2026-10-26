# Intermediate — stream the answer — Hints

> [Back to the exercise](../README.md#ex-streaming_ui) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](streaming_ui_solution.md)

- [Hint 1 — a generator of tokens](#hint-1)
- [Hint 2 — forward it, don't buffer](#hint-2)

## Hint 1 — a generator of tokens {: #hint-1 }

Streaming starts with a generator that `yield`s pieces of text. In a real app that's your `chain.stream(inputs)`; to practice, fake one:

```
import time
def stream_answer(text):
    for word in "this is a streamed reply".split():
        time.sleep(0.02)
        yield word + " "
```

The web layer's only job is to forward what this yields.

## Hint 2 — forward it, don't buffer {: #hint-2 }

- **Streamlit:** `st.write_stream(stream_answer(text))` — renders each chunk as it arrives.
- **FastAPI:** `return StreamingResponse(stream_answer(body.text), media_type="text/plain")` — the browser gets the body in chunks.
- **Flask:** `return Response(stream_answer(text), mimetype="text/plain")`.

The mistake to avoid: collecting the whole answer first (`"".join(gen)`) and then returning it — that's not streaming, the user still waits for everything. Pass the **generator itself** through. Test the FastAPI one with `TestClient`: `client.post("/stream", json={"text":"hi"}).text` assembles to the full reply. The full code is in the [Solution](streaming_ui_solution.md).
