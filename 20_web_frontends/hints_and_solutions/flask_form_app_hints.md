# Intermediate — a Flask app with a form — Hints

> [Back to the exercise](../README.md#ex-flask_form_app) · [Hint 1](#hint-1) · [Hint 2](#hint-2) · [Solution](flask_form_app_solution.md)

- [Hint 1 — one route, two methods](#hint-1)
- [Hint 2 — the template and the JSON route](#hint-2)

## Hint 1 — one route, two methods {: #hint-1 }

One `/` route handles both showing the form and processing it:

```
@app.route("/", methods=["GET", "POST"])
def home():
    label = None; text = ""
    if request.method == "POST":
        text = request.form.get("text", "")
        if text.strip():
            label = classify(text)
    return render_template_string(PAGE, label=label, text=text)
```

GET shows an empty form; POST reads `request.form["text"]`, calls the pipeline, and re-renders the same page with the answer. That re-render-with-the-result is the whole trick.

## Hint 2 — the template and the JSON route {: #hint-2 }

The template is HTML with Jinja slots — fixed page, changing `{{ text }}` and `{{ label }}`:

```
<form method="post">
  <input name="text" value="{{ text }}"><button>Classify</button>
</form>
{% if label %}<p>Result: {{ label }}</p>{% endif %}
```

Add a JSON route for programmatic callers, and validate there:

```
@app.post("/classify")
def classify_api():
    data = request.get_json(silent=True) or {}
    if not data.get("text","").strip():
        return jsonify({"error":"empty text"}), 400
    return jsonify({"label": classify(data["text"])})
```

Test both with `app.test_client()` — no running server needed. The full code is in the [Solution](flask_form_app_solution.md).
