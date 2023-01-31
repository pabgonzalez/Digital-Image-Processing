from collections import namedtuple
import cv2

KeyPoint = namedtuple('KeyPoint', ['xmin', 'xmax', 'ymin', 'ymax'])

class Score():
    def __init__(self, df):
        self.false_negative = set()
        self.true_positive = set()
        self.false_positive = set()
        for i in range(len(df)):
            self.false_negative.add(KeyPoint(
                xmin=df.iloc[i].xmin,
                xmax=df.iloc[i].xmax,
                ymin=df.iloc[i].ymin,
                ymax=df.iloc[i].ymax
            ))

    def isWithinLimits(self, x, y):
        for kp in self.false_negative.copy():
            if kp.xmin <= x and x <= kp.xmax and kp.ymin <= y and y <= kp.ymax:
                self.true_positive.add(kp)
                self.false_negative.remove(kp)
                return
        self.false_positive.add(KeyPoint(xmin=x, xmax=x, ymin=y, ymax=y))
    
    def checkKeyPoints(self, keypoints: list[cv2.KeyPoint]):
        for kp in keypoints:
            self.isWithinLimits(kp.pt[0], kp.pt[1])

    def getFScore(self, beta=1):
        tp = len(self.true_positive)
        fp = len(self.false_positive)
        fn = len(self.false_negative)
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        fscore = (1+beta**2) * (precision*recall) / ( beta**2 * precision + recall )
        return fscore