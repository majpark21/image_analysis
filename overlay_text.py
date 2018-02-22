def overlay_txt(imfile, coord, text, output=None, font=None, color=None, show=False):
    """"Read image file and add text at specified position.

    Args:
        imfile (str): Path to the image file.
        coord (2-tuple): Coordinates (x,y) where text is written.
        text (str): Text to be written.
        output(str, optional): Path to save the image with overlayed text. Defaults to imfile with 'ovl_' prefix.
    """
    from PIL import Image, ImageDraw, ImageFont
    # Read image file and create drawing object
    im = Image.open(imfile)
    imdraw = ImageDraw.Draw(im)
    # Set defaults
    if output is None:
        output = 'ovl_'+imfile
    if font is None:
        font = ImageFont.truetype(font='arial', size=12)
    if color is None:
        # Default to black for grayscale('L') or RGB
        default_col = {'L':0, 'RGB':(0,0,0)}
        color = default_col[im.mode]
    # Add text and save
    imdraw.text(coord, text, font = font, fill = color)
    im.save(output)
    if show:
        im.show()

overlay_label('temp_astro.jpg', (40,40), 'blabla')