import sys
import mido as mido
import numpy as np
from operator import itemgetter
from note import Note
from pychore import ChordRecognizer, Chord, ChordName
from functools import reduce
import inquirer


def num_to_symbol(num):
        if num in range(0, 132, 12):
            return "C"
        if num in range(1, 132, 12):
            return "C#"
        if num in range(2, 132, 12):
            return "D"
        if num in range(3, 132, 12):
            return "D#"
        if num in range(4, 132, 12):
            return "E"
        if num in range(5, 132, 12):
            return "F"
        if num in range(6, 132, 12):
            return "F#"
        if num in range(7, 132, 12):
            return "G"
        if num in range(8, 132, 12):
            return "G#"
        if num in range(9, 132, 12):
            return "A"
        if num in range(10, 132, 12):
            return "A#"
        if num in range(11, 132, 12):
            return "B"


def check_if_octave(chord_notes, note):
    for i in range(12, 132, 12):
        if note + i in chord_notes or note - i in chord_notes:
            return True
        else:
            return False


def expand_tracks(midi_file):
    return [t.name for t in midi_file.tracks]


def parse_midi(file_name):
    # User inputs the desired length for chord determination
    # 1 represents a quoter note; 4 is a bar
    resolution = 96 * int(4)
 
    # User inputs the number of notes to be analized as element of a chord
    chord_tone_num = int(4)

    f = mido.MidiFile(file_name)

    question = [inquirer.questions.List('track_name', message='Select track to process.', choices=expand_tracks(f))]

    track_name = ""
    while True:
        track_name_user_input = inquirer.prompt(question)
        track_name = track_name_user_input['track_name']
        if track_name not in [track.name for track in f.tracks]:
            print('No track such', track_name)
            return
        else:
            break    

    track = [t for t in f.tracks if t.name == track_name][0]

    msgs = []
    abs_time = 0

    for msg in track:
        abs_time += msg.time
        one_msg = [abs_time, msg.type]
        if msg.type == 'note_on' or msg.type == 'note_off':
            one_msg.append(msg.note)
            msgs.append(one_msg)

    note_nums = [m[2] for m in msgs]
    note_nums = list(set(note_nums))
    note_nums = [int(m) for m in note_nums]
    note_nums.sort()

    dict_by_note = {}
    for note_num in note_nums:
        list_by_note = list(filter(lambda x: x[2] == note_num, msgs))
        note_ons = np.asarray([m[0] for m in list_by_note if m[1] == 'note_on'])
        note_offs = np.asarray([m[0] for m in list_by_note if m[1] == 'note_off'])
        note_ons2D = note_ons.reshape(note_ons.shape[0], -1)
        note_offs2D = note_offs.reshape(note_offs.shape[0], -1)
        on_offs = np.hstack((note_ons2D, note_offs2D))
        dict_by_note[note_num] = on_offs

    note_obj_list = []
    for note_num, on_offs in dict_by_note.items():
        for on_off in on_offs:
            note_obj_list.append(Note(note_num, on_off[0], on_off[1]))

    notes_dup_rate_by_section = {}
    cursor_index = 1

    for cursor in range(0, msgs[-1][0] + resolution, resolution):
        note_dup_rate_dict = {}
        for note in note_obj_list:
            rate = note.get_duplication_rate(cursor, cursor + resolution)
            if rate != None and rate != 0:
                if note.number in note_dup_rate_dict.keys():
                    note_dup_rate_dict[note.number] += rate
                else:
                    note_dup_rate_dict[note.number] = rate
        notes_dup_rate_by_section[cursor_index] = note_dup_rate_dict
        cursor_index += 1

    chords = {}
    recognizer = ChordRecognizer.ChordRecognizer()
    while True:
        for cursor, note_dup in notes_dup_rate_by_section.items():
            chord_notes = []
            # Sorted descendingly by duplication rate
            sorted_list = sorted(note_dup.items(), key=itemgetter(1), reverse=True)
            for note, dup in sorted_list:
                # Get rid of short 'noise' and octoved
                if dup > 0.02 and not check_if_octave(chord_notes, note):
                    chord_notes.append(note)
            trimmed_chord_notes = chord_notes[:chord_tone_num]

            if len(chord_notes) > 1:
                cho = Chord.Chord([num_to_symbol(n).lower() for n in trimmed_chord_notes])
                chord_name = recognizer.RecognizeChord(cho)
                # If given chord does not match anything in table of PyChoRe,
                # just show the notes
                if chord_name == None:
                    # chord_name = f"No Match({' '.join([num_to_symbol(n) for n in chord_notes])})"
                    chord_name = ChordName.ChordName('', '', '', chord_notes)
                    pass
                # First loop    
                if cursor not in chords.keys():
                    chords[cursor] = chord_name
                # Second loop and after
                # if cursor in chords.keys() and str(chords[cursor])[:8] == 'No Match':
                #     chords[cursor] = chord_name
                if cursor in chords.keys() and chords[cursor].RootName == '':
                    chords[cursor] = chord_name
            if len(trimmed_chord_notes) == 0:
                chords[cursor] = ChordName.ChordName('Blank', '', '')
        if chord_tone_num < 4:
            break

        chord_tone_num -= 1


    chunk = 4
    chord_list = [cho_name.GetRootName().title() + 
                    cho_name.GetModifier() + '[' +
                    reduce((lambda sum, current: sum + current + ', '),
                            list([num_to_symbol(note) for note in cho_name.Notes]), '')[:-2] + ']'
                    for cho_name in chords.values()]
    chord_sheet = [chord_list[i:i+chunk] for i in range(0, len(chord_list), chunk)]

    print( [list(map((lambda n: n[0:-2] if n[-2:] == '[]' else n),  row)) for row in chord_sheet])
    
if __name__ == '__main__':
    parse_midi(sys.argv[1])