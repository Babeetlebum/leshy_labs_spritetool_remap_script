import csv
import json
import os.path

def calculateAvgWidthAndHeight(csvfile, reader):
    # Calculate the average height and width of a sprite
    total_h = total_w = 0
    for i, row in enumerate(reader):
        total_h += int(row["h"])
        total_w += int(row["w"])
    avg_h = total_h / (i + 1)
    avg_w = total_w / (i + 1)
    # print(avg_w, avg_h)
    csvfile.seek(0)
    return [avg_w, avg_h];

def calculateRowAndColumns(csvfile, reader, avg_w, avg_h):
    # Iterate over the sprites and define row and columns
    # Store new rows and columns in a list and check for duplicates
    list_row_col = []
    for i, row in enumerate(reader):
        # Ignore the sprite if the width and height are too small
        if (int(row["h"]) <= 2 and int(row["w"]) <= 2):
            print "Ignoring "+ row["sprite_name"] +" : too small"
            row["ignore"] = True
            continue;

        # Define row and column
        row["row"] = int(row["x"]) / avg_w
        row["col"] = int(row["y"]) / avg_h
        # Iterate over list filled with new values
        for j, prev in enumerate(list_row_col):
            # Check for duplicates
            if(prev["row"] == row["row"] and prev["col"] == row["col"]):
                print " ---\nDuplicate found : " + prev["sprite_name"] + " and " + row["sprite_name"]
                print "  - "+ str(prev)
                print "  - "+ str(row)
                # Fusionning duplicates
                # Calculate xmin, ymin, xmax, ymax
                print "Fusionning both sprites"
                xmin = min(int(prev["x"]), int(row["x"]))
                ymin = min(int(prev["y"]), int(row["y"]))
                xmax = max(int(prev["x"]) + int(prev["w"]), int(row["x"]) + int(row["w"]))
                ymax = max(int(prev["y"]) + int(prev["h"]), int(row["y"]) + int(row["h"]))
                # Deduce new x, y, w, h
                row["x"] = str(xmin)
                row["y"] = str(ymin)
                row["w"] = str(xmax - xmin)
                row["h"] = str(ymax - ymin)
                print "New sprite : "
                print "  - "+ str(prev)
                print " ---\n"
                # Remove the previous sprite
                del list_row_col[j]
                break
        # Fill the list
        list_row_col.append(row)
        # Print an excerpt
        if(i < 5 and False):
            print row
    csvfile.seek(0)
    return list_row_col;

def formatFrame(sprite):
    return {
        "filename": sprite["sprite_name"] + ".png",
        "frame": {
            "x": sprite["x"],
            "y": sprite["y"],
            "w": sprite["w"],
            "h": sprite["h"],
            },
        "rotated": False,
        "trimmed": False,
        "spriteSourceSize": {
            "x": sprite["x"],
            "y": sprite["y"],
            "w": sprite["w"],
            "h": sprite["h"]
        },
        "sourceSize": {
            "w": sprite["w"],
            "h": sprite["h"]
        }
    };

fieldnames = [
    "sprite_name",
    "x",
    "y",
    "w",
    "h",
]
output_file_name = "spritesheet_out.json"

# Prompting for the original file
sprites_orig_filepath = raw_input("Select the spritesheet.txt file with original mapping and sprite_names:\nDefault: sprites_orig.txt\n")
sprites_orig_filepath = sprites_orig_filepath or "sprites_orig.txt"

if (os.path.isfile(sprites_orig_filepath) == False):
    print "The file was not found, exiting"
    exit()

# Prompting for the remapped file
sprites_remapped_filepath = raw_input("Select the remapped spritesheet.txt file with new mapping but no sprite_names:\nDefault: sprites_remapped.txt\n")
sprites_remapped_filepath = sprites_remapped_filepath or "sprites_remapped.txt"
if (os.path.isfile(sprites_remapped_filepath) == False):
    print "The file was not found, exiting"
    exit()

# Original sprite file : this file has the right sprite_names but wrong coordinates
with open(sprites_orig_filepath, 'r') as sprites_orig_file:
    reader_orig = csv.DictReader(sprites_orig_file, fieldnames)

    # Calculate average width and height of the original sprite map
    [avg_w, avg_h] = calculateAvgWidthAndHeight(sprites_orig_file, reader_orig)

    # Define row and col of each sprite on the original spritesheet
    orig_sprites = calculateRowAndColumns(sprites_orig_file, reader_orig, avg_w, avg_h)
print str(len(orig_sprites)) +" sprites found in "+ str(sprites_orig_filepath)

# Remapped sprite file : this file has the right coordinates but the sprite_names were reset
with open(sprites_remapped_filepath, 'r') as sprites_remapped_file:
    reader_remapped = csv.DictReader(sprites_remapped_file, fieldnames)

    # Define row and col of each sprite on the remapped spritesheet
    remapped_sprites = calculateRowAndColumns(sprites_remapped_file, reader_remapped, avg_w, avg_h)

print str(len(remapped_sprites)) +" sprites found in "+ str(sprites_remapped_filepath)

# Format the JSON
# Memory intensive but I'm lazy
resultObject = {"frames":[]}
for new in remapped_sprites:
    if ("ignore" in new and new["ignore"] == True):
        continue
    for orig in orig_sprites:
        if(orig["row"] == new["row"] and orig["col"] == new["col"]):
            new["sprite_name"] = orig["sprite_name"]
            resultObject["frames"].append(formatFrame(new))
            break
with open(output_file_name, "w") as output_file:
    output_file.write(json.JSONEncoder().encode(resultObject))
    print "File generated : "+ output_file_name
