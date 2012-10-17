from convertColor import *

class myIO():
    """ My IO class for reading and saving data
    
    """
    def __init__(self, speicherpfad):
        """ Initialisation by choosing the file path
        
        """
        self.speicherpfad = speicherpfad
        self.cC = Convert_to_color()

    def save_2D_list(self, mylist, header, speichername='test.txt', **kwargs):
        """ Needs documentation and reprogramming
        
        """
        if 'speicherpfad' not in kwargs.keys():
            speicherpfad = self.speicherpfad + speichername
        else:
            speicherpfad = kwargs['speicherpfad']
            import os
            if not os.path.exists(speicherpfad):
                os.makedirs(speicherpfad)
            speicherpfad = speicherpfad + speichername
        header = header
        data = mylist
        #umwandeln der liste in text
        for index in range(len(data)):
            data[index] = str(data[index])
            data[index] = data[index].lstrip('[')
            data[index] = data[index].rstrip(']')
            data[index] = data[index].replace(', ', '\t')
        with open(speicherpfad, 'wb') as f:
            f.write(header + '\n')
            for entry in data:
                f.write(entry+'\n')

    def save_2D_list_oH(self, mylist, speichername='test.txt'):
        """ Needs documentation and reprogramming
        
        """
        speicherpfad = self.speicherpfad + speichername
        data = mylist
        #umwandeln der liste in text
        for index in range(len(data)):
            data[index] = str(data[index])
            data[index] = data[index].lstrip('[')
            data[index] = data[index].rstrip(']')
            data[index] = data[index].replace(', ', '\t')
        with open(speicherpfad, 'wb') as f:
            for entry in data:
                f.write(entry+'\n')

    def save_ndarray_as_Image(self, ndarray, speichername, **kwargs):
        """ Needs documentation and reprogramming
        
        """
        """
        kwargs argumente:
        speicherpfad = str,
        normiert = bool,
        color = bool
        """
        resultImage = PILImage.fromarray(ndarray)
        resultImage = resultImage.convert("L")
        try:
            if kwargs['normiert'] == True:
                import ImageOps
                resultImage = ImageOps.autocontrast(resultImage, cutoff=0)
        except:
            pass
        
        try:
            if kwargs['color'] == True:
                resultImage = self.cC.convert_to_rgb(resultImage)
        except:
            pass
        
        
        if 'speicherpfad' not in kwargs.keys():
            speicherpfad = self.speicherpfad + speichername
        else:
            speicherpfad = kwargs['speicherpfad']
            import os
            if not os.path.exists(speicherpfad):
                os.makedirs(speicherpfad)
            speicherpfad = speicherpfad + speichername
        resultImage.save(speicherpfad)





