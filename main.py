import viterbi
import corrupt
import mle

def calc_Recall_Precision(original_word,corrupted_word,corrected_word):
    no_crptd_char =0
    no_viterbi_crctd_char =0
    no_true_crctd_char =0
    for i in range(0,len(original_word)):
        if original_word[i] != corrupted_word[i]: 
           no_crptd_char += 1
        if corrupted_word[i] != corrected_word[i]:
           no_viterbi_crctd_char +=1
        if original_word[i] == corrected_word[i] and original_word[i] != corrupted_word[i] :
           no_true_crctd_char +=1
    return (no_crptd_char,no_viterbi_crctd_char,no_true_crctd_char)

def runViterbi(test_crpt_file_name,test_file_name):
    mle.calcProbabilty('training.txt','training_corrupt.txt')
    output_test_file = open('output_orig_crpt_crctd.txt','w+')
    recall_precision_file = open('recall_precision_stat.txt','w+')
    test_crpt_file = open(test_crpt_file_name,'r+')
    test_crpt_file_words = mle.words(test_crpt_file)
    test_file = open(test_file_name,'r+')
    test_file_words = mle.words(test_file)
    #observations = ('w','o','r','l','d')
    total_corrupted_char =0
    total_veterbi_crctd_char =0
    total_true_crctd_char =0
    total_characters =0
    for j in range(0,len(test_crpt_file_words)-1):
        word = test_crpt_file_words[j]
        word_original = test_file_words[j]
        if not word.isalpha():
           continue
        observations = ()
        word_char_list = []
        orig_word   =()
        orig_word_char_list = []
        for i in range (0,len(word)):
            word_char_list.append(word[i])
            orig_word_char_list.append(word_original[i])
        observations = tuple(word_char_list)
        orig_word = tuple(orig_word_char_list)
        output_test_file.write(word_original+'\t')
        print word_original
        print "".join(observations)
        output_test_file.write("".join(observations)+'\t')
        corrected_word = viterbi.viterbi(observations,
               mle.states,
               mle.start_probability,
               mle.transition_probability,
               mle.emission_probability)
        print "".join(corrected_word)
        output_test_file.write("".join(corrected_word)+'\n')
        recall_precision_stat = calc_Recall_Precision(orig_word,observations,corrected_word)
        total_characters += len(orig_word)
        total_corrupted_char += recall_precision_stat[0]
        total_veterbi_crctd_char += recall_precision_stat[1]
        total_true_crctd_char += recall_precision_stat[2]
        #recall_precision_file.write(str(j+1)+'\t'+str(total_corrupted_char)+'\t'+str(total_veterbi_crctd_char)+'\t'+str(total_true_crctd_char)+'\n')
    recall_precision_file.write(str(total_characters) +'\t'+str(total_corrupted_char)+'\t'+str(total_veterbi_crctd_char)+'\t'+str(total_true_crctd_char)+'\n') 
runViterbi('test_corrupt.txt','test.txt')

