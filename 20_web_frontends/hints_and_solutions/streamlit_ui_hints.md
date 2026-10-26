# Basic — a Streamlit UI — Hints

> [Back to the exercise](../README.md#ex-streamlit_ui) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](streamlit_ui_solution.md)

- [Hint 1 — widgets are function calls](#hint-1)
- [Hint 2 — chat needs session_state](#hint-2)

## Hint 1 — widgets are function calls {: #hint-1 }

A Streamlit app is a normal Python script. Each widget is a function that returns its current value:

```
import streamlit as st
from pipeline import classify
st.title("Sentiment Classifier")
text = st.text_input("Type something:")
if st.button("Classify"):
    st.write(classify(text))
```

Run it with `streamlit run app_streamlit.py`. The whole script re-runs top to bottom every time the user clicks — there are no routes and no server code to write. Guard the empty case: `if text.strip():` before calling the pipeline.

## Hint 2 — chat needs session_state {: #hint-2 }

Because the script re-runs on every interaction, a chatbot would forget the conversation — unless you store it in `st.session_state`, which survives re-runs:

```
if "messages" not in st.session_state:
    st.session_state["messages"] = []
# render each past message with st.chat_message(role)
user_text = st.chat_input("Say something")
if user_text:
    append {role: user, content: user_text}
    append {role: assistant, content: classify(user_text)}
    st.rerun()
```

`st.chat_message` / `st.chat_input` are the built-in chat widgets, and `st.session_state["messages"]` is the memory. That's the whole front end for an agent. The full code is in the [Solution](streamlit_ui_solution.md).
