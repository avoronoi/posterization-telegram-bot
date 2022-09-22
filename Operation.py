import numpy as np
from posterize_image import posterize_image
from PIL import Image

K_MEANS_TRIALS = 10

class Operation:
    def __init__(self):
        self.image = None
        self.image_id = None
        self.color_num = None
    
    @property
    def color_num(self):
        return self._color_num
    
    @color_num.setter
    def color_num(self, value: str):
        if value is None:
            self._color_num = None
            return
        try:
            value = int(value)
        except ValueError:
            raise ValueError('Please enter an integer.')
        if value < 1 or value > 256:
            raise ValueError('Please enter a number between 1 and 256.')
        self._color_num = value
        
    def posterize_image(self):
        if self.color_num == None:
            raise ValueError('The number of colors has not been specified.')
        np_image = np.asarray(self.image)
        image_id = self.image_id
        color_num = self.color_num
        self.image = self.image_id = self.color_num = None
        posterized_image = posterize_image(np_image, color_num, 
                                           n_init=K_MEANS_TRIALS)
        return Image.fromarray(posterized_image), image_id