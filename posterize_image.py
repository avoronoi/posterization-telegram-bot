import numpy as np
import multiprocessing as mp

def find_label_index(X, centroids, i):
    return np.argmin(np.linalg.norm(X[i] - centroids, axis=1))


def find_labels(X, centroids):
    ctx = mp.get_context('fork')
    with ctx.Pool() as pool:
        labels = np.array(pool.starmap(find_label_index, 
                                       ((X, centroids, i) 
                                        for i in range(X.shape[0]))))
    return labels


def k_means(X, k, n_init=10, max_iter=np.inf, eps=0):   
    k = min(k, X.size)
     
    best_cost = np.inf
    best_centroids = None
    
    for _ in range(n_init):
        centroids = np.float64(X[np.random.choice(X.shape[0], size=k, replace=False)])
        it = 0
        old_cost, cost = None, None
        
        while it < max_iter and (old_cost is None or old_cost - cost > eps * X.size):
            labels = find_labels(X, centroids)
            
            # Update centroids
            new_centroids = centroids.copy()
            cluster_sizes = np.bincount(labels)
            new_centroids[:len(cluster_sizes)][cluster_sizes != 0] = 0
            for i, centroid in enumerate(labels):
                new_centroids[centroid] += X[i]
            new_centroids[:len(cluster_sizes)][cluster_sizes != 0] /= (
                cluster_sizes[cluster_sizes != 0, np.newaxis])
            
            # Calculate new cost
            old_cost = cost
            cost = np.sum(np.linalg.norm(X - new_centroids[labels], axis=1))
            centroids = new_centroids
            it += 1
            
        # Choose the best set of centroids
        if cost < best_cost:
            best_cost = cost
            best_centroids = centroids

    return best_centroids, find_labels(X, best_centroids)


def posterize_image(image, color_num, **kwargs):
    # Make RGB values floats in 0..1 range in order to pass to k_means
    if issubclass(image.dtype.type, np.integer):
        image = np.float32(image.copy()) / 255

    image_reshaped = image.reshape(image.shape[0] * image.shape[1], 
                                   image.shape[2])
    
    centroids, labels = k_means(image_reshaped, color_num, **kwargs)
    
    float_image = centroids[labels].reshape(image.shape)
    return np.uint8(np.round(float_image * 255))