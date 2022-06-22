import csv
import text_to_mp3
import os


def convert_verses_to_mp3(csv_file):
    with open(csv_file, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            print(row[0])
            full_verse = row[0] + " — " + row[1]
            mp3_file = row[1].replace(" ", "_")
            text_to_mp3.text_to_mp3(full_verse, "verse_tracks/" + mp3_file)


if __name__ == "__main__":
    convert_verses_to_mp3("verses.csv")
    print("Done!")
