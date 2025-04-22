from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_targets():
    conn = sqlite3.connect("data/data.db")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT 지원대상 FROM support ORDER BY 지원대상")
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]

@app.route("/", methods=["GET", "POST"])
def index():
    keyword = request.form.get("keyword", "").strip() if request.method == "POST" else ""
    target = request.form.get("target", "").strip() if request.method == "POST" else ""
    region = request.form.get("region", "").strip() if request.method == "POST" else ""

    targets = get_targets()

    query = "SELECT rowid, * FROM support WHERE 1=1"
    params = []

    if keyword:
        query += " AND 사업명 LIKE ?"
        params.append(f"%{keyword}%")
    if target:
        query += " AND 지원대상 = ?"
        params.append(target)

    conn = sqlite3.connect("data/data.db")
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    results = [{"id": r[0], "사업명": r[1], "지원대상": r[2]} for r in rows]

    return render_template("index.html", results=results, keyword=keyword, target=target, targets=targets, region=region)

@app.route("/detail/<int:item_id>")
def detail(item_id):
    conn = sqlite3.connect("data/data.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM support WHERE rowid = ?", (item_id,))
    row = cur.fetchone()
    conn.close()

    if row:
        return render_template("detail.html", row={
            "id": item_id,
            "사업명": row[0],
            "지원대상": row[1]
        })
    else:
        return "❌ 상세 정보를 찾을 수 없습니다.", 404

if __name__ == "__main__":
    app.run(debug=True)
