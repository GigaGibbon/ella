#!/usr/bin/env python

import markovify
import re
import spacy
import sys
import os
import argparse
import json
import errno
import random

nlp = spacy.load("en")

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

parser = argparse.ArgumentParser()
parser.add_argument("config", help="The JSON config file to load.")
parser.add_argument("-r", "--refresh", help="Force a refresh of the corpora",
        action="store_true")

args = parser.parse_args()

config = {}
with open(args.config, 'r') as f:
    config = json.load(f)

bad_config = False
stanzas_missing = []

# Config handling and setup
def check_stanza(key, description):
    global bad_config, stanzas_missing
    if not key in config:
        bad_config = True
        stanzas_missing.append({'name':key, 'description':description})

check_stanza("main_corpus_source", "The path to the main corpus directory")
check_stanza("main_corpus_json", "The path to the main corpus JSON")
check_stanza("link_corpora_json_dir", "The path of the link corpora JSON files")
check_stanza("link_corpora", "The collection of link copora")
check_stanza("outputs", "The output for the raw text")

if bad_config:
    print("Error parsing config file!\n")
    print("The following stanzas were missing from the config file:\n")
    for st in stanzas_missing:
        print("\tstanza: '{0}'".format(st['name']))
        print("\t{0}\n".format(st['description']))
    sys.exit(1)

def load_corpus(json_file, fullpath):
    model = None
    if os.path.isfile(json_file) and not args.refresh:
        try:
            with open(json_file, 'r') as f:
                j = f.read()
            model = POSifiedText.from_json(j)
        except:
            print("Error parsing json file: {0}".format(json_file))
            print("Trying to load corpus, and JSON file invalid!")
            sys.exit(1)
    if model is None:
        # Okay, we load it from the directory
        for (dirpath, _, filenames) in os.walk(fullpath):
            for filename in filenames:
                with open(os.path.join(dirpath, filename)) as f:
                    m = POSifiedText(f, retain_original=False)
                if model:
                    model = markovify.combine(models=[model, m])
                else:
                    model = m

    return model

def save_corpus(json_file, model):
    j = model.to_json()
    with open(json_file, 'w') as f:
        f.write(j)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass

# Load corpora
#--------------
main_model = load_corpus(config['main_corpus_json'],config['main_corpus_source'])
link_corpora = {}
for k in config['link_corpora']:
    n = k['name']
    jf = os.path.join(config['link_corpora_json_dir'], '{0}.json'.format(n))
    fp = k['source']
    model = load_corpus(jf, fp)
    link_corpora[n] = model

# Save corpora
#--------------
save_corpus(config['main_corpus_json'], main_model)
for k in config['link_corpora']:
    n = k['name']
    jf = os.path.join(config['link_corpora_json_dir'], '{0}.json'.format(n))
    save_corpus(jf, link_corpora[n])

# Make the stuff
#----------------
for outs in config['outputs']:
    print("Processing output: {0}".format(outs['name']))
    mkdir_p(outs['out_dir'])
    num_sent = random.randint(
            outs['min_max']['sent_per_para'][0],
            outs['min_max']['sent_per_para'][1])
    num_para = random.randint(
            outs['min_max']['para_per_page'][0],
            outs['min_max']['para_per_page'][1])
    num_page = random.randint(
            outs['min_max']['pages'][0], outs['min_max']['pages'][1])
    page_count = 0
    while page_count < num_page:
        page_count += 1
        para_count = 0
        page_filename = os.path.join(outs['out_dir'],
                "page_{0}.html".format(page_count))
        with open(page_filename, 'w') as f:
            while para_count < num_para:
                para_count += 1
                f.write('<p>')
                sent_count = 0
                while sent_count < num_sent:
                    sent_count += 1
                    # FIXME Logic for links
                    sent = main_model.make_sentence()
                    f.write(sent)
                f.write('</p>\n\n')
