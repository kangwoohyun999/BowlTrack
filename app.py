import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'bowling_secret_key_2025')

# ── DB 연결 ──────────────────────────────────────────────

def get_db():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL 환경변수가 설정되지 않았습니다.")
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id        SERIAL PRIMARY KEY,
            username  TEXT UNIQUE NOT NULL,
            password  TEXT NOT NULL,
            nickname  TEXT NOT NULL,
            style     TEXT NOT NULL DEFAULT 'dumless',
            status    TEXT NOT NULL DEFAULT '볼링이 좋아 🎳',
            dark_mode BOOLEAN NOT NULL DEFAULT FALSE,
            strikes   INTEGER NOT NULL DEFAULT 0,
            spares    INTEGER NOT NULL DEFAULT 0,
            misses    INTEGER NOT NULL DEFAULT 0
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id         SERIAL PRIMARY KEY,
            username   TEXT NOT NULL REFERENCES users(username) ON DELETE CASCADE,
            date       TEXT NOT NULL,
            score      INTEGER,
            note       TEXT DEFAULT '',
            strikes    INTEGER NOT NULL DEFAULT 0,
            spares     INTEGER NOT NULL DEFAULT 0,
            misses     INTEGER NOT NULL DEFAULT 0,
            UNIQUE (username, date)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_user(username):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close(); conn.close()
    return dict(user) if user else None

# ── Routes ──────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('home') if 'username' in session else url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = get_user(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error='아이디 또는 비밀번호가 틀렸습니다.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        nickname = request.form.get('nickname', '').strip() or username
        style    = request.form.get('style', 'dumless')
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password, nickname, style) VALUES (%s, %s, %s, %s)",
                (username, password, nickname, style)
            )
            conn.commit()
            session['username'] = username
            return redirect(url_for('home'))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            return render_template('register.html', error='이미 존재하는 아이디입니다.')
        finally:
            cur.close(); conn.close()
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = get_user(session['username'])
    return render_template('home.html', user=user)

@app.route('/calendar')
def calendar():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = get_user(session['username'])
    return render_template('calendar.html', user=user)

@app.route('/stats')
def stats():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = get_user(session['username'])
    total = user['strikes'] + user['spares'] + user['misses']
    def pct(v): return round(v / total * 100, 1) if total > 0 else 0
    return render_template('stats.html', user=user,
        strike_pct=pct(user['strikes']),
        spare_pct=pct(user['spares']),
        miss_pct=pct(user['misses']))

@app.route('/info')
def info():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = get_user(session['username'])
    return render_template('info.html', user=user)

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = get_user(session['username'])
    return render_template('profile.html', user=user)

@app.route('/settings')
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = get_user(session['username'])
    return render_template('settings.html', user=user)

# ── API ─────────────────────────────────────────────────

@app.route('/api/save_record', methods=['POST'])
def save_record():
    if 'username' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    body     = request.get_json()
    username = session['username']
    date     = body.get('date')
    score    = body.get('score') or None
    note     = body.get('note', '')
    strikes  = int(body.get('strikes', 0))
    spares   = int(body.get('spares', 0))
    misses   = int(body.get('misses', 0))

    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT strikes, spares, misses FROM records WHERE username=%s AND date=%s",
                (username, date))
    old = cur.fetchone()
    old_s  = old['strikes'] if old else 0
    old_sp = old['spares']  if old else 0
    old_m  = old['misses']  if old else 0

    cur.execute("""
        INSERT INTO records (username, date, score, note, strikes, spares, misses)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (username, date) DO UPDATE
        SET score=%s, note=%s, strikes=%s, spares=%s, misses=%s
    """, (username, date, score, note, strikes, spares, misses,
          score, note, strikes, spares, misses))

    cur.execute("""
        UPDATE users
        SET strikes = strikes - %s + %s,
            spares  = spares  - %s + %s,
            misses  = misses  - %s + %s
        WHERE username = %s
    """, (old_s, strikes, old_sp, spares, old_m, misses, username))

    conn.commit(); cur.close(); conn.close()
    return jsonify({'ok': True})

@app.route('/api/get_records')
def get_records():
    if 'username' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT date, score, note, strikes, spares, misses FROM records WHERE username=%s",
                (session['username'],))
    rows = cur.fetchall()
    cur.close(); conn.close()
    return jsonify({r['date']: dict(r) for r in rows})

@app.route('/api/update_profile', methods=['POST'])
def update_profile():
    if 'username' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    body = request.get_json()
    conn = get_db(); cur = conn.cursor()
    cur.execute("UPDATE users SET nickname=%s, status=%s WHERE username=%s",
                (body.get('nickname'), body.get('status'), session['username']))
    conn.commit(); cur.close(); conn.close()
    return jsonify({'ok': True})

@app.route('/api/update_settings', methods=['POST'])
def update_settings():
    if 'username' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    body = request.get_json()
    conn = get_db(); cur = conn.cursor()
    cur.execute("UPDATE users SET style=%s, dark_mode=%s WHERE username=%s",
                (body.get('style'), body.get('dark_mode'), session['username']))
    conn.commit(); cur.close(); conn.close()
    return jsonify({'ok': True})

# ── 실행 ─────────────────────────────────────────────────

with app.app_context():
    try:
        init_db()
    except Exception as e:
        print(f"[init_db 스킵] DB 미연결 상태: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
