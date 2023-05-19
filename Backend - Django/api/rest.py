import torch.utils.data as data
import cv2
import sys
from os import listdir
from os.path import join
import numpy as np
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu

from .Dataset import *
from .EncoderCNN import *
from .DecoderRNN import *
from .inference.Compiler import *

def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None


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


def Upload(image_path, my_dateset, encoder, decode):
	img = resize_img(image_path)
	all_pred = []
	decoded_words = []
	star_text = '<START> '
	hidden = decoder.init_hidden()
	image = Variable(torch.FloatTensor([img]))
	predicted = '<START> '
	for di in range(9999):
    		sequence = my_dateset.tokenizer.texts_to_sequences([star_text])[0]
    		decoder_input = Variable(torch.LongTensor(sequence)).view(1,-1)
    		features = encoder(image)
    		outputs,hidden = decoder(features, decoder_input,hidden)
    		topv, topi = outputs.data.topk(1)
    		ni = topi[0][0][0]
    		word = word_for_id(ni,my_dateset.tokenizer)
    		if word is None:
       			continue
    		predicted += word + ' '
    		star_text = word
    		if word == '<END>':
       			break
  
	gui = ' '.join(predicted.split())
	gui = gui.replace(',', ' ,')
	gui = gui.split()
	gui.remove('<START>')
	gui.remove('<END>')
	all_pred.append(gui)
	return all_pred


def normalized_gui(original_gui, generated_gui):
    # Predicted images don't have color so we normalize all buttons to btn-orange or btn-active
    btns_to_replace = ['btn-green', 'btn-red']
    normalized_original_gui = ['btn-orange' if token in btns_to_replace else token for token in original_gui]
    normalized_original_gui = ['btn-active' if token == 'btn-inactive' else token for token in normalized_original_gui]
    normalized_generated_gui = ['btn-orange' if token in btns_to_replace else token for token in generated_gui]
    normalized_generated_gui = ['btn-active' if token == 'btn-inactive' else token for token in normalized_generated_gui]
    return normalized_original_gui, normalized_generated_gui


def gen_html(predicted, name, i):
    compiler = Compiler('default')
    compiled_website = compiler.compile(predicted)
    # print(compiled_website)
    text_file = open(name+".html", "w")
    n = text_file.write(compiled_website)
    text_file.close()


# dataset directory given here
dir_name = 'data/training/'
batch_size = 32
my_dateset = Dataset(dir_name)

embed_size = 50
hidden_size = 256
num_layers = 3
num_epochs = 30

encoder = EncoderCNN(embed_size)
decoder = DecoderRNN(embed_size, hidden_size, my_dateset.vocab_size, num_layers)
criterion = nn.MSELoss()
params = list(decoder.parameters()) + list(encoder.linear.parameters()) + list(encoder.bn.parameters())
optimizer = torch.optim.Adam(params,lr=0.001)

encoder = torch.load('model_weights/encoder_resnet34_tensor(0.0643).pt')
decoder = torch.load('model_weights/edecoder_resnet34_tensor(0.0643).pt')

pred = Upload(img_p, my_dataset, encoder, decoder)
gen_html(pred, file_name)