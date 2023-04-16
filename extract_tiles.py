import os
from PIL import Image

def convert_2bpp_to_png(input_2bpp_path, output_png_path, width, height):
    # Read the 2bpp file
    with open(input_2bpp_path, 'rb') as f:
        data = f.read()

    # Calculate the number of tiles
    num_tiles = len(data) // 16

    # Create a new image
    image = Image.new("P", (width, height))
    image.putpalette([
        0, 0, 0,  # Color 0
        85, 85, 85,  # Color 1
        170, 170, 170,  # Color 2
        255, 255, 255  # Color 3
    ])

    pixels = image.load()

    # Process each tile
    for i in range(num_tiles):
        tile_data = data[i * 16:(i + 1) * 16]

        # Calculate the tile position
        tile_x = (i * 8) % width
        tile_y = (i * 8) // width * 8

        for y in range(8):
            byte1 = tile_data[y * 2]
            byte2 = tile_data[y * 2 + 1]

            for x in range(8):
                bit1 = (byte1 >> (7 - x)) & 1
                bit2 = (byte2 >> (7 - x)) & 1
                color = (bit2 << 1) | bit1

                pixels[tile_x + x, tile_y + y] = color

    # Save the image as a PNG
    image.save(output_png_path, 'PNG')


rom = None #load the rom later
rom_filename = os.path.join(os.getcwd(), "pr.gb")
def load_rom(filename=None):
    "load the rom into a global (returns True/False)"
    global rom
    if not filename:
        filename = rom_filename
    try:
        rom = open(filename, "rb").read()
        return True
    except Exception as exception:
        print("error loading rom")
        return False

def main():
    load_rom()
    locations = {
    "Tset00_GFX": [0x64000, 0x645E0, "00"],
    "Tset01_GFX": [0x64DE0, 0x65270, "01"],
    "Tset08_GFX": [0x653A0, 0x65980, "08"],
    "Tset13_GFX": [0x65BB0, 0x66190, "13"],
    "Tset0E_GFX": [0x66610, 0x66BF0, "0e"],
    "Tset10_GFX": [0x66D60, 0x67350, "10"],
    "Tset17_GFX": [0x676F0, 0x67B50, "17"],
    "Tset05_GFX": [0x6807F, 0x6867F, "05"],
    "Tset02_GFX": [0x68DBF, 0x693BF, "02"],
    "Tset09_GFX": [0x6960F, 0x69BFF, "09"],
    "Tset03_GFX": [0x6A3FF, 0x6A9FF, "03"],
    "Tset16_GFX": [0x6B1FF, 0x6B7FF, "16"],
    "Tset0F_GFX": [0x6C000, 0x6C5C0, "0f"],
    "Tset11_GFX": [0x6CCA0, 0x6D0C0, "11"],
    "Tset12_GFX": [0x6D8C0, 0x6DEA0, "12"],
    "Tset0D_GFX": [0x6E390, 0x6E930, "0d"],
    "Tset14_GFX": [0x6ED10, 0x6F2D0, "14"],
    "Tset15_GFX": [0x6F670, 0x6FB20, "15"],
    "Tset0B_GFX": [0x6FD60, 0x6FEF0, "0b"],
    }

    for tileset_id in locations.keys():
        tileset = locations[tileset_id]
        print("writing tilesets/" + tileset[2] + ".2bpp")
        newfile = "tileset/" + tileset[2] + ".2bpp"
        fh = open(newfile, "wb")
        fh.write(rom[tileset[0]:tileset[1]])
        fh.close()
        output_png_path = "tileset/"+tileset[2]+'.png'
        width, height = 64, 128  # Provide the desired width and the height of the output image
        convert_2bpp_to_png(newfile, output_png_path, width, height)

if __name__ == '__main__':
    main()
