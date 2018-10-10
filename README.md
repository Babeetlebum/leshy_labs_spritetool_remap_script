# Leshy Labs Spritetool Remap Script for Phaser 3
Leshy Labs Spritetool script to map the sprite names after a remapping

# Why
When using the default settings of Leshy Labs Spritetool, the sprite_names are generated automatically using the individual PNG file names. However the mapping is also based on the individual PNGs sizes. When importing the sprites in the game the size box is too large.

In order to get a more accurate mapping I want to use the "Remap" option of the Leshy Labs Spritetool. As a result the sprites are remapped accurately thanks to the Leshy Labs Spritetool's image detection algorithm but in the process the sprite names are gone.

This script matches the sprite_names of the original mapping with the coordinates of the remapped spritesheet and exports as a phaser 3 ready spritesheet_out.json file

# How to
1. Go to https://www.leshylabs.com/apps/sstool/
2. Drag and drop the individual PNGs to the drag box
7. Export the Sprite Sheet, you'll need it in your phaser project ("Save" button in the middle of the page)
3. Export the original Sprite Map ("Save" button on the bottom of the page). The script prompts for a filename but default name is "spritesheet_orig.txt"
4. Hit the Remap button
5. Notice that your sprites are perfectly adjusted now but all the sprites names are gone
6. Export the remapped Sprite Map ("Save" button on the bottom of the page). The script prompts for a filename but default name is "spritesheet_remapped.txt"
8. Throw these two Sprite Maps in the same folder as this python script
9. python leshy_spritemap_remap.py
10. Use the newly generated Sprite Map "spritesheet_out.json" along with the previously exported Sprite Sheet "spritesheet.png" in your phaser 3 project

# What if the remapped file has more sprites than the original file
The Leshy Labs Spritetool "Remap" algorithm identifies each independant square of image and create a new sprite from this. As a result, some small particules may be interpreted as a whole new sprite. The script ignores the really small artifacts (a few pixel wide) and tries to expand the bigger sprites to incorporate these smaller independant sprites. The algorithm worked in my case but is quite simple and may need tweaking 
