import re
#initialise variables

global pos_count # count of sentences with positive tags
global neg_count #count of sentences with neagative tags
global pos_words # total number of positive words
global neg_words # total number of negative words
global total # total number of sentences. 
global freq # dictionary that stores the frequency and label for each word
global pos_prob # temporary array that stores the probabilities of words being positive in a sentence
global neg_prob # temporary array that stores the probabilities of words being negative in a sentence
global correct       # number of correctly assigned labels
global incorrect     # number of incorrectly assigned labels 

 
# tokenizer function
def tokenize(string):
    #removing addresses in the begining of the tweets
    string=re.sub('@[\w\']*','',string)
    #replacing n't with not
    string=re.sub('n\'t',' not',string)
    #remove URLs
    string=re.sub('\bhttp://[\w\.-/&%$#]*','',string)
    #removing sprecial characters
    string=re.sub('[\*\$&\(\)#;:,%"]+',' ',string)
    #replace mutliple occurance of the punctuations with a single one
    string=re.sub('[\.]+',' .',string)
    string=re.sub('[\?]+',' ?',string)
    string=re.sub('[!]+',' !',string)
    #remove spaces in the begining and end of the sentence
    string= re.sub('^\s*|\s$','', string)
    string =re.sub('\s+',' ',string)
    return string

# calculate probability
def calc_probability(words):
    positive=pos_prob    # probability of the tweet being posiitve
    negative=neg_prob    # probability of the tweet being negative

    #calulate the positive probability
    for w in words:
        if w in freq.keys():
            if '1' in freq[w]:   #calulate the probability of the word being positive   
                a=(freq[w]['1']+1)/(pos_words+(1*vocab))
            else:  
                a=(0+1)/(pos_words+(1*vocab))
            if '0' in freq[w]:  #calulate the probability of the word being negative
                b=(freq[w]['0']+1)/(neg_words+(1*vocab))
            else:                       
                b=(0+1)/(neg_words+(1*vocab))
        else:   
            a=1/(pos_words+(1*vocab))
            b=1/(neg_words+(1*vocab))
        positive=positive*a
        negative=negative*b      
    if (positive>negative):
        return '1'
    else:
        return '0'

#main funcion
#open training data set
f1=open('C:/Python33/sentiment_analysis/sentiment140_training.txt',encoding="latin-1")
total=0
pos_words=0.0
neg_words=0.0
freq={}
pos_count=0
neg_count=0

for line in f1:
    line=line.rstrip('\n')
    total=total+1
    temp= line.split('\t')  #split on tab to separate the tweet from the label
    tokenized_text=tokenize(temp[1])    #tokenize the tweet
    words = tokenized_text.split(' ')   #split the tokenized tweet to store the words

    # applying negation
    for i in range(len(words)):
        if(words[i] == "not"):
            while(i+1<len(words)):
                if(re.match('[?\.!]',words[i+1])):
                    break
                else:
                    words[i+1]=words[i+1]+"not"
                    i+=1
            break

    
    # count the total number of positive and negative words
    if(temp[0]=='1'):
        pos_words=pos_words+len(words)
        pos_count=pos_count+1.0  #count the number of positive tweets

    else:
        neg_words=neg_words+len(words)
        neg_count=neg_count+1.0    #count the number of negative tweets
        
        # maintain a dictionary containing the word, its label and frequency of occurance    for w in words:
    for w in words:
        if w in freq.keys():
            if temp[0] in freq[w]:
                freq[w][temp[0]]+=1    #if the word exists then update the freq count for the word
            else:
                #adding label to hash
                freq[w][temp[0]]=1
        else:
            # adding w to hash
            freq[w]={temp[0]:1}  #if word doest exist, add it to the dicitonary.
f1.close()

#count the probability of postive and negative tweet
pos_prob = pos_count/total
neg_prob = neg_count/total
vocab=len(freq) # total number of words

testtotal=0
# reading from the test file:
f2= open('C:/Python33/sentiment_analysis/sentiment140_testing.txt',encoding="latin-1")
incorrect=0.0
correct=0.0
for line1 in f2:
    line1=line1.lower()
    testtotal+=1
    line=line.rstrip('\n')
    temp1=line1.split('\t')
    tokenized_text=tokenize(temp1[1])
    words =  tokenized_text.split(' ')
    ##    # applying negation
    for i in range(len(words)):
        if(words[i] == "not"):
            while(i+1<len(words)):
                if(re.match('[?\.!]',words[i+1])):
                    break
                else:
                    words[i+1]=words[i+1]+"not"
                    i+=1
            break
    label = calc_probability(words)     #function returns the label of the tweet
    if label==temp1[0]:
        correct+=1.0
    else:
        incorrect=incorrect+1.0
error= incorrect/testtotal
print(error)
f2.close()
