import matplotlib.pyplot as plt; plt.rcdefaults()
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from scipy.misc import toimage
import random 
import os


# https://scipy-cookbook.readthedocs.io/items/Matplotlib_converting_a_matrix_to_a_raster_image.html
from scipy import mgrid
def imsave(filename, X, **kwargs):
    """ Homebrewed imsave to have nice colors... """
    figsize=(np.array(X.shape)/100.0)[::-1]
    plt.rcParams.update({'figure.figsize':figsize})
    fig = plt.figure(figsize=figsize)
    plt.axes([0,0,1,1]) # Make the plot occupy the whole canvas
    plt.axis('off')
    fig.set_size_inches(figsize)
    plt.imshow(X,origin='lower', **kwargs)
    plt.savefig(filename, facecolor='black', edgecolor='black', dpi=100)
    plt.close(fig)
    
    

def expand(a):
    # zero row to be added below
    new_row = np.zeros(len(a[0]) +2)
    # zero columnns to be adde on both sides
    zero_stack = np.zeros((len(a),1))
    # sticking everything together
    a = np.hstack((zero_stack, a ))
    a = np.hstack((a, zero_stack ))
    a = np.vstack((a,new_row))
    return a

def initialize():
    a = np.zeros((2,3))
    a[0][1] = 1
    a[1][1] = 1
    return a



def run(a,rules, rounds):
    
    print("            0%" + 48*" " + "100%" + 4*" " + "progress not linear!")
    print("processing: [", end="")
    for i in range(rounds):
        # prints one every fiftyest part (time taken not linear)
        if i % (rounds/50) == 0.0:
            print("=", end="")
        
        a = expand(a)
        a = apply_rules(a, rules)
    print("]")
    return(a)

def apply_rules(a, rules):
    for i in range(1,len(a[0])-1):
        parent = [a[len(a)-2][i-1], a[len(a)-2][i], a[len(a)-2][i+1] ]
        for k in rules:
            if parent == k[0]:
                a[len(a)-1][i] = k[1]
    #print()
    return a

# @param string string containing only 8 times 1 or 0, as contained in filename of image produced by main()
# @return ruleset to generate pattern 
def reproduce_ruleset(string):
    ruleset = [([1,1,1],int(string[0])),
               ([1,1,0],int(string[1])),
               ([1,0,1],int(string[2])),
               ([1,0,0],int(string[3])),
               ([0,1,1],int(string[4])),
               ([0,1,0],int(string[5])),
               ([0,0,1],int(string[6])),
               ([0,0,0],int(string[7]))
               ]
    return ruleset


# @param number 0 generates random ruleset, 1-4 are rulesets shown in chapter 2 of "a new kind of science"
# @return ruleset to generate pattern 
def get_ruleset(number):
    if (number == 1):
        ruleset = reproduce_ruleset("11111010")
    elif (number == 2):
        ruleset = reproduce_ruleset("01011010")
    elif (number == 3):
        ruleset = reproduce_ruleset("00011110")
    elif (number == 4):
        ruleset = reproduce_ruleset("01101110")
    else:
        ruleset = [ ([1,1,1],int(random.getrandbits(1))),
                    ([1,1,0],int(random.getrandbits(1))),
                    ([1,0,1],int(random.getrandbits(1))),
                    ([1,0,0],int(random.getrandbits(1))),
                    ([0,1,1],int(random.getrandbits(1))),
                    ([0,1,0],int(random.getrandbits(1))),
                    ([0,0,1],int(random.getrandbits(1))),
                    ([0,0,0],int(random.getrandbits(1)))
                    ]
    return ruleset
    
def generate_pattern(runs, ruleset):
    # init
    a = initialize()
    
    # get rules and tell which
    rules = get_ruleset(ruleset)
    rule_sequence = []
    rule_string = ""
    for i in rules:
        rule_sequence.append(i[1])
        rule_string = rule_string + str(i[1]) # for file name
    
    # print some info
    print("iterations:", runs)
    print("rules:", rule_sequence)
        
    # da magic
    a = run(a, rules, runs)

    # show image
    # plt.imshow(a)
    # plt.show()

    # save image
    filename = "wolfram_img/" + str(runs) + "/" + 'wolfram_' + rule_string + "_" + str(runs) + '.png'
    plt.imsave(filename, a)
    #choose different colors:
    #imsave(filename, a, cmap=plt.cm.magma )
    
    print()
    print("done")
    
def main():
    # basic parameter
    runs = 10
    size = 500
    ruleset = 0 # random
    
    directory = "wolfram_img/" + str(size)
    if not os.path.exists(directory):
        os.makedirs(directory)

    for i in range(runs):
        print("run ",i, ":")
        generate_pattern(size, ruleset)
        print()

# @param number integer < 256
# @return string of the length 8 representing the binary of "number"
def int2patternstring(number):
    if (number > 255):
        number = 0
    pattern = str(bin(number))[2::]
    pattern = "0" * (8 - len(pattern)) + pattern
    return pattern

def every_pattern(size):
    directory = "wolfram_img/" + str(size)
    if not os.path.exists(directory):
        os.makedirs(directory)

    for i in range(256):
        print( int2patternstring(i), ":")
        generate_pattern(size, reproduce_ruleset(int2patternstring(i)))
        print()



every_pattern(500)
