import cv2
import numpy as np
from PIL import Image


####################################
# IN-LINE DISPLAY                  #
####################################
def display_np(x, scale = 1.0, resampling = Image.Resampling.BICUBIC):
    im = Image.fromarray(x.clip(0, 255).astype(np.uint8))
    display(im.resize((np.array(im.size)*scale).astype(int), resampling))
    
def display_np_row(x, scale = 1.0, resampling = Image.Resampling.BICUBIC, spacer_width = 0, spacer_grayscale = 0):
    img = np.array(x, dtype=np.uint8)
    if len(img.shape) <= 3:
        spacer = np.ones((img[0].shape[0], spacer_width), dtype=np.uint8) * spacer_grayscale
    else:
        spacer = np.ones((img[0].shape[0], spacer_width, img[0].shape[2]), dtype=np.uint8) * spacer_grayscale
        
    img_combined = img[0]
    for i in range(1, len(img)):
        img_combined = np.concatenate((img_combined, spacer, img[i]), axis=1)
    display_np(img_combined, scale, resampling)

####################################
# HISTOGRAM                        #
####################################
def img_histogram(image, exclude_black=False):
    histogram = np.zeros(256)
    for pixel_value in image.flatten().astype(np.uint8):
        histogram[pixel_value] += 1
    if exclude_black:
        result = [0] + histogram[1:] 
        result /= np.size(image) - histogram[0]
    else:
        result = histogram / np.size(image)
    return result

def equalize_image_histogram(image, exclude_black=False):
    # Get the image histogram
    image_hist = img_histogram(image, exclude_black)
    # Calculate the cumulative sum of the histogram
    cumulative_hist = np.cumsum(image_hist)
    # Create a function to map the image levels to the cumulative histogram values
    map_to_cdf = np.vectorize(lambda pixel_value: cumulative_hist[pixel_value] * 255)
    # Apply the mapping to the image and clip the result to the range [0, 255]
    equalized_image = np.clip(map_to_cdf(image), 0, 255).astype(np.uint8)
    # Return the equalized image
    return equalized_image


####################################
# CONTRAST                         #
####################################
def adjust_contrast(img, in_low, in_high, out_low, out_high, gamma=1):
    # Normalize the image by dividing each intensity value by (in_high - in_low)
    norm_img = (img - in_low) / (in_high - in_low)
    # Apply a power transformation with a power of gamma to the normalized image
    adj_img = norm_img ** gamma
    # Scale the image by multiplying it by (out_high - out_low) and adding out_low
    adj_img = adj_img * (out_high - out_low) + out_low
    return adj_img

def stretch_image_contrast(image, low_in=0.01, high_in=0.99, low_out=0.0, high_out=1.0):
    # Convert input and output limits to range [0, 255]
    in_low, in_high, out_low, out_high = low_in*255, high_in*255, low_out*255, high_out*255

    def map_intensity(intensity):
        if intensity < in_low:
            return adjust_contrast(intensity, 0, in_low, 0, out_low)
        elif intensity < in_high:
            return adjust_contrast(intensity, in_low, in_high, out_low, out_high)
        else:
            return adjust_contrast(intensity, in_high, 255, out_high, 255)

    # Vectorize the mapping function and apply it to each pixel of the image
    adjusted_image = np.vectorize(map_intensity)(image)
    
    return adjusted_image.astype(np.uint8)


####################################
# K-MEANS CLUSTERING               #
####################################
def kmeans_cluster(img, k):
    # reshape the image to a 2D array of pixels and 3 color values (RGB)
    pixel_values = img.reshape((-1, 3))
    # convert to float
    pixel_values = np.float32(pixel_values)

    # define stopping criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

    # number of clusters (K)
    _, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # convert back to 8 bit values
    centers = np.uint8(centers)
    # flatten the labels array
    labels = labels.flatten()
    # convert all pixels to the color of the centroids
    segmented_image = centers[labels.flatten()]
    # reshape back to the original image dimension
    segmented_image = segmented_image.reshape(img.shape)

    return segmented_image, labels

def kmeans_disable_clusters(img, labels, k, clusters):
    masked_image = np.copy(img)
    # convert to the shape of a vector of pixel values
    masked_image = masked_image.reshape((-1, 3))
    # color (i.e cluster) to disable
    for cluster in range(k):
        # disable the cluster number (turn the pixel into black)
        if cluster not in clusters:
            masked_image[labels == cluster] = [0, 0, 0]
            
    # convert back to original shape
    masked_image = masked_image.reshape(img.shape)

    return masked_image


####################################
# IMAGE SEGMENTATION AND FILTERING #
####################################
def get_pcb_silk_and_pads(img_pcb, light_green = (30, 120, 0), dark_green = (80, 255, 255), glitch_radius=20):
    hsv_pcb =  cv2.cvtColor(img_pcb, cv2.COLOR_RGB2HSV)
    mask_pads = cv2.inRange(hsv_pcb, light_green, dark_green)

    # Correct for small glitches and reflections
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(glitch_radius,glitch_radius))
    mask_pads  = cv2.dilate(mask_pads, kernel)
    mask_pads  = cv2.erode(mask_pads, kernel)

    pcb_silk = cv2.bitwise_and(img_pcb, img_pcb, mask=mask_pads)
    pcb_pads = cv2.bitwise_and(img_pcb, img_pcb, mask=cv2.bitwise_not(mask_pads))

    return pcb_silk, pcb_pads

def gray_smooth_pcb(img_pcb, blur_ksize=11):
    pcb_gray = cv2.cvtColor(img_pcb, cv2.COLOR_BGR2GRAY)
    pcb_silk_constrast = stretch_image_contrast(pcb_gray, low_in=0.01, high_in=0.5, low_out=0.0, high_out=1.0)
    pcb_silk_smooth = cv2.medianBlur(pcb_silk_constrast, blur_ksize)

    return pcb_silk_smooth
