from flask import Flask, render_template, request
import midi_logic

app = Flask(__name__)

# serve your piano UI
@app.route('/')
def index():
    return render_template('index.html')

# play a note
@app.route('/play_note/<note>', methods=['GET'])
def play_note_route(note):
    midi_logic.play_note(note)
    return '', 204

# stop a note
@app.route('/stop_note/<note>', methods=['GET'])
def stop_note_route(note):
    midi_logic.stop_note(note)
    return '', 204

# change instrument by name
@app.route('/set_instrument', methods=['POST'])
def set_instrument():
    data = request.json or {}
    name = data.get('instrument')
    if name:
        midi_logic.set_program_by_name(name)
    return '', 204

if __name__ == '__main__':
    # listen on all interfaces so Render can route traffic
    app.run(host='0.0.0.0', port=10000, debug=True)
