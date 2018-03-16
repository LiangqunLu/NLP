#!/home/llu/anaconda3/bin/python

'''
1. Extract from the BROWN file all grammar rules embedded in parse
   trees. Do not consider punctuation as a nonterminal. Eliminate
   numbers attached to non-terminals such as '-1', '-2', etc. Report 
   how many distinct rules you found, what are the 10 most frequent
   rules regardless of the non-terminal on the left-hand side, and
   what is the non-terminal with the most alternate rules (i.e. the
   non-terminal that can have most diverse structures). [20 points]

2. Try to estimate how large the above grammar would be if you were to
   lexicalize it, i.e. to add head words to some of the rules. Work
   with your own assumptions. The important part for this problem is
   your general reasoning and not the details. [20 points]   
   
'''
import os, sys
import re
from collections import Counter
import nltk

def grammar_each_tree(test):
    
    output = list()
    test = re.sub('\s+', ' ', test.strip())
    ss =  re.findall("\([^\(\)]*\)", test)
    
    for m in range(len(ss)):
        arr = ss[m].split(' ')
        left = arr[0].replace("(", "")    
        test = test.replace(ss[m], left)
    
    while len(re.findall("\([^\(\)]*\)", test)) > 0:
    
        test = re.sub('\s+', ' ', test.strip())
        ss =  re.findall("\([^\(\)]*\)", test)
    
        for m in range(len(ss)):
            arr = ss[m].split(' ')
            left = arr[0].replace("(", "")
            left = re.sub("-\d+", "", left)
            add_list = [arr[i].replace(")", "") for i in range(1, len(arr)) if re.search('[a-zA-Z]', arr[i]) and 'NONE' not in arr[i]]
            add_list = [re.sub("-\d+", "", one) for one in add_list]
            
            if re.search('[a-zA-Z]', left) and len(add_list) > 0:
                
                add_list = left + " -> " + ' '.join(add_list)
                #add_list = [one for one in add_list if 'TOP' not in one and re.search('[a-zA-Z]', one[0]) and 'NONE' not in one]
                output.append(add_list) 
            
            test = test.replace(ss[m], left)

    output = output[::-1]
    output = [one for one in output if 'TOP' not in one]
    print(output)
    return(output)
    

def obtain_grammar(infile = "../dataset/BROWN.pos.all"):

    infile = "../dataset/BROWN.pos.all"    
    ff = open(infile, 'r')
    content = ff.read()    
    content = content.replace("\n", "")
        
    treefiles = content.replace("(TOP END_OF_TEXT_UNIT)", "\n")
    treefiles = treefiles.split("\n")
    treefiles = [one for one in treefiles if one != ""]
    
    ##generate the grammar list
    grammar_list = list()
    for i in range(len(treefiles)):
        test = treefiles[i]
        grammar_list = grammar_list + grammar_each_tree(treefiles[i])

    ## distinct grammar rules
    print("The number of distinct grammar rules:")
    print(len(set(grammar_list)))    
    
    ## count the highly frequent elements    
    grammar_frq = Counter(grammar_list)
    print("The top 10 frequent grammars are:")
    print(grammar_frq.most_common(10))

    ###Question 2
    grammar_str = " ".join(grammar_list)
    grammar_str = grammar_str.replace("->", " ")
    set(grammar_str.split(" "))
    len(set(grammar_str.split(" "))  ) #71
    
    ## count the sentence length
    grammar_len = list()
    for i in range(len(treefiles)):
        #t = nltk.Tree.fromstring(treefiles[i])
        #tmp_list = [" ".join(one[::-1]) for one in t.pos()]
        POS = [p.split(')')[0] for p in treefiles[i].split('(') if ')' in p]
        #tmp_list = " ".join(POS)
        #out_list.append(tmp_list) 
        grammar_len.append(len(POS))
    
    avg = sum(grammar_len)/len(grammar_len)
    # 23.52966159216523
    
obtain_grammar(infile = "../dataset/BROWN.pos.all")



