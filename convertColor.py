import numpy as np
from PIL import Image as PILImage

    
class Convert_to_color():
    """ Converts array/image to another color format
    
    """
    def __init__(self):
        """ Does nothing currntly
        
        """
        pass

    def convert_to_rgb(self, pilImage):
        """ Converts an monochrome Pil Image to rgb
        
        pilImage (PilImage): monochrom PIL Image object
        
        """
        assert pilImage.mode == "L"
        lut = []
        adp = 256
        depth = 255
        Deltax = adp/4
        steigung = depth/Deltax
        for i in range(adp):
            if i <= adp/4:
                r = depth
                g = steigung * i
                b = 0
            elif i > adp/4 and  i <= adp/2:
                r = depth- steigung*(i-adp/4)
                g = depth
                b = 0
            elif i > adp/2 and i <= adp*3/4:
                r = 0
                g = depth
                b = steigung*(i-adp/2)  
            else:
                r = 0
                g = depth - steigung*(i-adp*3/4)  
                b = depth
            lut.extend([r, g, b])
        pilImage.putpalette(lut)
        assert pilImage.mode == "P"
        return pilImage

"""
fp = 'testcbild.bmp'
myImage = PILImage.open(fp)
myImage = myImage.convert("L")

cc = Convert_to_color()
myImage = cc.convert_to_rgb(myImage)

sp = 'bugc.png'
myImage.save(sp)
"""



