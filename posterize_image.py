from matplotlib.image import imread
import numpy as np
import sklearn.cluster

def posterize_image(image, color_num, **kwargs):
    # Make RGB values floats in 0..1 range in order to pass to k_means
    if issubclass(image.dtype.type, np.integer):
        image = np.float32(image.copy()) / 255

    image_reshaped = image.reshape(image.shape[0] * image.shape[1], 
                                   image.shape[2])
    
    centroid, label = sklearn.cluster.k_means(image_reshaped, color_num, 
                                              **kwargs)[:2]
    
    float_image = centroid[label].reshape(image.shape)
    return np.uint8(np.round(float_image * 255))
        