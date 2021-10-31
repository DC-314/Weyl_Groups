import hashlib
import numpy as np


# This program generates the Weyl group for E6, and partitions the group, 
# depending on the order of the group elements. The order of the group element 
# is defined as the number of generators, multipled together to create the element.
# The program also counts the elements that are their own inverse in each partition.


## Generates a finite group with generators from ADE of E6
#
#         0
#         |
# 1---2---3---4---5
#
#  The order of the group is 51840


##########    FUNCTIONS    ##########
# Given a list E6, that contains the idenity and the generators this function will
# populate E6 with the Weyl group, partitioned into 36 parts.

def Generate_E6_Group(E6):
    H = set(); H_table( E6[0], H )  #initialise Hash set
    Sk = E6[1];   m = len(E6[1])  
    for k in range(1,36): 
        n = len( Sk );   Sk_plus_1 = []
        H_table( Sk, H )  #adds hash of Sk to H    
        for i in range( n ): 
              for j in range( m ):
                    s = np.matmul( Sk[i], E6[1][j] )
                    hash = hashlib.sha256(s).hexdigest()[:20] 
                    if hash not in H:   #lookup hash table
                        H.add( hash )
                        Sk_plus_1.append( s)
        Sk = Sk_plus_1
        E6.append(Sk_plus_1)  


# Given a list of matrices, and a set H, (ie H = set()), this function will hash LM
# and add it to H. Helper function for Generate_E6_Group.
# The hash table allows fast look up, of group elements, in each partition.
def H_table( LM, H ):
    n = len( LM ); 
    for i in range( n ):
        H.add( hashlib.sha256( LM[i] ).hexdigest()[:20] )


#def print_array(A):
#    n = len(A)
#    for i in range(n):
#        for j in range(n):
#            print '{:4}'.format(A[i][j]),
#        print


# Find number of elements that are their own inverse in each partition of E6.
# ie. A = A-1   => A^2 = I
def Count_Inverses(E6,I_6):
    I_count= [];
    for k in range(37):
        count = 0
        for i in range( len(E6[k]) ):
            M = np.matmul( E6[k][i], E6[k][i] )
            if( np.array_equal( M , I_6 ) ):
               count += 1
        I_count.append(count)
    return I_count


#######      THE GENERATORS      ######
#
#         0
#         |
# 1---2---3---4---5

s0 = np.array([[-1, 0, 0, 0, 0, 0],
               [ 0, 1, 0, 0, 0, 0],
               [ 0, 0, 1, 0, 0, 0],
               [ 1, 0, 0, 1, 0, 0],
               [ 0, 0, 0, 0, 1, 0],
               [ 0, 0, 0, 0, 0, 1]])

s1 = np.array([[ 1, 0, 0, 0, 0, 0],
               [ 0,-1, 0, 0, 0, 0],
               [ 0, 1, 1, 0, 0, 0],
               [ 0, 0, 0, 1, 0, 0],
               [ 0, 0, 0, 0, 1, 0],
               [ 0, 0, 0, 0, 0, 1]])

s2 = np.array([[ 1, 0, 0, 0, 0, 0],
               [ 0, 1, 1, 0, 0, 0],
               [ 0, 0,-1, 0, 0, 0],
               [ 0, 0, 1, 1, 0, 0],
               [ 0, 0, 0, 0, 1, 0],
               [ 0, 0, 0, 0, 0, 1]])

s3 = np.array([[ 1, 0, 0, 1, 0, 0],
               [ 0, 1, 0, 0, 0, 0],
               [ 0, 0, 1, 1, 0, 0],
               [ 0, 0, 0,-1, 0, 0],
               [ 0, 0, 0, 1, 1, 0],
               [ 0, 0, 0, 0, 0, 1]])

s4 = np.array([[ 1, 0, 0, 0, 0, 0],
               [ 0, 1, 0, 0, 0, 0],
               [ 0, 0, 1, 0, 0, 0],
               [ 0, 0, 0, 1, 1, 0],
               [ 0, 0, 0, 0,-1, 0],
               [ 0, 0, 0, 0, 1, 1]])

s5 = np.array([[ 1, 0, 0, 0, 0, 0],
               [ 0, 1, 0, 0, 0, 0],
               [ 0, 0, 1, 0, 0, 0],
               [ 0, 0, 0, 1, 0, 0],
               [ 0, 0, 0, 0, 1, 1],
               [ 0, 0, 0, 0, 0,-1]])

# The Identity
I_6 = np.array([[1, 0, 0, 0, 0, 0 ],
                [0, 1, 0, 0, 0, 0 ],
                [0, 0, 1, 0, 0, 0 ],
                [0, 0, 0, 1, 0, 0 ],
                [0, 0, 0, 0, 1, 0 ],
                [0, 0, 0, 0, 0, 1 ]])

#Initialise identity and generators for Weyl group of E6.
E6 = [ [I_6], [s0,s1,s2,s3,s4,s5] ]

#This will take about 5 seconds to generate all 51840 group elements of the Weyl group of E6. 
Generate_E6_Group(E6)

#Generating Hash tables of all 51840 group elements
H_E6=[]
for i in range(36):
  H=set()
  H_table(E6[i],H)
  H_E6.append(H)


#  Stores size of each partition
P_size = []    # list of Partition size, ie. number of elemetns in each partition
for i in range( len(E6) ):
    P_size.append( len( E6[i] ) )

    
# Count number of group elements in each partition that are their own inverses.
Inverses = Count_Inverses(E6,I_6)     
    
#Print Table
sum=0
sum1=0
for i in range(len(P_size)):
   print(i,P_size[i],Inverses[i])
   sum += P_size[i]
   sum1 += Inverses[i]


print("TOTAL  " + str(sum) + "  " +  str(sum1))

