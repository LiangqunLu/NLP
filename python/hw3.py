#!/home/llu/anaconda3/bin/python
'''
1. Build a baseline statistical tagger.

(i) [10 points] Use the assignment#2's hash of hashes to train a
baseline lexicalized statistical tagger on the entire BROWN corpus.

(ii) [20 points] Use the baseline lexicalized statistical tagger to tag 
all the words in the SnapshotBROWN.pos.all.txt file. Evaluate and report the
performance of this baseline tagger on the Snapshot file.

(iii) [20 points] add few rules to handle unknown words for the tagger
   in (ii). The rules can be morphological, contextual, or of other
   nature. Use 25 new sentences to evaluate this tagger (the (ii) tagger +
   unknown word rules). You can pick 25 sentences from a news article
   from the web and report the performance on those.

NOTE: You should only consider the 45 proper tags from Penn Treebank
tagset (available in the slides). You should disregard tags such as
-NONE-, etc.

'''
import os, sys
import re
from collections import Counter
sys.path = [''] + sys.path
from hw2 import get_hash, get_clean 

####I
output_dict = get_hash(filename = "../dataset/BROWN-clean.pos.txt")
get_lines = get_clean(filename = "../dataset/SnapshotBROWN.pos.all.txt")

print(output_dict)

#####II
def eval_snapshot(dicfile = output_dict, fileline = get_lines):
    
    strline = " ".join(fileline)
    true_tags = strline.split(" ")[::2]
    words = strline.split(" ")[1::2]
    
    tag_w = []
    for w in words:
        v = output_dict[w]
        tag = max(v, key = v.get)
        tag_w.append(tag)        

    count = [true_tags[i] == tag_w[i] for i in range(len(true_tags))]           
    accuracy = count.count(True)/len(true_tags)
    print(count.count(True), len(true_tags))
    print("SnapshotBROWN accuracy:", accuracy)

    return(accuracy)

#get_lines = get_clean(filename = "BROWN.pos.all") 
accuracy = eval_snapshot(dicfile = output_dict, fileline = get_lines) 

############III
def nltk_tag(file = "../dataset/25sentences.txt"):
    import nltk
    from nltk import word_tokenize
    
    ff = open(file, "r")
    content = ff.read()
    content = content.replace("\n", " ")
    text = word_tokenize(content)
    tag_nltk = nltk.pos_tag(text)
    
    return(tag_nltk)    
 
def modify_tag(output_dict):
    
    tag_nltk = nltk_tag()
    words = [one[0] for one in tag_nltk]
    true_tags = [one[1] for one in tag_nltk]
    
    ##baseline tag
    tag_baseline = list()
    for w in words:
        if w in output_dict:
            v = output_dict[w]
            tag = max(v, key = v.get)
            tag_baseline.append(tag) 
        else:
            tag = "None"
            tag_baseline.append(tag) 

    count = [ true_tags[i] == tag_baseline[i] for i in range(len(true_tags))]           
    accuracy = count.count(True)/len(true_tags)
    print(count.count(True), len(true_tags))
    print("baseline accuracy:", accuracy)
    
    ##modify the tags from training in BROWN file
    Penn_TagSet = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "POS", "PP", "PP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "WDT", "WP", "WP$", "WRB", "$", "/", "'", "(", ")", ",", ".", ":"]
    
    tags = [list(output_dict[one].keys()) for one in output_dict.keys()]
    
    tag_uniq = list()
    for one in tags:
        tag_uniq.extend(one)

    tag_uniq = list(set(tag_uniq))
    tag_uniq = [ one for one in tag_uniq if one in Penn_TagSet]
    
    ##
    tag_tager_test = list()
    for w in words:
        if w in output_dict:
            v = output_dict[w]
            tag = max(v, key = v.get)
            tag_tager_test.append(tag)
        elif w not in output_dict:
            if w[0].isupper():
                tag_tager_test.append("NN")
            elif w.isnumeric():
                tag_tager_test.append("CD")    
            else: 
                tag_tager_test.append("None")
            
    count = [ true_tags[i] == tag_tager_test[i] for i in range(len(true_tags))]           
    accuracy = count.count(True)/len(true_tags)
    print(count.count(True), len(true_tags))
    print("tag_tager_test accuracy:", accuracy)               
               
modify_tag(output_dict)    

