# Backend Contract

The front-end is already built. To make it work, your Flask backend must
provide the routes below with the **exact endpoint names** (the templates call
them via `url_for`). For each, the variables the template expects are listed.

> Tip: attribute access in the templates is written as `student.firstname`.
> That works whether `student` is an ORM object **or** a dict (Jinja maps
> `student.firstname` to `student['firstname']` automatically). So either DB
> approach is fine.

---

## Routes the templates call by name

| Endpoint (function name) | Method | Purpose | Must pass to template |
|---|---|---|---|
| `home` | GET | Landing page | — |
| `portal` | GET | Show the registration form | — |
| `save_student` | POST | Handle the form submit | (redirects to `students`) |
| `students` | GET | List + filter all students | `students=[...]` |
| `student_detail` | GET | One student's full record | `student={...}` (takes `id`) |
| `update_status` | POST | Async status change | JSON `{ "success": true }` / 400 |

A minimal stub so the app boots while you build:

```python
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/portal")
def portal():
    return render_template("portal_form.html")

@app.route("/save_student", methods=["POST"])
def save_student():
    # validate, save image to static/uploads/, insert row, then:
    return redirect(url_for("students"))

@app.route("/students")
def students():
    return render_template("students.html", students=[])

@app.route("/student/<int:id>")
def student_detail(id):
    return render_template("student_details.html", student=get_one(id))

@app.route("/update_status", methods=["POST"])
def update_status():
    return jsonify(success=True)
```

---

## `students` — list items

Each item needs: `id`, `firstname`, `middlename`, `lastname`, `gender`,
`jamb`, `status`. The template numbers rows itself (`loop.index`) — you don't
need a serial column in the DB.

## `student_detail` — single record

Needs everything above plus: `image` (stored filename, or falsy → placeholder
shows), `email`, `phone`, `dob`, `address`, `nextofkin`, and the location.
For the location you can pass either raw values (`state`, `lga`) or resolved
names (`state_name`, `lga_name`) — the template prefers the `_name` version and
falls back to the raw one.

## Form field names (what `save_student` receives)

`image` (file), `firstname`, `middlename`, `lastname`, `email`, `dob`,
`gender`, `phone`, `address`, `state`, `lga`, `nextofkin`, `jamb`.

Remember: set the image's saved **filename** in the DB, save the **file** to
`static/uploads/`, and `redirect(url_for("students"))` on success.

---

## The two async features (the JS is stubbed for you)

### 1. State ➜ LGA dependent dropdowns (`static/js/locations.js`)

Expose data one of two ways:

- **JSON endpoints** (recommended):
  - `GET /api/states` → `["Abia State", "Adamawa State", ...]`
  - `GET /api/lgas/<state>` → `["Aba North", "Aba South", ...]`
  - You can build both from the bundled `static/data/states-lgas.json`.
- **Or** let the browser fetch `static/data/states-lgas.json` directly and
  filter it client-side (no endpoint needed).

### 2. Async status change (`static/js/status.js`)

```
POST /update_status
body: { "student_id": <id>, "status": "admitted|undecided|rejected" }
→ 200 { "success": true }   on success
→ 400 { "error": "..." }    if the status value isn't one of the three
```

Validate the status server-side against the allowed set before writing.
