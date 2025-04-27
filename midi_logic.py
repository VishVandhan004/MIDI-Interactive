import mido

# ————————————————————————————————
# MIDI setup with graceful fallback
# ————————————————————————————————
try:
    # Use RtMidi backend and open a virtual ALSA port
    mido.set_backend('mido.backends.rtmidi')
    output_port = mido.open_output(virtual=True)
except Exception as e:
    # On Render (or any headless server) this will likely fail.
    # Fall back to a dummy port that swallows messages.
    print("⚠️  Warning: MIDI output unavailable, running in dummy mode:", e)
    class DummyPort:
        def send(self, msg): pass
    output_port = DummyPort()

# ————————————————————————————————
# GM instruments (128 total)
# ————————————————————————————————
gm_instruments = [
    "Acoustic Grand Piano", "Bright Acoustic Piano", "Electric Grand Piano", "Honky-tonk Piano",
    "Electric Piano 1 (Rhodes Piano)", "Electric Piano 2 (Chorused Rhodes)", "Harpsichord", "Clavinet",
    "Celesta", "Glockenspiel", "Music Box", "Vibraphone", "Marimba", "Xylophone", "Tubular Bells", "Dulcimer",
    "Drawbar Organ", "Percussive Organ", "Rock Organ", "Church Organ", "Reed Organ", "Accordion", "Harmonica",
    "Tango Accordion", "Acoustic Guitar (nylon)", "Acoustic Guitar (steel)", "Electric Guitar (jazz)",
    "Electric Guitar (clean)", "Electric Guitar (muted)", "Overdriven Guitar", "Distortion Guitar",
    "Guitar Harmonics", "Acoustic Bass", "Electric Bass (finger)", "Electric Bass (pick)", "Fretless Bass",
    "Slap Bass 1", "Slap Bass 2", "Synth Bass 1", "Synth Bass 2", "Violin", "Viola", "Cello", "Contrabass",
    "Tremolo Strings", "Pizzicato Strings", "Orchestral Harp", "Timpani", "String Ensemble 1",
    "String Ensemble 2", "SynthStrings 1", "SynthStrings 2", "Choir Aahs", "Voice Oohs", "Synth Voice",
    "Orchestra Hit", "Trumpet", "Trombone", "Tuba", "Muted Trumpet", "French Horn", "Brass Section",
    "SynthBrass 1", "SynthBrass 2", "Soprano Sax", "Alto Sax", "Tenor Sax", "Baritone Sax", "Oboe",
    "English Horn", "Bassoon", "Clarinet", "Piccolo", "Flute", "Recorder", "Pan Flute", "Blown Bottle",
    "Shakuhachi", "Whistle", "Ocarina", "Lead 1 (square)", "Lead 2 (sawtooth)", "Lead 3 (calliope)",
    "Lead 4 (chiff)", "Lead 5 (charang)", "Lead 6 (voice)", "Lead 7 (fifths)", "Lead 8 (bass + lead)",
    "Pad 1 (new age)", "Pad 2 (warm)", "Pad 3 (polysynth)", "Pad 4 (choir)", "Pad 5 (bowed)",
    "Pad 6 (metallic)", "Pad 7 (halo)", "Pad 8 (sweep)", "FX 1 (rain)", "FX 2 (soundtrack)", "FX 3 (crystal)",
    "FX 4 (atmosphere)", "FX 5 (brightness)", "FX 6 (goblins)", "FX 7 (echoes)", "FX 8 (sci-fi)", "Sitar",
    "Banjo", "Shamisen", "Koto", "Kalimba", "Bag pipe", "Fiddle", "Shanai", "Tinkle Bell", "Agogo",
    "Steel Drums", "Woodblock", "Taiko Drum", "Melodic Tom", "Synth Drum", "Reverse Cymbal",
    "Guitar Fret Noise", "Breath Noise", "Seashore", "Bird Tweet", "Telephone Ring", "Helicopter",
    "Applause", "Gunshot"
]

# ————————————————————————————————
# Note mapping (Sa Re Ga Ma…)
# ————————————————————————————————
key_to_note = {
    'sa': 60,     # C4
    're': 62,     # D4
    'ga': 64,     # E4
    'ma': 65,     # F4
    'pa': 67,     # G4
    'dha': 69,    # A4
    'ni': 71,     # B4
    'sa_high': 72 # C5
}

# ————————————————————————————————
# State: current program (instrument)
# ————————————————————————————————
current_program = 0

# ————————————————————————————————
# Helpers to change instrument
# ————————————————————————————————
def set_program_by_number(n):
    """Set current_program to n (0–127)."""
    global current_program
    if 0 <= n < len(gm_instruments):
        current_program = n

def set_program_by_name(name):
    """Look up instrument name in gm_instruments and set program."""
    global current_program
    if name in gm_instruments:
        current_program = gm_instruments.index(name)

# ————————————————————————————————
# Play / stop functions (called by Flask routes)
# ————————————————————————————————
def play_note(note_name):
    """Send program change + note_on for given note_name."""
    if note_name in key_to_note:
        note = key_to_note[note_name]
        # program change
        output_port.send(mido.Message('program_change', program=current_program, channel=0))
        # note on
        output_port.send(mido.Message('note_on', note=note, velocity=64, channel=0))

def stop_note(note_name):
    """Send note_off for given note_name."""
    if note_name in key_to_note:
        note = key_to_note[note_name]
        output_port.send(mido.Message('note_off', note=note, velocity=64, channel=0))
