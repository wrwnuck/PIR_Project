import numpy as np
import math
import random
from scipy.interpolate import lagrange
from numpy.polynomial import Polynomial

#every calculation is based in mod
mod = 1037
inverseModArr = [1, 6, 4, 3, 9, 2, 8, 7, 5, 10]
#note:
# y = pow(3, -1, 11)
# y is the inverse of 3 mod 11

# functions---------------------------------

# conv2ASCII and convSData are to convert string ASCII to their number values per cell
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
            rarr[i][j] = conv2ASCII(arr[i][j]) % mod
    return rarr

# plug in an x to calculate polynomials in terms of mod n in vector 
def computePolyVec(polyVec, x, size):
    rarr = [0 for i in range (size)]
    for i, val in enumerate(polyVec):
        rarr[i] = polyVec[i](x) % mod
    return rarr

# input x value to batch index of queries in terms of mod n
def computeBatchInput(batch, x):
    w, h = 6, 4
    rarr = [[0 for x in range(w)] for y in range(h)]
    for i, val in enumerate(batch):
        for j, val2 in enumerate(batch[i]):
            rarr[i][j] = batch[i][j](x) % mod
    return rarr

# converts 
def convertMod(resArr):
    rarr = [0, 0, 0, 0, 0, 0]
    for i, val in enumerate(resArr):
        rarr[i] = resArr[i] % mod
    return rarr

def convertMod2(resArr):
    rarr = [0, 0, 0, 0, 0]
    for i, val in enumerate(resArr):
        rarr[i] = resArr[i] % mod
    return rarr

def matrixMul(largeMatrix, smallMatrix):
    res = [0 for i in range(6)]
    for idx in range(6):
        res[idx] = (smallMatrix[0] * largeMatrix[0][idx]) + (smallMatrix[1] * largeMatrix[1][idx]) + (smallMatrix[2] * largeMatrix[2][idx]) + (smallMatrix[3] * largeMatrix[3][idx])
    return res
            
#need to edit this ---------------------------------------------------------------------------------------------------------------------------------
def createPolynomials_Recon(ser1Res, ser2Res):
    res = [0 for i in range(len(ser1Res))]
    for idx, i in enumerate(ser1Res):
        slope = (pow((ser2Res[idx][0]-ser1Res[idx][0]), -1, 11) * ((ser2Res[idx][1] - ser1Res[idx][1]) % mod)) % mod
        res[idx] = np.poly1d([slope, ((ser1Res[idx][1]-(slope * ser1Res[idx][0]))%mod)])
    return res


#user functions:

# vectorToPoint takes vector made by user to get certain index and converts it to points in an array 
def vectorToPoint(arr, x):
    arr1 = [[0,0], [0,0], [0,0], [0,0]]
    for idx, val in enumerate(arr):
        arr1[idx][0] = x
        arr1[idx][1] = arr[idx]
    return arr1

# vectorToPoint but for results from servers
def vectorToPoint_Server(arr, x):
    arr1 = [[0,0], [0,0], [0,0], [0,0], [0,0]]
    for idx, val in enumerate(arr):
        arr1[idx][0] = x
        arr1[idx][1] = arr[idx]
    return arr1

# randomPOints makes random points in a vector equal to the length of the vector the user makes
def randomPoints(X):
    arr2 = [0, 0, 0, 0]
    for idx, val in enumerate(arr2):
        arr2[idx] = random.randrange(1,(mod-1)) 
    return arr2

# gets the slope in regards of inverse x mod n
# potentially randVec2 parameter
def createPolynomials(alice, randVec1, randVec2, xCoor):
    res = [0, 0, 0, 0]
    for i in range(4):
        mul=[0, 0, 0]
        mul[0] = pow((((xCoor[0]-xCoor[1])%mod)*((xCoor[0]-xCoor[2])%mod))% mod, -1, mod)
        mul[1] = pow((((xCoor[1]-xCoor[0])%mod)*((xCoor[1]-xCoor[2])%mod))% mod, -1, mod)
        mul[2] = pow((((xCoor[2]-xCoor[0])%mod)*((xCoor[2]-xCoor[1])%mod))% mod, -1, mod)
        tempPoly1 = [(alice[i]*mul[0])% mod, (alice[i] * ((mul[0] * ((-1 * (xCoor[2]+xCoor[1]))%mod))%mod))%mod, (alice[i] * ((mul[0] * ((xCoor[1]*xCoor[2])%mod))%mod))%mod]
        tempPoly2 = [(randVec1[i]*mul[1])% mod, (randVec1[i] * ((mul[1] * ((-1 * (xCoor[2]+xCoor[0]))%mod))%mod))%mod, (randVec1[i] * ((mul[1] * ((xCoor[0]*xCoor[2])%mod))%mod))%mod]
        tempPoly3 = [(randVec2[i]*mul[2])% mod, (randVec2[i] * ((mul[2] * ((-1 * (xCoor[1]+xCoor[0]))%mod))%mod))%mod, (randVec2[i] * ((mul[2] * ((xCoor[0]*xCoor[1])%mod))%mod))%mod]
        res[i] = np.poly1d([(((tempPoly1[0]+tempPoly2[0])%mod) + tempPoly3[0])%mod, (((tempPoly1[1]+tempPoly2[1])%mod) + tempPoly3[1])%mod, (((tempPoly1[2]+tempPoly2[2])%mod) + tempPoly3[2])%mod])
    return res

#1 degree lagrange interpolating polynomial
def create1DPoly(sbv1, sbv2, xes):
    res=[0, 0, 0, 0]
    for i in range(4):
        mul = [0, 0]
        mul[0] = pow((xes[0] - xes[1])%mod, -1, mod)
        mul[1] = pow((xes[1] - xes[0])%mod, -1, mod) 
        tempPoly1 = [(sbv1[i] * mul[0])%mod, (-1*(sbv1[i] *((xes[1] * mul[0])%mod))%mod)%mod]
        tempPoly2 = [(sbv2[i] * mul[1])%mod, (-1*(sbv2[i] *((xes[0] * mul[1])%mod))%mod)%mod]
        res[i] = np.poly1d([(tempPoly1[0] + tempPoly2[0])%mod, (tempPoly1[1] + tempPoly2[1])%mod])
    return res

#3 degree lagrange interpolating polynomial
def create4DPoly(s1, s2, s3, s4, x):
    res=[0, 0, 0, 0, 0]
    for i in range(5):
        mul = [0, 0, 0, 0]
        mul[0] = pow(((((x[0] - x[1])%mod * ((x[0] - x[2])%mod))%mod) * ((x[0] - x[3])%mod))% mod, -1, mod)
        mul[1] = pow(((((x[1] - x[0])%mod * ((x[1] - x[2])%mod))%mod) * ((x[1] - x[3])%mod))% mod, -1, mod)
        mul[2] = pow(((((x[2] - x[0])%mod * ((x[2] - x[1])%mod))%mod) * ((x[2] - x[3])%mod))% mod, -1, mod)
        mul[3] = pow(((((x[3] - x[0])%mod * ((x[3] - x[1])%mod))%mod) * ((x[3] - x[2])%mod))% mod, -1, mod)
        tempPoly1 = [(s1[i] * mul[0])%mod, (s1[i] * ((mul[0] * (((-1 * x[3])-x[2]-x[1])%mod))%mod))%mod, (s1[i] * ((mul[0] * ((((x[2]*x[3])%mod + (x[1]*x[3])%mod + (x[1]*x[2])%mod)%mod))%mod)))%mod, ((-1*(s1[i] * ((mul[0] * (x[1]*x[2]*x[3])%mod))%mod))%mod)%mod]
        tempPoly2 = [(s2[i] * mul[1])%mod, (s2[i] * ((mul[1] * (((-1 * x[3])-x[2]-x[0])%mod))%mod))%mod, (s2[i] * ((mul[1] * ((((x[2]*x[3])%mod + (x[0]*x[3])%mod + (x[0]*x[2])%mod)%mod))%mod)))%mod, ((-1*(s2[i] * ((mul[1] * (x[0]*x[2]*x[3])%mod))%mod))%mod)%mod]
        tempPoly3 = [(s3[i] * mul[2])%mod, (s3[i] * ((mul[2] * (((-1 * x[3])-x[1]-x[0])%mod))%mod))%mod, (s3[i] * ((mul[2] * ((((x[1]*x[3])%mod + (x[0]*x[3])%mod + (x[0]*x[1])%mod)%mod))%mod)))%mod, ((-1*(s3[i] * ((mul[2] * (x[0]*x[1]*x[3])%mod))%mod))%mod)%mod]
        tempPoly4 = [(s4[i] * mul[3])%mod, (s4[i] * ((mul[3] * (((-1 * x[2])-x[1]-x[0])%mod))%mod))%mod, (s4[i] * ((mul[3] * ((((x[1]*x[2])%mod + (x[0]*x[2])%mod + (x[0]*x[1])%mod)%mod))%mod)))%mod, ((-1*(s4[i] * ((mul[3] * (x[0]*x[1]*x[2])%mod))%mod))%mod)%mod]
        res[i] = np.poly1d([(tempPoly1[0]+tempPoly2[0]+tempPoly3[0]+tempPoly4[0])%mod, (tempPoly1[1]+tempPoly2[1]+tempPoly3[1]+tempPoly4[1])%mod, (tempPoly1[2]+tempPoly2[2]+tempPoly3[2]+tempPoly4[2])%mod, (tempPoly1[3]+tempPoly2[3]+tempPoly3[3]+tempPoly4[3])%mod])
    return res
# end functions-----------------------------

# What each server contains-----------------

#database
sData = [["John John", "jj@gmail.com", "1/19/2021", "1.1KB", "0xb3ff3a"],
        ["Jake Smith", "js@gmail.com", "5/29/2019", "2.3KB", "0x33aa93"],
        ["Elizabeth Thao", "et123@gmail.com", "2/2/2021", "1.2KB", "0x23cd24"],
        ["Blake Cortez", "bc@gmail.com", "3/15/2007", "200KB", "0xa94103"],
        ["John John", "el@gmail.com", "7/13/2016", "71KB", "0x11a2b4"],
        ["Elizabeth Thao", "et123@gmail.com", "12/12/2008", "1.2MB", "0x84CD22"]]

#convert database from ASCII strings to numbers
snumData = convSData(sData)

#index of queries
email = [[0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0]]

size = [[0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 0]]

date = [[1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0]]

#index of queries labels
ioq_labels = [0, 1, 2]

#batch index of queries for email, size, and date respecitely
batchIndServer = [[np.poly1d([(1*pow(2,-1,mod)),(1*pow(-2,-1,mod)), 0]), np.poly1d([0]), np.poly1d([0]), np.poly1d([0]), np.poly1d([(1*pow(-2,-1,mod)),(1*pow(2,-1,mod)), 1]), np.poly1d([0])],
                [np.poly1d([0]), np.poly1d([1]), np.poly1d([0]), np.poly1d([0]), np.poly1d([0]), np.poly1d([0])],
                [np.poly1d([0]), np.poly1d([0]), np.poly1d([1, (-2 % mod), 1]), np.poly1d([0]), np.poly1d([0]), np.poly1d([(-1 % mod), 2, 0])],
                [np.poly1d([0]), np.poly1d([0]), np.poly1d([0]), np.poly1d([1]), np.poly1d([0]), np.poly1d([0])]]

# end of server contains--------------------

# Start of protocol-------------------------

#print database
print("Database:")
print(snumData)
print("\n")


#userside

# 1 Alice wants 
alice = [1, 0, 0, 0]
alice2 = [0, 1, 0, 0]

#x-coordinates for vectors
xCoor = [0,1]
print("Alice's Basis Vectors:")
print(alice)
print(xCoor[0])
print(alice2)
print(xCoor[1])
print("\n")


# 4 generate polynomial vector out of alice's vector and random point vector
# this is where you use approx lagrange mod
polyVec = create1DPoly(alice, alice2, xCoor)


print("Alice's generate polynomials:")
print(polyVec)
print("\n")

# 5 plug x=3 and x=4 into Alice's polynomial vector to send to the 2 servers
aliceQ1 = computePolyVec(polyVec, 4, 4)
aliceQ2 = computePolyVec(polyVec, 5, 4)
aliceQ3 = computePolyVec(polyVec, 6, 4)
aliceQ4 = computePolyVec(polyVec, 7, 4)

print("Query1 sent to Server 1 with x = 4")
print(aliceQ1)
print("Query2 sent to Server 2 with x = 5")
print(aliceQ2)
print("Query3 sent to Server 3 with x = 6")
print(aliceQ3)
print("Query4 sent to Server 4 with x = 7")
print(aliceQ3)

#severside
print("Email index of queries:")
print(email)
print("\n")

print("Size index of queries:")
print(size)
print("\n")

print("Date index of queries:")
print(date)
print("\n")

print("Batch Index of queries:")
print(batchIndServer)
print("\n")
# 6 server plugs in x to batch index of queries
# server 1
s1_idxq = computeBatchInput(batchIndServer, 4)
# server 2
s2_idxq = computeBatchInput(batchIndServer, 5)
# server 3
s3_idxq = computeBatchInput(batchIndServer, 6)
# server 3
s4_idxq = computeBatchInput(batchIndServer, 7)

print("Server 1 batch index of queries x = 4")
print(s1_idxq)
print("Server 2 batch index of quereis x = 5")
print(s2_idxq)
print("Server 3 batch index of quereis x = 6")
print(s3_idxq)
print("Server 4 batch index of quereis x = 7")
print(s4_idxq)
print("\n")

# 7 Matrix multiply Alice's respective server query and the batch index of queries calculated then convert to mod n
# server 1
s1_Q1 = np.dot( aliceQ1, s1_idxq)
s2_Q2 = np.dot( aliceQ2, s2_idxq)
s3_Q3 = np.dot( aliceQ3, s3_idxq)
s4_Q4 = np.dot( aliceQ4, s4_idxq)
s1_Q1 = convertMod(s1_Q1)
s2_Q2 = convertMod(s2_Q2)
s3_Q3 = convertMod(s3_Q3)
s4_Q4 = convertMod(s4_Q4)

print("Matrix Multiply of Alice's Query 1 and server1")
print(s1_Q1)
print("Matrix Multiply of Alice's Query 2 and server2")
print(s2_Q2)
print("Matrix Multiply of Alice's Query 3 and server3")
print(s3_Q3)
print("Matrix Multiply of Alice's Query 4 and server4")
print(s4_Q4)
print("\n")

# 8 resulting query(x)*indexofqueries(x) matrix multiply to database and converted to mod n
#server1
s1_Q1_data = np.dot(s1_Q1, snumData)
#server2
s2_Q2_data = np.dot(s2_Q2, snumData)
#server3
s3_Q3_data = np.dot(s3_Q3, snumData)
#server3
s4_Q4_data = np.dot(s4_Q4, snumData)

s1_Q1_data = convertMod2(s1_Q1_data)
s2_Q2_data = convertMod2(s2_Q2_data)
s3_Q3_data = convertMod2(s3_Q3_data)
s4_Q4_data = convertMod2(s4_Q4_data)

print("Matrix Multiply of Alice's Query 1, server1, and database")
print(s1_Q1_data)
print("Matrix Multiply of Alice's Query 2, server2, and database")
print(s2_Q2_data)
print("Matrix Multiply of Alice's Query 3, server3, and database")
print(s3_Q3_data)
print("Matrix Multiply of Alice's Query 4, server4, and database")
print(s4_Q4_data)
print("\n")

# 10 Alice reconstructs vectors to polynomial vectors
# this is where you use approximate lagrange mod
serverLab = [4, 5, 6, 7]
resPoly = create4DPoly(s1_Q1_data, s2_Q2_data, s3_Q3_data, s4_Q4_data, serverLab)
print("Reconstructed polynomials from server results:")
print(resPoly)
print("\n")

# 11 Alice inputs x to resultant polynomial vectors to get data
data = computePolyVec(resPoly, 0, 5)
print("Final Result Query 1:")
print(data)
print("Actual Result Query 1:")
print(np.dot(np.dot(alice,email), snumData))

data2 = computePolyVec(resPoly, 1, 5)
print("Final Result: Query 2:")
print(data2)
print("Actual Result Query 2:")
print(np.dot(np.dot(alice2, size), snumData))
print("\n")