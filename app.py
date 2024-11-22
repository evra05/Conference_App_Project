from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

# JSON file path for storing meetings
MEETINGS_FILE = 'scheduled_meetings.json'

# Load scheduled meetings from JSON file
def load_meetings():
    try:
        with open(MEETINGS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save scheduled meetings to JSON file
def save_meetings():
    with open(MEETINGS_FILE, 'w') as file:
        json.dump(scheduled_meetings, file)

# Load meetings into memory at the start
scheduled_meetings = load_meetings()

@app.route('/')
def home():
    return render_template('home.html', meetings=scheduled_meetings)

@app.route('/schedule', methods=['GET', 'POST'])
def schedule_meeting():
    if request.method == 'POST':
        data = request.form
        meeting = {
            "title": data.get("title"),
            "date": data.get("date"),
            "time": data.get("time"),
            "room_name": data.get("room_name"),
            "link": f"https://meet.jit.si/{data.get('room_name')}"
        }
        scheduled_meetings.append(meeting)
        save_meetings()  # Save to JSON file
        return redirect(url_for('schedule_meeting'))
    return render_template('schedule.html', meetings=scheduled_meetings)

@app.route('/remove_meeting/<int:index>')
def remove_meeting(index):
    if 0 <= index < len(scheduled_meetings):
        scheduled_meetings.pop(index)
        save_meetings()  # Save changes to JSON file
    return redirect(url_for('home'))

@app.route('/edit_meeting/<int:index>', methods=['GET', 'POST'])
def edit_meeting(index):
    if 0 <= index < len(scheduled_meetings):
        if request.method == 'POST':
            data = request.form
            scheduled_meetings[index] = {
                "title": data.get("title"),
                "date": data.get("date"),
                "time": data.get("time"),
                "room_name": data.get("room_name"),
                "link": f"https://meet.jit.si/{data.get('room_name')}"
            }
            save_meetings()  # Save changes to JSON file
            return redirect(url_for('home'))
        meeting = scheduled_meetings[index]
        return render_template('edit_meeting.html', meeting=meeting, index=index)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
