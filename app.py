
from flask import Flask, render_template
import threading
import midi_logic  # notice: underscore instead of dash

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def run_midi_logic():
    midi_logic.start_midi_listener()

if __name__ == '__main__':
    threading.Thread(target=run_midi_logic, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
