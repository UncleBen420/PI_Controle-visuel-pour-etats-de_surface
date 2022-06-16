import numpy
#Load model
import pickle
#from keras.models import load_model
# Granulometry
from skimage import data
from skimage import filters
from skimage import exposure
from scipy import ndimage

#labelling
from skimage.morphology import label

import numpy as np
import cv2

class Granulometry:
    def __init__(self, minDisc=1, maxDisc=30, growth=1):
        self.sizes = range(minDisc, maxDisc, growth)
        nb = int((maxDisc - minDisc) / growth)
        self.granulo = np.zeros(nb)


    def disk_structure(self, n):
        struct = np.zeros((2 * n + 1, 2 * n + 1))
        x, y = np.indices((2 * n + 1, 2 * n + 1))
        mask = (x - n)**2 + (y - n)**2 <= n**2
        struct[mask] = 1
        return struct.astype(bool)


    def granulometry(self, data):
        s = max(data.shape)
        if self.sizes is None:
            self.sizes = range(1, s/2, 2)
        self.granulo = [ndimage.binary_opening(data, structure=self.disk_structure(n)).sum() for n in self.sizes]
        return self.granulo

    def granulometry_with_step(self, data):
        s = max(data.shape)
        if self.sizes is None:
            self.sizes = range(1, s/2, 2)

        i = 0
        for n in self.sizes:
            print(i)
            opened = ndimage.binary_opening(data, structure=self.disk_structure(n))
            self.granulo[i] = opened.sum()
            plt.imshow(data, cmap=plt.cm.gray)
            plt.contour(opened, [0.5], colors='b', linewidths=2)
            plt.show()
            i += 1

        return self.granulo

    def plot_granulo(self):
        plt.plot(self.sizes, self.granulo, 'ok', ms=8)
        plt.show()

class Model:
    def __init__(self, class_model="classification_lda.pkl", pca_model="pca.pkl", reg_model="regression_linear.pkl", gran_mm="granuloMinMax.pkl",  labl_mm="labelMinMax.pkl"):
        with open(pca_model, 'rb') as file:
            self.pca_model = pickle.load(file)

        with open(class_model, 'rb') as file:
            self.classification_model = pickle.load(file)

        with open(gran_mm, 'rb') as file:
            self.gran_mm = pickle.load(file)

        with open(labl_mm, 'rb') as file:
            self.labl_mm = pickle.load(file)

        with open(reg_model, 'rb') as file:
            self.regression_model = pickle.load(file)

	# for keras
        #self.regression_model = load_model(reg_model)

        self.granulometry = Granulometry(1, 20, 2)
        print(self.classification_model)
        print(self.pca_model)
        print(self.regression_model)

    def rescale(self, x):
        return x / 255.

    def preprocessImage(self, image):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
        erode = cv2.erode(image,kernel)
        image = image - erode
        image = cv2.resize(image, (320,256))
        self.image = self.rescale(image)

    def extractData(self):
        val = filters.threshold_otsu(self.image)
        image_otsu = self.image < val

        #labeling
        label_image = label(image_otsu, connectivity=2)
        labelling = np.array(len(np.unique(label_image)))
        granulo = np.array(self.granulometry.granulometry(image_otsu))
        granulo = self.gran_mm.transform(granulo.reshape(1,-1))
        labelling = self.labl_mm.transform(labelling.reshape(1,-1))
        X = np.append(granulo,labelling,axis=1)
        self.X = self.pca_model.transform(X)


    def predict(self, image):
        self.preprocessImage(image)
        self.extractData()
        pred_reg = self.regression_model.predict(self.X)
        pred_cla = self.classification_model.predict(self.X)
        return pred_reg[0][0], pred_cla[0]
