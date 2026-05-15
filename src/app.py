from flask import Flask, render_template, request, redirect, session, url_for, flash
from database import get_connection
from werkzeug.security import generate_password_hash
from flask_bcrypt import Bcrypt
import os
import re
print("CURRENT DIR:", os.getcwd())

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "your_secret_key"

# ==================================================================================================

# =========================
# VIEW USERS + SEARCH
# =========================
@app.route('/users')
def users():

    if session.get('role') != 'admin':
        flash("Access denied!")
        return redirect('/')

    search = request.args.get('search', '')
# @app.route('/users')
# def users():

#     search = request.args.get('search', '')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if search:
        cursor.execute("""
            SELECT * FROM users
            WHERE full_name LIKE %s
               OR username LIKE %s
               OR email LIKE %s
               OR role LIKE %s
        """, (f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    conn.close()

    return render_template('users/users.html', users=users)


# =========================
# ADD USERS
# =========================
@app.route('/users/add', methods=['GET', 'POST'])
def add_user():

    if session.get('role') != 'admin':
        flash("Access denied!")
        return redirect('/')

    if request.method == 'POST':

        full_name = request.form['full_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        role = request.form['role']

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (full_name, username, email, password, role)
                VALUES (%s, %s, %s, %s, %s)
            """, (full_name, username, email, password, role))

            conn.commit()

        except Exception as e:
            conn.rollback()
            return f"Error: {e}"

        finally:
            conn.close()

        return redirect('/users')

    return render_template('users/add_user.html')

# =========================
# EDIT USERS
# =========================
@app.route('/users/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):

    if session.get('role') != 'admin':
        flash("Access denied!")
        return redirect('/')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':

        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        role = request.form['role']

        try:
            cursor.execute("""
                UPDATE users
                SET full_name=%s,
                    email=%s,
                    password=%s,
                    role=%s
                WHERE user_id=%s
            """, (full_name, email, password, role, id))

            conn.commit()

        except Exception as e:
            conn.rollback()
            return f"Error: {e}"

        finally:
            conn.close()

        return redirect('/users')

    cursor.execute(
        "SELECT * FROM users WHERE user_id=%s",
        (id,)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template('users/edit_user.html', user=user)


# =========================
# DELETE USERS
# =========================
@app.route('/users/delete/<int:id>')
def delete_user(id):

    if session.get('role') != 'admin':
        flash("Access denied!")
        return redirect('/')

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "DELETE FROM users WHERE user_id=%s",
            (id,)
        )

        conn.commit()

    except Exception as e:

        conn.rollback()
        return f"Error: {e}"

    finally:
        conn.close()

    return redirect('/users')
# ==================================================================================================


# =========================
# VIEW EVENTS + SEARCH
# =========================
@app.route('/events')
def events():

    search = request.args.get('search', '')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if search:
        cursor.execute("""
            SELECT * FROM events
            WHERE event_name LIKE %s
               OR location LIKE %s
               OR description LIKE %s
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))
    else:
        cursor.execute("SELECT * FROM events")

    events_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'events/events.html',
        events=events_list
    )


# =========================
# ADD EVENT
# =========================
@app.route('/add_event', methods=['GET', 'POST'])
def add_event():

    if request.method == 'POST':

        event_name = request.form['event_name']
        event_date = request.form['event_date']
        location = request.form['location']
        description = request.form['description']

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO events (
            user_id,
            event_name,
            event_date,
            location,
            description
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            session['user_id'],
            event_name,
            event_date,
            location,
            description
        )

        cursor.execute(query, values)

        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/events')

    return render_template('events/add_event.html')


# =========================
# EDIT EVENT
# =========================
@app.route('/edit_event/<int:id>', methods=['GET', 'POST'])
def edit_event(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':

        event_name = request.form['event_name']
        event_date = request.form['event_date']
        location = request.form['location']
        description = request.form['description']

        query = """
        UPDATE events
        SET
            event_name=%s,
            event_date=%s,
            location=%s,
            description=%s
        WHERE event_id=%s
        """

        values = (
            event_name,
            event_date,
            location,
            description,
            id
        )

        cursor.execute(query, values)

        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/events')

    query = """
    SELECT * FROM events
    WHERE user_id = %s
    """

    cursor.execute(query, (session['user_id'],))

    event = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        'events/edit_event.html',
        event=event
    )


# =========================
# DELETE EVENT
# =========================
@app.route('/delete_event/<int:id>')
def delete_event(id):

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM events WHERE event_id = %s"

    cursor.execute(query, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/events')

# ==================================================================================================

# =========================
# VIEW ATTENDEES + SEARCH
# =========================
@app.route('/attendees')
def attendees():

    search = request.args.get('search', '')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if search:
        cursor.execute("""
            SELECT * FROM attendees
            WHERE fullname LIKE %s
               OR email LIKE %s
               OR contact_no LIKE %s
               OR address LIKE %s
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))
    else:
        cursor.execute("SELECT * FROM attendees")

    attendees_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'attendees/attendees.html',
        attendees=attendees_list
    )


# =========================
# ADD ATTENDEE
# =========================
@app.route('/add_attendee', methods=['GET', 'POST'])
def add_attendee():

    if request.method == 'POST':

        fullname = request.form['fullname']
        email = request.form['email']
        contact_no = request.form['contact_no']
        address = request.form['address']

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO attendees (
            fullname,
            email,
            contact_no,
            address
        )
        VALUES (%s, %s, %s, %s)
        """

        values = (
            fullname,
            email,
            contact_no,
            address
        )

        cursor.execute(query, values)

        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/attendees')

    return render_template('attendees/add_attendee.html')


# =========================
# EDIT ATTENDEE
# =========================
@app.route('/edit_attendee/<int:id>', methods=['GET', 'POST'])
def edit_attendee(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':

        fullname = request.form['fullname']
        email = request.form['email']
        contact_no = request.form['contact_no']
        address = request.form['address']

        query = """
        UPDATE attendees
        SET
            fullname=%s,
            email=%s,
            contact_no=%s,
            address=%s
        WHERE attendee_id=%s
        """

        values = (
            fullname,
            email,
            contact_no,
            address,
            id
        )

        cursor.execute(query, values)

        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/attendees')

    query = "SELECT * FROM attendees WHERE attendee_id = %s"

    cursor.execute(query, (id,))

    attendee = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        'attendees/edit_attendee.html',
        attendee=attendee
    )


# =========================
# DELETE ATTENDEE
# =========================
@app.route('/delete_attendee/<int:id>')
def delete_attendee(id):

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM attendees WHERE attendee_id = %s"

    cursor.execute(query, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/attendees')

# ==================================================================================================

# =========================
# VIEW REGISTRATIONS + SEARCH
# =========================
@app.route('/registrations')
def registrations():

    search = request.args.get('search', '')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        registrations.registration_id,
        attendees.fullname,
        events.event_name,
        registrations.attendance_status,
        registrations.registration_date
    FROM registrations
    JOIN attendees
        ON registrations.attendee_id = attendees.attendee_id
    JOIN events
        ON registrations.event_id = events.event_id
    """

    if search:
        query += """
        WHERE attendees.fullname LIKE %s
           OR events.event_name LIKE %s
           OR registrations.attendance_status LIKE %s
        """

        cursor.execute(query, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))
    else:
        cursor.execute(query)

    registrations_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'registrations/registrations.html',
        registrations=registrations_list
    )


# =========================
# ADD REGISTRATION
# =========================
@app.route('/add_registration', methods=['GET', 'POST'])
def add_registration():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':

        attendee_id = request.form['attendee_id']
        event_id = request.form['event_id']
        attendance_status = request.form['attendance_status']

        query = """
        INSERT INTO registrations (
            attendee_id,
            event_id,
            attendance_status,
            registration_date
        )
        VALUES (%s, %s, %s, NOW())
        """

        values = (
            attendee_id,
            event_id,
            attendance_status
        )

        cursor.execute(query, values)

        conn.commit()

        return redirect('/registrations')

    cursor.execute("SELECT * FROM attendees")
    attendees = cursor.fetchall()

    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'registrations/add_registration.html',
        attendees=attendees,
        events=events
    )


# =========================
# DELETE REGISTRATION
# =========================
@app.route('/delete_registration/<int:id>')
def delete_registration(id):

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM registrations WHERE registration_id = %s"

    cursor.execute(query, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/registrations')
# ==================================================================================================


# =========================
# REGISTER
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # USERNAME LENGTH VALIDATION
        if len(username) > 20:
            flash("Username must not exceed 20 characters!")
            return redirect('/register')

        # PASSWORD LENGTH VALIDATION
        if len(password) > 20:
            flash("Password must not exceed 16 characters!")
            return redirect('/register')

        # EMAIL VALIDATION
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(email_pattern, email):
            flash("Invalid email format!")
            return redirect('/register')

        # HASH PASSWORD
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        try:

            # CHECK IF USERNAME ALREADY EXISTS
            cursor.execute(
                "SELECT * FROM users WHERE username = %s",
                (username,)
            )

            existing_user = cursor.fetchone()

            if existing_user:
                flash("Username already exists!")
                return redirect('/register')

            # CHECK IF EMAIL ALREADY EXISTS
            cursor.execute(
                "SELECT * FROM users WHERE email = %s",
                (email,)
            )

            existing_email = cursor.fetchone()

            if existing_email:
                flash("Email already exists!")
                return redirect('/register')

            # INSERT NEW USER
            cursor.execute("""
                INSERT INTO users (
                    full_name,
                    email,
                    username,
                    password
                )
                VALUES (%s, %s, %s, %s)
            """, (
                full_name,
                email,
                username,
                hashed_password
            ))

            conn.commit()

            flash("Registration successful!")
            return redirect('/login')

        except Exception as e:

            conn.rollback()
            return f"Error: {e}"

        finally:

            cursor.close()
            conn.close()

    return render_template('login/register.html')


# =========================
# LOGIN
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s",
            (username,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()
    

        if user and bcrypt.check_password_hash(
            user['password'],
            password
        ):

            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['role'] = user['role']

            flash("Login successful!")

            return redirect('/')

        else:
            flash("Invalid username or password")

    return render_template('login/login.html')


# =========================
#  LOGOUT
# =========================
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect('/login')


# =========================
# INDEX ROUTE
# =========================
@app.route('/')
def index():

    if 'user_id' not in session:
        return redirect('/login')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM events")
    total_events = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attendees")
    total_attendees = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM registrations")
    total_registrations = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template(
        'login/index.html',
        total_events=total_events,
        total_attendees=total_attendees,
        total_registrations=total_registrations
    )


# =========================
# RUN APP
# =========================
if __name__ == '__main__':
    app.run(debug=True)