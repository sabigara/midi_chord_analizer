import mido
import sys


def main():

    file = mido.MidiFile('oasis.mid')
    for track in file.tracks:
        print(track)

    del file.tracks[3]

    print('\nDeleted track 3.\n')

    for track in file.tracks:
        print(track)

    new_track = mido.MidiTrack()
    new_track.name = 'New Track'
    new_track.append(mido.Message('program_change', program=12, time=0))
    new_track.append(mido.Message('note_on', note=64, velocity=64, time=32))
    new_track.append(mido.Message('note_off', note=64, velocity=127, time=32))

    file.tracks.append(new_track)

    print('\nAdded a new track.\n')

    for track in file.tracks:
        print(track)

    print()

    for message in new_track:
        print(message)

    print(new_track[2].note)



    return 0


if __name__ == '__main__':
    main()