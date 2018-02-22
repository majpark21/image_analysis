def overlay_text(imfile, coord, text, output=None, font=None, color=None, show=False):
    """"Read image file, add text at specified positions and save.

    Args:
        imfile (str): Path to the image file.
        coord (list of 2-tuple): Coordinates (x,y) where text is written.
        text (list of str): Text to be written.
        output(str, optional): Path to save the image with overlayed text. Defaults to imfile with 'ovl_' prefix.
        font (ImageFont object, optional): Font of text. Defaults to arial, 12pt.
        color (n-tuple, optional): Color of text. Should have same length as the number of channels in image. Defaults
        to black.
        show (bool, optional): Whether to display the annotated image. Defaults to False.
    Returns:
        None
    Examples:
        # Custom font (tested on Windows, see doc if error)
        myfont= ImageFont.truetype(font='calibri.ttf', size=20)
        overlay_text('path/to/image.jpg', [(40,10), (80,120)], ['1st coords', '2nd coords'], font=myfont)

    """
    if type(coord)!=list or type(text)!=list:
        raise TypeError('coord and text must be lists')
    if len(coord)!=len(text):
        raise ValueError('coord and text must have same length')
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
    for xy, txt in zip(coord, text):
        imdraw.text(xy, txt, font = font, fill = color)
    im.save(output)
    if show:
        im.show()
