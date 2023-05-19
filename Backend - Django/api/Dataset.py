import torch.utils.data as data
import cv2
import sys
from os import listdir
from os.path import join
import numpy as np
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical


def resize_img(png_file_path):
        img_rgb = cv2.imread(png_file_path)
        img_grey = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        img_adapted = cv2.adaptiveThreshold(img_grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 101, 9)
        img_stacked = np.repeat(img_adapted[...,None],3,axis=2)
        resized = cv2.resize(img_stacked, (224,224), interpolation=cv2.INTER_AREA)
        bg_img = 255 * np.ones(shape=(224,224,3))
        bg_img[0:224, 0:224,:] = resized
        bg_img /= 255
        bg_img = np.rollaxis(bg_img, 2, 0)  
        return bg_img
    
def load_doc(filename):
    file = open(filename, 'r')
    text = file.read()
    file.close()
    return text

class Dataset():
    def __init__(self, data_dir, input_transform=None, target_transform=None):
        self.data_dir = data_dir
        self.image_filenames = []
        self.texts = []
        all_filenames = listdir(data_dir)
        all_filenames.sort()
        for filename in (all_filenames):
            if filename[-3:] == "png":
                self.image_filenames.append(filename)
            else:
                text = '<START> ' + load_doc(self.data_dir+filename) + ' <END>'
                text = ' '.join(text.split())
                text = text.replace(',', ' ,')
                self.texts.append(text)
        self.input_transform = input_transform
        self.target_transform = target_transform
        
        # Initialize the function to create the vocabulary 
        tokenizer = Tokenizer(filters='', split=" ", lower=False)
        # Create the vocabulary 
        tokenizer.fit_on_texts([load_doc('api/vocabulary.vocab')])
        self.tokenizer = tokenizer
        # Add one spot for the empty word in the vocabulary 
        self.vocab_size = len(tokenizer.word_index) + 1
        # Map the input sentences into the vocabulary indexes
        self.train_sequences = tokenizer.texts_to_sequences(self.texts)
        # The longest set of boostrap tokens
        self.max_sequence = max(len(s) for s in self.train_sequences)
        # Specify how many tokens to have in each input sentence
        self.max_length = 48
        
        X, y, image_data_filenames = list(), list(), list()
        for img_no, seq in enumerate(self.train_sequences):
            in_seq, out_seq = seq[:-1], seq[1:]
            out_seq = to_categorical(out_seq, num_classes=self.vocab_size)
            image_data_filenames.append(self.image_filenames[img_no])
            X.append(in_seq)
            y.append(out_seq)
                
        self.X = X
        self.y = y
        self.image_data_filenames = image_data_filenames
        self.images = list()
        for image_name in self.image_data_filenames:
            image = resize_img(self.data_dir+image_name)
            self.images.append(image)
