# Author - Uma Abu
# Description - This file contains stand alone script used for generating the thumbnail.

from PIL import Image, ImageFont, ImageDraw 


thumbnail_template = Image.open("thumbnail_template.png") # Open the template
image_width, image_height = thumbnail_template.size # Get the size of the template
title_font = ImageFont.truetype('peace-sans.regular.ttf', 180) # Load the font
view_count = 300
formated_view_count = format(view_count, ',d')
views_count_string = str(formated_view_count) # Text to be written
image_editable = ImageDraw.Draw(thumbnail_template) # Make the image editable
_, _, textbox_width, textbox_height = image_editable.textbbox((0, 0), views_count_string, font=title_font)
image_editable.text(((image_width-textbox_width)/2, 75), views_count_string, (255, 255, 255), font=title_font)# Draw the text
thumbnail_template.save("result.png") # Save the image
