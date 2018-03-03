#!/home/llu/anaconda3/bin/python

'''
1. Write a Perl script that creates a hash of hashes containing words, their
   parts-of-speech tags (POSes), and frequencies of the tags for the corresponding
   words from an expert-annotated text file. Assume the words in the file
   have been manually annotated by experts with POS tags. Keys for the first
   level of hash should be the words while the values are hashes. The second
   level of hashing uses the POSes as keys and the values are the frequencies
   of the POSes for the corresponding words.
   dict[word] = {POS:freq}

(i) [10 points] Write a Perl script that maps each parse tree in the
   SnapshotBROWN.pos.all.txt file (see the website) into one-line
   sentences as shown below. You should retain only the parts-of-speech
   and the words from the parse trees. Each sentence should span a single
   line in the outpute file.

Example Output

DT The NNP Fulton NNP County NNP Grand NNP Jury VBD said NNP Friday DT
an NN investigation ... rest of the sentence here 

Run the script on the file SnapshotBROWN.pos.all.txt and save the
result in BROWN-clean.pos.txt

(ii) [10 points] Generate the hash of hashes from the clean file BROWN-clean.pos.txt .

(iii) [10 points] In BROWN-clean.pos.txt detect the 20 most frequent
tags. Report their frequency.

(iv) [10 points] take the most frequent tag and use it to
   tag the words in all the sentences from the BROWN-clean.pos.txt file. 
   Report the performance of this tagger. See the slides for details on 
   how to measure the performance.
'''

import os, sys
import re
from collections import Counter
#import nltk

def get_clean(filename = "../dataset/BROWN.pos.all"):
    
    ff = open(filename, "r")
    content = ff.read()
    content = content.replace("\n", "")
    
    treefiles = content.replace("(TOP END_OF_TEXT_UNIT)", "\n")
    treefiles = treefiles.split("\n")
    treefiles = [one for one in treefiles if one != ""]
    
    out_list = []
    for one in range(len(treefiles)):
        #t = nltk.Tree.fromstring(treefiles[one])
        #print(t.flatten())
        #tmp_list = [" ".join(one[::-1]) for one in t.pos()]
        #out_list.append(" ".join(tmp_list))
        POS = [p.split(')')[0] for p in treefiles[one].split('(') if ')' in p]
        tmp_list = " ".join(POS)
        out_list.append(tmp_list)
    
    #oout = open("BROWN-clean.pos.txt", "w")  
    #for n in out_list:
        #oout.write(n + "\n")
    
    #return("get clean file first")        
    return(out_list)
    
def get_hash(filename = "../dataset/BROWN-clean.pos.txt"):
    
    get_clean()
    
    ff = open(filename, "r")
    content = ff.read()    
    content = content.replace("\n", " ")
    content = content.split(" ")
    content = content[:-1]

    ###ii
    output_dict = {}
    for i in range(int(len(content)/2)):
        pos = content[2*i]
        word = content[2*i + 1]
            
        if word not in output_dict:
            output_dict[word] = {pos:1}
        else:
            if pos not in output_dict[word]:
                output_dict[word][pos] = 1
            else:
                output_dict[word][pos] += 1
            
    ###iii        
    poses = content[::2]
    pos_frq = Counter(poses)
    print("The top 20 frequent POSes are:")
    print(pos_frq.most_common(20))

    ###iv
    words = content[1::2]
    ##get the most tag for each word
    tag_w_top = []
    tag_w_all = poses ##right tag
    for w in words:
        v = output_dict[w]
        tag = max(v, key = v.get)
        tag_w_top.append(tag)
    
    count = 0
    for i in range(len(tag_w_all)):
        if tag_w_top[i] == tag_w_all[i]:
            count +=1
    
    print(count, len(tag_w_all))
            
    print("Performance based on the top tage for each word:")
    acc = count/len(tag_w_all)
    print(acc)
    
    return(output_dict)
    
    
#get_hash()
        
    


