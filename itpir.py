import numpy as np
import random

# functions -----------------------

def vectorToPoint(*arr):
    arr1 = [[0,0],[0,0],[0,0],[0,0]]
    for idx, val in enumerate(arr):
        if val == 1:
            arr1[idx][1] = 1
    return arr1

def randomPoints():
    arr2 = [[0,0],[0,0],[0,0],[0,0]]
    for idx, val in enumerate(arr2):
        arr2[idx][0] = random.randrange(1,100)
        arr2[idx][1] = random.randrange(1,100)
    return arr2

def polyVector(basic, randArr):
    polys = [0,0,0,0]
    for idx, val in enumerate(basic):
        slope = float((randArr[idx][1] - basic[idx][1]))/float((randArr[idx][0] - basic[idx][0]))
        polys[idx] = np.poly1d([slope, basic[idx][1]])
    return polys

def conv2ASCII(str):
    sum = 0
    for character in str:
        sum += ord(character)
    return sum

def convSData(arr):
    w, h = 5, 6
    rarr = [[0 for x in range(w)] for y in range(h)]
    for i, val in enumerate(arr):
        for j, val2 in enumerate(arr[i]):
            rarr[i][j] = conv2ASCII(arr[i][j])
    return rarr

def arrFunc(arr, num):
    w, h = 6, 4
    rarr = [[0 for x in range(w)] for y in range(h)]
    for i, val in enumerate(arr):
        for j, val2 in enumerate(arr[i]):
            rarr[i][j] = arr[i][j](num)
    return rarr

def aliceArrFunc(arr, num):
    rarr = [0 for i in range (4)]
    for i, val in enumerate(arr):
        rarr[i] = arr[i](num)
    return rarr

def polyVectorFinal(finalvector1, finalvector2):
    polys = [0, 0, 0, 0, 0]
    for idx, val in enumerate(finalvector1):
        slope = ((finalvector2[idx][1] - finalvector1[idx][1]) / (finalvector2[idx][0] - finalvector1[idx][0]))
        if idx != 2:
            polys[idx] = np.poly1d([slope, 0])
        else:
            polys[idx] = np.poly1d([slope, 1])
    return polys

def aliceArrFuncRecon(arr, num):
    rarr = [0 for i in range (5)]
    for i, val in enumerate(arr):
        rarr[i] = arr[i](num)
    return rarr
    
# main ---------------------------

#database within both servers
sData = [["John John", "jj@gmail.com", "1/19/2021", "1.1KB", "0xb3ff3a"],
        ["Jake Smith", "js@gmail.com", "5/29/2019", "2.3KB", "0x33aa93"],
        ["Elizabeth Thao", "et123@gmail.com", "2/2/2021", "1.2KB", "0x23cd24"],
        ["Blake Cortez", "bc@gmail.com", "3/15/2007", "200KB", "0xa94103"],
        ["John John", "el@gmail.com", "7/13/2016", "71KB", "0x11a2b4"],
        ["Elizabeth Thao", "et123@gmail.com", "12/12/2008", "1.2MB", "0x84CD22"]]

#converts entries in database to numbers (converts to ASCII values then addes ASCII values together)
snumData = convSData(sData)

# batch index of queries that each server has of Email, Size, Date
batchIndServer = [[np.poly1d([.5, -.5, 0]), np.poly1d([0]), np.poly1d([0]), np.poly1d([0]), np.poly1d([-.5, .5, 1]), np.poly1d([0])],
                [np.poly1d([0]), np.poly1d([1]), np.poly1d([0]), np.poly1d([0]), np.poly1d([0]), np.poly1d([0])],
                [np.poly1d([0]), np.poly1d([0]), np.poly1d([1, -2, 1]), np.poly1d([0]), np.poly1d([0]), np.poly1d([-1, 2, 0])],
                [np.poly1d([0]), np.poly1d([0]), np.poly1d([0]), np.poly1d([1]), np.poly1d([0]), np.poly1d([0])]]

        
# Alice wants Elizabeth's largest email
alice = [0,0,1,0]
x = 1
# converts alice's vector to points
aliceVector = vectorToPoint(*alice)
# 2nd vector for random points to create polynomials
randPointsVector = randomPoints()
testvec = [[120,3], [5,3], [1,6], [9,2]]
# creates vector of polynomials of alice's point vector and random point vector
pVec = polyVector(aliceVector, testvec)
# Alice puts that x=3 and x=4 in her polynomials (pVec)
a1 = aliceArrFunc(pVec, 3)
a2 = aliceArrFunc(pVec, 4)

# Alice sends 2 queries to servers 1 and 2 (as s1 and s2) which contain that
# x=3 for server 1 and x=4 for server 2) 
s1 = arrFunc(batchIndServer, 3)
s2 = arrFunc(batchIndServer, 4)

# Dot product of Alice's query (a1 and a2) with server query (s1 and s2)
test = [0.075, 1.8, 16, 0.666667]
test2 = [0.1, 2.4, 21, 0.888889]
dot1 = np.dot(test, s1)
dot2 = np.dot(test2, s2)

# Then Dot product from dot1 and dot2 to the numbered database (snumData)
finaldots1 = np.dot(dot1, snumData)
finaldots2 = np.dot(dot2, snumData)

# Convert finaldots1 and finaldots2 to point vectors with respective x
finalvector1 = [[3, round(finaldots1[0])], [3, round(finaldots1[1])], [3, round(finaldots1[2])], [3, round(finaldots1[3])], [3, round(finaldots1[4])]]
finalvector2 = [[4, round(finaldots2[0])], [4, round(finaldots2[1])], [4, round(finaldots2[2])], [4, round(finaldots2[3])], [4, round(finaldots2[4])]]

# Alice reconstructs polynomials based off these vectors
reconPolyVector = polyVectorFinal(finalvector1, finalvector2)

# Alice puts x = 1 in new reconstructed polynomials
res = aliceArrFuncRecon(reconPolyVector, 1)
print(res)
print(snumData[2])