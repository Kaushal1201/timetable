from flask import Flask, render_template, request, Response
import random
import json
import csv
from io import StringIO

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

# CSV download route
@app.route('/download', methods=['POST'])
def download_csv():
    timetable1 = json.loads(request.form['timetable1'])
    timetable2 = json.loads(request.form['timetable2'])

    # Convert timetable1 and timetable2 to CSV format
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Day', 'Time', 'Subject'])
    for day in timetable1:
        for time, subject in timetable1[day].items():
            writer.writerow([day, time, subject])
    for day in timetable2:
        for time, subject in timetable2[day].items():
            writer.writerow([day, time, subject])

    output.seek(0)
    return Response(output.getvalue(),
                    mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment;filename=timetable.csv'})

# PDF download route (currently a placeholder)
@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    timetable1 = json.loads(request.form['timetable1'])
    timetable2 = json.loads(request.form['timetable2'])

    # Create a PDF (use a library like `reportlab` for this)
    # For simplicity, we won't implement it fully here
    return "PDF download feature is not implemented yet."

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

