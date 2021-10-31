import hashlib
import numpy as np


# This program generates the Weyl group for E7, and partitions the group, 
# depending on the order of the group elements. The order of the group element 
# is defined as the number of generators, multipled together to create the element.
# The program also counts the elements that are their own inverse in each partition.
#
#  Diagram for  E7
#
#         0
#         |
# 1---2---3---4---5---6
#
#  The order of the group is 2,903,040
#
# The program takes about 5 minutes to run.


##########    FUNCTIONS    ##########

# Given a list E7, that contains the idenity and the generator this function will
# populate E7 with the Weyl group, partitioned into 36 parts.
def Generate_E7_Group(E7):
    H = set(); H_table( E7[0], H )  #initialise Hash set
    Sk = E7[1];   m = len(E7[1])
    for k in range(1,64):
        n = len( Sk );   Sk_plus_1 = []
        H_table( Sk, H )  #adds hash of Sk to H    
        for i in range( n ):
              for j in range( m ):
                    s = np.matmul( Sk[i], E7[1][j] )
                    hash = hashlib.sha256(s).hexdigest()[:20]
                    if hash not in H:
                        H.add( hash )
                        Sk_plus_1.append( s)
        Sk = Sk_plus_1
        E7.append(Sk_plus_1)


# Given a list of matrices, and a set H, (ie H = set()), this function will hash LM
# and add it to H. Helper function for Generate_E7_Group.
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


# Find number of elements that are their own inverse in each partition of E7
# ie. A = A-1   => A^2 = I
def Count_Inverses(E7,I_7):
    I_count= [];
    for k in range(65):
        count = 0
        for i in range( len(E7[k]) ):
            M = np.matmul( E7[k][i], E7[k][i] )
            if( np.array_equal( M , I_7 ) ):
               count += 1
        I_count.append(count)
    return I_count


#######      THE GENERATORS      #######

s0 = np.array([[-1, 0, 0, 0, 0, 0, 0 ],
               [ 0, 1, 0, 0, 0, 0, 0 ],
               [ 0, 0, 1, 0, 0, 0, 0 ],
               [ 1, 0, 0, 1, 0, 0, 0 ],
               [ 0, 0, 0, 0, 1, 0, 0 ],
               [ 0, 0, 0, 0, 0, 1, 0 ],
               [ 0, 0, 0, 0, 0, 0, 1 ]])

s1 = np.array([[ 1, 0, 0, 0, 0, 0, 0 ],
               [ 0,-1, 0, 0, 0, 0, 0 ],
               [ 0, 1, 1, 0, 0, 0, 0 ],
               [ 0, 0, 0, 1, 0, 0, 0 ],
               [ 0, 0, 0, 0, 1, 0, 0 ],
               [ 0, 0, 0, 0, 0, 1, 0 ],
               [ 0, 0, 0, 0, 0, 0, 1 ]])

s2 = np.array([[ 1, 0, 0, 0, 0, 0, 0 ],
               [ 0, 1, 1, 0, 0, 0, 0 ],
               [ 0, 0,-1, 0, 0, 0, 0 ],
               [ 0, 0, 1, 1, 0, 0, 0 ],
               [ 0, 0, 0, 0, 1, 0, 0 ],
               [ 0, 0, 0, 0, 0, 1, 0 ],
               [ 0, 0, 0, 0, 0, 0, 1 ]])

s3 = np.array([[ 1, 0, 0, 1, 0, 0, 0 ],
               [ 0, 1, 0, 0, 0, 0, 0 ],
               [ 0, 0, 1, 1, 0, 0, 0 ],
               [ 0, 0, 0,-1, 0, 0, 0 ],
               [ 0, 0, 0, 1, 1, 0, 0 ],
               [ 0, 0, 0, 0, 0, 1, 0 ],
               [ 0, 0, 0, 0, 0, 0, 1 ]])

s4 = np.array([[ 1, 0, 0, 0, 0, 0, 0 ],
               [ 0, 1, 0, 0, 0, 0, 0 ],
               [ 0, 0, 1, 0, 0, 0, 0 ],
               [ 0, 0, 0, 1, 1, 0, 0 ],
               [ 0, 0, 0, 0,-1, 0, 0 ],
               [ 0, 0, 0, 0, 1, 1, 0 ],
               [ 0, 0, 0, 0, 0, 0, 1 ]])

s5 = np.array([[ 1, 0, 0, 0, 0, 0, 0 ],
               [ 0, 1, 0, 0, 0, 0, 0 ],
               [ 0, 0, 1, 0, 0, 0, 0 ],
               [ 0, 0, 0, 1, 0, 0, 0 ],
               [ 0, 0, 0, 0, 1, 1, 0 ],
               [ 0, 0, 0, 0, 0,-1, 0 ],
               [ 0, 0, 0, 0, 0, 1, 1 ]])

s6 = np.array([[ 1, 0, 0, 0, 0, 0, 0 ],
               [ 0, 1, 0, 0, 0, 0, 0 ],
               [ 0, 0, 1, 0, 0, 0, 0 ],
               [ 0, 0, 0, 1, 0, 0, 0 ],
               [ 0, 0, 0, 0, 1, 0, 0 ],
               [ 0, 0, 0, 0, 0, 1, 1 ],
               [ 0, 0, 0, 0, 0, 0,-1 ]])

# The Identity
I_7 = np.array([[1, 0, 0, 0, 0, 0, 0 ],
                [0, 1, 0, 0, 0, 0, 0 ],
                [0, 0, 1, 0, 0, 0, 0 ],
                [0, 0, 0, 1, 0, 0, 0 ],
                [0, 0, 0, 0, 1, 0, 0 ],
                [0, 0, 0, 0, 0, 1, 0 ],
                [0, 0, 0, 0, 0, 0, 1 ]])

#Initialise generators for Weyl group of E7
E7 = [[I_7],[s0,s1,s2,s3,s4,s5,s6]]

print "This program takes about 5 minutes to run"
#This will take about 5 minutes to generate all 2,903,040 group elements of the Weyl group of E7 
Generate_E7_Group(E7)

#Generating Hash tables of all 2,903,040 group elements
H_E7=[]
for i in range(64):
  H=set()
  H_table(E7[i],H)
  H_E7.append(H)

# Calculate size of each partition
P_size = []    # list of Partition size, ie. number of elemetns in each partition
for i in range( len(E7) ):
    P_size.append( len( E7[i] ) )

# Count number of group elements in each partition that are their own inverses
Inverses = Count_Inverses(E7,I_7)

# Print Table
sum=0
sum1=0
for i in range(len(P_size)):
   print(i,P_size[i],Inverses[i])
   sum += P_size[i]
   sum1 += Inverses[i]

print( "TOTAL  " + str(sum) + "  " +  str(sum1) )
