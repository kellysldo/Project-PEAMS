from flask import Flask, render_template, request, redirect
from database import get_connection

app = Flask(__name__)


# =========================
# VIEW EVENTS
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

    query = "SELECT * FROM events WHERE event_id = %s"

    cursor.execute(query, (id,))

    event = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        'edit_event.html',
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

# ==============================================================

# =========================
# VIEW ATTENDEES
# =========================
@app.route('/attendees')
def attendees():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM attendees"
    cursor.execute(query)

    attendees_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'attendees.html',
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

    return render_template('add_attendee.html')


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
        'edit_attendee.html',
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

# =================================================================

# =========================
# VIEW REGISTRATIONS
# =========================
@app.route('/registrations')
def registrations():

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

    cursor.execute(query)

    registrations_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'registrations.html',
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
        'add_registration.html',
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


# =========================
# RUN APP
# =========================
if __name__ == '__main__':
    app.run(debug=True)
