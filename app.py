from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Timetable generation function
def generate_timetable(subjects):
    timetable = {}
    time_slots = ['9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM']
    assigned_subjects = set()

    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        day_timetable = {}
        used_subjects = set()
        random.shuffle(time_slots)

        for hour in time_slots:
            subject = random.choice(subjects)
            while subject in used_subjects or subject in assigned_subjects or list(day_timetable.values()).count(subject) == 2:
                subject = random.choice(subjects)

            day_timetable[hour] = subject
            used_subjects.add(subject)
            assigned_subjects.add(subject)

        timetable[day] = day_timetable

    return timetable

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject_input = request.form['subjects']
        subjects = [s.strip() for s in subject_input.split(',') if s.strip()]
        
        if len(subjects) < 7:
            error = "Please enter at least 7 subjects."
            return render_template('index.html', error=error)

        timetable1 = generate_timetable(subjects)
        timetable2 = generate_timetable(subjects)

        return render_template('result.html', timetable1=timetable1, timetable2=timetable2)

    return render_template('index.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
