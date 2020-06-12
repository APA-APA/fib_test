__author__ = 'apa'

import numpy as np
import random

#  https://docs.python.org/2.7/library/random.html?highlight=random%20number#module-random

random.seed()

xxx=[]    # Create a tuple for use for saving words
yyy=[]    # Tuple to save the words and use in inerting itno the array.
leny=[]   # Tuple to contain the lengths of the words in yyy
len_max=0 # Place holder for the max word length
num_words=0  # Number of words to be processed  palce holder

array_max=30  # Max size of the search array

imax=10 # Max number of words allowed

# Step loop counter to zero
strl="go"
i=0

# while loop to allow typing in of words to be searched.

while (strl != 'stop'):   #Loop until 'stop' is entered

    strl=raw_input("Enter a word - entering 'stop' ends word entry:  ");  # Read in a word into str

    #print( 'Word input is: ', strl, '   contains ', len(strl), ' characters')   #list the word and number of characters

    xxx.append(strl)    # Add new word to tuple
    i=i+1
    if i>=imax:  #trap the case when the max number of words is exceeded.
        i=i+1
        break

num_words=i-1  # Eliminate the extra word 'stop'

# Set up the words and lengths for insertion into array
for k in range(0,num_words):
    yyy.append(xxx[k])
    leny.append(len(xxx[k]))
    if len_max<leny[k]: len_max=leny[k]
    print 'Word# ', k,  '  length=', leny[k], '   ', yyy[k]

print 'Max word length is ', len_max, '  characters'


# Establish the search array size based on words mengths and pre-set limit
array_size=4*len_max
if array_size>array_max: array_size=array_max

# Create the search array

dt=np.dtype('S1')
x=np.ndarray(shape=(array_size,array_size), dtype=np.dtype('S1'))
x.fill('-')


#Loop thru and insert the words
count=0
i=0
while i<=num_words-1:

    #Use random number to select the word location
    x_loc = random.randint(0,array_size-1)
    y_loc = random.randint(0, array_size-1)

    #Use random number to set direction
    direct=random.randint(0,7)
    if direct==0:    # Left to right horizontal
        dx=1
        dy=0
    if direct == 1:  # Left to right 45 down
        dx = 1
        dy = 1
    if direct == 2:  # Vertical down
        dx = 0
        dy = 1
    if direct == 3:  # Right to left 45 down
        dx = -1
        dy = 1
    if direct == 4:  # Right to left horizontal
        dx = -1
        dy = 0
    if direct == 5:  # Right to left 45 up
        dx = -1
        dy = -1
    if direct == 6:  # Vertical up
        dx = 0
        dy = -1
    if direct == 7:  # Left to right 45 up
        dx = 1
        dy = -1

    word=yyy[i]

    x_locl=x_loc
    y_locl=y_loc
    for k in range(0,leny[i]):
        flag = 0  # Flag to see if word was inserted
        if x_locl+dx*(leny[i]-1)>array_size-1: # If word goes off the right edge, iterate
            break
        if y_locl+dy*(leny[i]-1)>array_size-1: # If word goes off the bottom edge, iterate
            break
        if x_locl+dx*(leny[i]-1)<0:            # If word goes off left edge, iterate
            break
        if y_locl+dy*(leny[i]-1)<0:            # If word goes off the top edge, iterate
            break

        if x[x_locl, y_loc]!='-':              # Check if the word conflicts with an existing word insert.
            if word[k] != x[x_locl, y_locl]:   # Check that words do not ahve same letter at the common point
                break

        #x[x_loc, y_loc]= word[k]
        # Increment the letter location
        x_locl=x_locl+dx
        y_locl=y_locl+dy

        flag=1

    # If flag==1 at this point then the word can be inserted into array so do it
    if flag==1:
        x_locl = x_loc
        y_locl = y_loc
        for k in range(0, leny[i]):
            x[x_locl, y_locl] = word[k]
            x_locl = x_locl + dx
            y_locl = y_locl + dy

        i=i+1
    count=count+1

    # Put in a trap if the solution cannot be found within a finite number of tries.
    if count >1000000:
        print 'Could not find a solution'
        exit(4321)

# Create the solution in a text file for printing
# Solution contains the words without unused location fill with random letters
soln_file=open('solution.txt', 'w',)

soln_file.write('\n\n     SOLUTION   \n\n')
for i in range(0,array_size):
    for j in range(0, array_size):
        soln_file.write( x[i,j]+' ')
    soln_file.write('\n')

soln_file.write('\n\n')
soln_file.write('HIDDEN WORDS \n\n')
for i in range(0,num_words):
    soln_file.write(yyy[i]+'\n')

soln_file.close()

# Create a tuple with the alphabet, (could use more sophisticate approach)

alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

# Fill the un-used array spaces with a random letter
for i in range(0,array_size):
    for j in range(0,array_size):
        if x[i,j]=='-':
            letter=random.randint(0,25)
            x[i,j]=alphabet[letter]

# Place the filled array in the challenge file which is handed out for competitors.

soln_file=open('challenge.txt', 'w',)

soln_file.write('\n\n     CHALLENGE   \n\n')
for i in range(0,array_size):
    for j in range(0, array_size):
        soln_file.write( x[i,j]+' ')
    soln_file.write('\n')

soln_file.write('\n\n')
soln_file.write('WORDS TO BE FOUND \n\n')
for i in range(0,num_words):
    soln_file.write(yyy[i]+'\n')

soln_file.close()


exit(123)  # Current end of program!!


