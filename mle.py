import operator
import math
states = ('a', 'b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
 
start_probability = {}
 
transition_probability = {}
 
emission_probability = {   }

def words(fileobj):
    word_list=[]
    for line in fileobj:
        for word in line.split():
             word_list.append(word)
    return word_list


def calcProbabilty(training_file,training_corrupt_file):
    
    traing_file = open(training_file,'r+')
    traing_crpt_file = open(training_corrupt_file,'r+')
    traing_file_words = words(traing_file)
    traing_crpt_file_words = words(traing_crpt_file)
    total_words  = 0
    start_probab = {}
    trans_probab = {}
    emission_probab = {}
    for i in range(0,len(traing_file_words)-1):        
        ch_first = traing_file_words[i][0]
        if not ch_first.isalpha():
           continue
        total_words = total_words+1
        if ch_first in start_probab:
            start_probab[ch_first] = start_probab[ch_first] +1 
        else:
            start_probab[ch_first]=1
        ch_orig  = ch_first
        ch_crpt  = traing_crpt_file_words[i][0]
        for j in range(1,len(traing_file_words[i])):         
            ch_orig_next = traing_file_words[i][j]
            ch_crpt_next = traing_crpt_file_words[i][j]
            if not ch_orig_next.isalpha():
                continue
            if (ch_orig,ch_orig_next) in trans_probab:
               trans_probab[(ch_orig,ch_orig_next)] = trans_probab[(ch_orig,ch_orig_next)]+1
            else:
               trans_probab[(ch_orig,ch_orig_next)] =1
            if not ch_orig_next.isalpha():
                continue
            if (ch_orig,ch_crpt) in emission_probab:
               emission_probab[(ch_orig,ch_crpt)] = emission_probab[(ch_orig,ch_crpt)]+1
            else:
               emission_probab[(ch_orig,ch_crpt)] =1
            ch_orig = ch_orig_next
            ch_crpt = ch_crpt_next
    start_chars = start_probab.keys()
    total_probab = 0
    for start_char in states:
        if start_char not in start_probab:
            start_probability[start_char] = math.log(float(1)/(total_words+26)) 
            total_probab += float(1)/(total_words+26) 
        else: 
            start_probability[start_char] = math.log(float(start_probab[start_char]+1)/(total_words+26))
            total_probab += float(start_probab[start_char]+1)/(total_words+26)
    
    sorted_trans_probab = sorted(trans_probab.iteritems(), key=operator.itemgetter(0))
    sorted_emission_probab = sorted(emission_probab.iteritems(), key=operator.itemgetter(0))
    state_prev = sorted_trans_probab[0][0][0]
    tot_trans_state=0
    temp_dict = {}
    for trans_tup in sorted_trans_probab:
        state_next = trans_tup[0][0]
        trans_char = trans_tup[0][1]
        if state_prev == state_next:
           tot_trans_state += trans_tup[1]
           temp_dict[trans_char] = float(trans_tup[1])
        else:
               for char in states:
                   if char not in temp_dict.keys(): 
                       temp_dict[char] = math.log(float(1)/(tot_trans_state+26))
                   else:
                        temp_dict[char] = math.log(float(temp_dict[char]+1)/(tot_trans_state+26))
               transition_probability[state_prev] = temp_dict
               temp_dict = {}
               state_prev = state_next
               #print 'state prev is' + state_prev + 'state next is' + state_next +  'and total is' +  tot_trans_state
               tot_trans_state = 0
               tot_trans_state += trans_tup[1]
               temp_dict[trans_char] = float(trans_tup[1])
    for char in states: 
        if char not in temp_dict.keys(): 
             temp_dict[char] = math.log(float(1)/(tot_trans_state+26))
        else:
             temp_dict[char] = math.log(float(temp_dict[char]+1)/(tot_trans_state+26))
    transition_probability[state_prev] = temp_dict   

    # calculate emission probability
    state_prev = sorted_emission_probab[0][0][0]
    tot_emission_state=0
    temp_dict = {}
    for emission_tup in sorted_emission_probab:
        state_next = emission_tup[0][0]
        emission_char = emission_tup[0][1]
        if state_prev == state_next:
           tot_emission_state += emission_tup[1]
           temp_dict[emission_char] = float(emission_tup[1])
        else:
               for char in states: 
                   if char not in temp_dict.keys():
                       temp_dict[char] = math.log(float(1)/(tot_emission_state+26))
                   else: 
                       temp_dict[char] = math.log(float(temp_dict[char]+1)/(tot_emission_state+26))
               emission_probability[state_prev] = temp_dict
               temp_dict = {}
               state_prev = state_next
               #print 'state prev is' + state_prev + 'state next is' + state_next +  'and total is' +  tot_trans_state
               tot_emission_state = 0
               tot_emission_state += emission_tup[1]
               temp_dict[emission_char] = float(emission_tup[1])
    for char in states: 
        if char not in temp_dict.keys():
            temp_dict[char] = math.log(float(1)/(tot_emission_state+26))
        else: 
             temp_dict[char] = math.log(float(temp_dict[char]+1)/(tot_emission_state+26))
    emission_probability[state_prev] = temp_dict  
    #sorted(trans_probab, key=lambda key: trans_probab[key][1])
    #print start_probability
    #print total_probab
    #print sorted_trans_tup
    #print sorted_emission_probab
    #for state_char in states:
       #print sum(emission_probability[state_char].values())
def writeHMMtoFile(states,start_probability,emission_probability,transition_probability):
    hmm_file = open('hmm.txt','w+')
    hmm_file.write('states\n')
    hmm_file.write(str(len(states)))
    hmm_file.write('\nInitialProbability '+str(len(start_probability)))
    start_keys = start_probability.keys()
    for start_key in start_keys:       
        hmm_file.write('\n'+start_key+' '+str(start_probability[start_key]))
    output_prob_count = 0
    emission_keys = emission_probability.keys()
    for emission_key in emission_keys:
        emitted_keys = emission_probability[emission_key].keys()
        for emitted_key in emitted_keys:
            output_prob_count  = output_prob_count+1;
            #hmm_file.write('\n'+emission_key+' '+emitted_key+' '+str(emission_probability[emission_key][emitted_key]))
    hmm_file.write('\nOutputProbability '+str(output_prob_count))
    transition_keys = transition_probability.keys()
    for emission_key in emission_keys:
        emitted_keys = emission_probability[emission_key].keys()
        for emitted_key in emitted_keys:
            #output_prob_count  = output_prob_count+1;
            hmm_file.write('\n'+emission_key+' '+emitted_key+' '+str(emission_probability[emission_key][emitted_key]))
    transition_prob_count = 0
    for transition_key in transition_keys:
        transmitted_keys = transition_probability[transition_key].keys()
        for emitted_key in transmitted_keys:
            transition_prob_count  = transition_prob_count+1;
            #hmm_file.write('\n'+transition_key+' '+emitted_key+' '+str(transition_probability[transition_key][emitted_key]))
    hmm_file.write('\nTransitionProbability '+str(transition_prob_count))
    transition_keys = transition_probability.keys()
    for transition_key in transition_keys:
        transmitted_keys = transition_probability[transition_key].keys()
        for transmitted_key in transmitted_keys:
            #output_prob_count  = output_prob_count+1;
            hmm_file.write('\n'+transition_key+' '+transmitted_key+' '+str(transition_probability[transition_key][transmitted_key]))
    
calcProbabilty('training.txt','training_corrupt.txt')
writeHMMtoFile(states,start_probability,emission_probability,transition_probability)


         
   
