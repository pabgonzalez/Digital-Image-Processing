import cv2
from .pcb_dip_tools import get_pcb_silk_and_pads, gray_smooth_pcb

def get_missing_hole_keypoints_from_smooth(img_pcb, ignore_border=120):
    pcb_binary = cv2.threshold(img_pcb, 1, 255, cv2.THRESH_BINARY)[1]

    # Set up the detector with parameters.
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 5
    params.maxArea = 10000

    params.filterByCircularity = True
    params.minCircularity = 0.1

    params.filterByConvexity = True
    params.minConvexity = 0.1

    params.filterByInertia = True
    params.minInertiaRatio = 0.01
    detector = cv2.SimpleBlobDetector_create(params)

    # Detect blobs.
    keypoints = detector.detect(pcb_binary)

    return keypoints


def get_missing_hole_keypoints(img_pcb):
    _, pcb_pads = get_pcb_silk_and_pads(img_pcb, glitch_radius=1)
    pcb_pads_smooth = gray_smooth_pcb(pcb_pads)
    keypoints = get_missing_hole_keypoints_from_smooth(pcb_pads_smooth)
    return keypoints
