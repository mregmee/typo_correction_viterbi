from random import randint
randomize_alphabet = {'a':['q','w','s','z'],'b':['v','g','h','n'],'c':['x','d','f','v'],'d':['x','s','e','r','f','c'],'e':['w','s','d','r'],
                      'f':['d','r','t','g','v','c'],'g':['f','t','y','h','b','v'],'h':['g','y','u','j','n','b'],'i':['u','j','k','l','o'],
                      'j':['h','u','i','k','m','n'],'k':['j','i','o','l','m'],'l':['k','o','p'],'m':['n','j','k'],'n':['b','h','j','m'],
                      'o':['i','k','l','p'],'p':['o','l'],'q':['w','s','a'],'r':['e','d','f','t'],'s':['a','w','e','d','x','z'],
                      't':['r','f','g','y'],'u':['y','h','j','i'],'v':['c','f','g','b'],'w':['q','a','s','e'],'x':['z','s','d','c'],
                      'y':['t','g','h','u'],'z':['a','s','x']  
                     }

def getInput(file_name):    # read input file with file name as file_name and split and corrupt each files
    text1=open(file_name,'r+').read()
    training_text=open('training.txt','w+')
    test_text    =open('test.txt','w+')
    training_corrupt_text=open('training_corrupt.txt','w+')
    test_corrupt_text=open('test_corrupt.txt','w+')
    total_count = len(text1)
    training_count = int(0.8*total_count)
    test_count     = total_count-training_count
    char_count = 0
    with open(file_name) as f:
	  while True:
		c = f.read(1).lower()
		char_count = char_count+1
		if not c:
		  print "Splitting and corrupting done"
		  break
		if char_count<=training_count:
		    rand_int = randint(1,100)
		    training_text.write(c)            
		    if rand_int >= 1 and rand_int <= 20 and c.isalpha() :
		        c = corruptCharacter(c)
		    training_corrupt_text.write(c)
		else:
		    rand_int = randint(1,100)
		    test_text.write(c)
		    if rand_int >=1 and rand_int <=5 and c.isalpha() :
		        c = corruptCharacter(c)
		    test_corrupt_text.write(c)


		
def corruptCharacter(ch):
    list_replacing_alphabet = randomize_alphabet[ch.lower()];
    random_item = randint(0,len(list_replacing_alphabet)-1)
    #print random_item
    return list_replacing_alphabet[random_item];

getInput("unabom.txt")
#print corruptCharacter('z')
