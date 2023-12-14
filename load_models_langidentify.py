import sys
import numpy as np
import tensorflow as tf
import tokenization
import codecs
#from load_models_root import get_root
from typing import List, Optional
import attr
import ast


VERSION = 5.0


labels = ["as","bho","bn","en","gu","hi","ka","kn","ml","mni","mr","or","pa","ta","te","ur",'unk']

def load_online_model():
    model_path = 'langidentifyv1'
    return tf.saved_model.load(model_path)

models = {}


vocab_file = 'langidentifyv1/assets/vocab.txt'
tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file, do_lower_case=True, split_on_punc=False)

processor_text_fn = tokenization.convert_to_unicode


class InputExample(object):
    def __init__(self,
                 guid,
                 text_a,
                 text_b=None,
                 label=None,
                 weight=None,
                 example_id=None):
        self.guid = guid
        self.text_a = text_a
        self.text_b = text_b
        self.label = label
        self.weight = weight
        self.example_id = example_id


def convert_single_example(ex_index, example, max_seq_length, tokenizer):
    tokens_a = tokenizer.tokenize(example.text_a)
    tokens_b = None
    if example.text_b:
        tokens_b = tokenizer.tokenize(example.text_b)

    if tokens_b:
        _truncate_seq_pair(tokens_a, tokens_b, max_seq_length - 3)
    else:
        if len(tokens_a) > max_seq_length - 2:
            tokens_a = tokens_a[0:(max_seq_length - 2)]

    seg_id_a = 0
    seg_id_b = 1
    seg_id_cls = 0
    seg_id_pad = 0

    tokens = []
    segment_ids = []
    tokens.append("[CLS]")
    segment_ids.append(seg_id_cls)


    for token in tokens_a:
        tokens.append(token)
        segment_ids.append(seg_id_a)

    tokens.append("[SEP]")
    segment_ids.append(seg_id_a)

    if tokens_b:
        for token in tokens_b:
            tokens.append(token)
            segment_ids.append(seg_id_b)
        tokens.append("[SEP]")
        segment_ids.append(seg_id_b)

    input_ids = tokenizer.convert_tokens_to_ids(tokens)

    input_mask = [1] * len(input_ids)

    while len(input_ids) < max_seq_length:
        input_ids.append(0)
        input_mask.append(0)
        segment_ids.append(seg_id_pad)

    assert len(input_ids) == max_seq_length
    assert len(input_mask) == max_seq_length
    assert len(segment_ids) == max_seq_length

    return input_ids, input_mask, segment_ids, tokens_a


def pre_common(text):
    example = InputExample(guid="unused_id", text_a=text, text_b=None, label=None)
    sample = convert_single_example(1, example, 400, tokenizer)
    return sample

def predict_common(text, model, label):
    sample = pre_common(text)
    preds = model([tf.constant([sample[1]]), tf.constant([sample[2]]), tf.constant([sample[0]])])
    class_index = tf.math.argmax(preds, 1).numpy()
    output = label[class_index[0]]

    return output

model = load_online_model()
def _all(text):
    label = labels
    prediction = predict_common(text, model, label)
    return prediction


def print_start_sentence(sent_count):
    return '<Sentence id="'+str(sent_count)+'">'

def print_end_sentence():
    return '</Sentence>'
    

def language_identify(text):
    org_text = text
    text = text.replace('\u200d', '')
    text = text.replace('\u200b', '')
    text = text.replace('\u200d', '')
    text = text.replace('\u200e', '')
    text = " ".join(text.split())

    sentences = [text]
    output_list = []
    for sentence in sentences:
        p_all = _all(sentence)
        output_list.append(p_all)
        return output_list[0], 100

    
    return send


text = 'कल पुलिस ने सोनिया गांधी और राहुल गांधी के घरों को घेर लिया था।'
print (language_identify(text))



