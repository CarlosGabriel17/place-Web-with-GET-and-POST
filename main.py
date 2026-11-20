from urllib.parse import quote
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import psycopg2
from database import get_connection

app = FastAPI(title="Sitio Web SSR - Alumnos (GET y POST)")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def consultar_alumnos(request: Request, q: str = "", msg: str = "", error: str = ""):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            if q.strip():
                patron = f"%{q.strip()}%"
                cur.execute(
                    """
                    SELECT no_control, nombre, carrera FROM alumnos
                    WHERE no_control ILIKE %s OR nombre ILIKE %s OR carrera ILIKE %s
                    ORDER BY no_control ASC;
                    """,
                    (patron, patron, patron),
                )
            else:
                cur.execute("SELECT no_control, nombre, carrera FROM alumnos ORDER BY no_control ASC;")
            alumnos = cur.fetchall()
    finally:
        conn.close()

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "alumnos": alumnos, "q": q, "msg": msg, "error": error},
    )


@app.post("/alumnos/alta")
def alta_alumno(no_control: str = Form(...), nombre: str = Form(...), carrera: str = Form(...)):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO alumnos (no_control, nombre, carrera) VALUES (%s, %s, %s);",
                (no_control.strip(), nombre.strip(), carrera.strip()),
            )
            conn.commit()
        return RedirectResponse(url=f"/?msg={quote('Alumno registrado correctamente.')}", status_code=303)
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return RedirectResponse(url=f"/?error={quote('Ese número de control ya existe.')}", status_code=303)
    finally:
        conn.close()


@app.post("/alumnos/baja")
def baja_alumno(no_control: str = Form(...)):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM alumnos WHERE no_control = %s;", (no_control.strip(),))
            conn.commit()
        return RedirectResponse(url=f"/?msg={quote('Alumno dado de baja.')}", status_code=303)
    finally:
        conn.close()