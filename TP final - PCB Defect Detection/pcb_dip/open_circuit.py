import cv2
import numpy as np
from scipy.signal import find_peaks
from .pcb_dip_tools import img_histogram, get_pcb_silk_and_pads, gray_smooth_pcb

def get_open_circuit_keypoints_from_smooth(img_pcb, ignore_border=120, debug_mode=False):
    peaks,_ = find_peaks(img_histogram(img_pcb), distance = 25, prominence = 0.01)

    pcb_binary = cv2.threshold(img_pcb, (peaks[0]+peaks[-1])/2, 255, cv2.THRESH_BINARY)[1]

    kernel = np.ones((3, 3), dtype=np.uint8)
    img_eroded  = cv2.erode(pcb_binary, kernel)

    kernel = np.ones((25, 25), dtype=np.uint8)
    img2  = cv2.dilate(img_eroded, kernel)
    img2  = cv2.erode(img2, kernel)

    kernel = np.ones((10, 10), dtype=np.uint8)
    img3  = cv2.erode(img2-img_eroded, kernel)

    inner_mask = np.zeros_like(img3)
    inner_mask[ignore_border:inner_mask.shape[0]-ignore_border,ignore_border:inner_mask.shape[1]-ignore_border] = True
    img3 = img3 * inner_mask

    # Set up the detector with parameters.
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 2
    
    params.filterByCircularity = True
    params.minCircularity = 0.001
    
    params.filterByConvexity = True
    params.minConvexity = 0.01
    
    params.filterByInertia = True
    params.minInertiaRatio = 0.001
    detector = cv2.SimpleBlobDetector_create(params)
    
    # Detect blobs.
    keypoints = detector.detect(cv2.bitwise_not(img3))

    if debug_mode:
        return keypoints, [pcb_binary, img_eroded, img2, img3]
    return keypoints


def get_open_circuit_keypoints(img_pcb):
    pcb_silk, _ = get_pcb_silk_and_pads(img_pcb, glitch_radius=20)
    pcb_silk_smooth = gray_smooth_pcb(pcb_silk) 
    keypoints = get_open_circuit_keypoints_from_smooth(pcb_silk_smooth)
    return keypoints