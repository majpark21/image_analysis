def overlay_label(imfile, coord, labels, output=None, font=None, color=None, show=False):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.open(imfile)
    imdraw = ImageDraw.Draw(im)
    if output is None:
        output = 'ovl'+imfile
    if font is None:
        font = ImageFont.truetype(font='arial', size=12)
    if color is None:
        # Default to black for grayscale('L') or RGB
        default_col = {'L':0, 'RGB':(0,0,0)}
        color = default_col[im.mode]
    imdraw.text(coord, labels, font = font, fill = color)
    im.save(output)
    if show:
        im.show()

overlay_label('temp_astro.jpg', (40,40), 'blabla')