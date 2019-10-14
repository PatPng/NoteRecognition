import input
import output


def main():
    track = input.getMidiNotes()
    print("==============")
    output.createMidi(track)


if __name__ == "__main__":
    main()
