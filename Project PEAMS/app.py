from flask import Flask, render_template, request, redirect
from database import get_connection

app = Flask(__name__)


# =========================
# EVENTS CRUD
# =========================
@app.route('/events')
def events():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM events"
    cursor.execute(query)

    events_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'events.html',
        events=events_list
    )


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
            1,
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

    return render_template('add_event.html')


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

    query = "SELECT * FROM events WHERE event_id = %s"

    cursor.execute(query, (id,))

    event = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        'edit_event.html',
        event=event
    )


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

# =====================================================
#  ATTENDEES CRUD
# =====================================================

@app.route('/attendees')
def attendees():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM attendees")
    data = cursor.fetchall()
    conn.close()
    return render_template('attendees.html', attendees=data)


@app.route('/add_attendee', methods=['POST'])
def add_attendee():
    name = request.form['name']
    email = request.form['email']

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendees (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    conn.close()

    return redirect('/attendees')


@app.route('/update_attendee/<int:id>', methods=['POST'])
def update_attendee(id):
    name = request.form['name']
    email = request.form['email']

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE attendees SET name=%s, email=%s WHERE id=%s",
        (name, email, id)
    )
    conn.commit()
    conn.close()

    return redirect('/attendees')


@app.route('/delete_attendee/<int:id>')
def delete_attendee(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attendees WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return redirect('/attendees')


# =====================================================
# REGISTRATION CRUD
# =====================================================

@app.route('/registrations')
def registrations():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.id, a.name AS attendee_name, r.event_name, r.status
        FROM registrations r
        JOIN attendees a ON r.attendee_id = a.id
    """)

    data = cursor.fetchall()
    conn.close()
    return render_template('registrations.html', registrations=data)


@app.route('/add_registration', methods=['POST'])
def add_registration():
    attendee_id = request.form['attendee_id']
    event_name = request.form['event_name']
    status = request.form['status']

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO registrations (attendee_id, event_name, status)
        VALUES (%s, %s, %s)
    """, (attendee_id, event_name, status))
    conn.commit()
    conn.close()

    return redirect('/registrations')


@app.route('/update_registration/<int:id>', methods=['POST'])
def update_registration(id):
    event_name = request.form['event_name']
    status = request.form['status']

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE registrations
        SET event_name=%s, status=%s
        WHERE id=%s
    """, (event_name, status, id))

    conn.commit()
    conn.close()

    return redirect('/registrations')


@app.route('/delete_registration/<int:id>')
def delete_registration(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM registrations WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return redirect('/registrations')


# =====================================================
# RUN APP
# =====================================================

if __name__ == '__main__':
    app.run(debug=True)
