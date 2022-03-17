import numpy as np
import math
import random
from scipy.interpolate import lagrange
from numpy.polynomial import Polynomial

#every calculation is based in mod
mod = 11
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
    # topDeg = [0, 0, 0]
    # tempPolys = [0, 0, 0]
    # for i in range(4):
    #     topDeg[0] = pow(((userVec[i][0]-randVec1[i][0])*(userVec[i][0]-randVec2[i][0])), -1, mod)
    #     topDeg[1] = pow((randVec1[i][0]-userVec[i][0])*(randVec1[i][0]-randVec2[i][0]), -1, mod)
    #     topDeg[2] = pow((randVec2[i][0]-userVec[i][0])*(randVec2[i][0]-randVec1[i][0]), -1, mod)
    #     tempPolys[0] = np.poly1d([topDeg[0], ((topDeg[0]*(randVec2[i][0] + randVec1[i][0]))% mod), ((topDeg[0] * (randVec1[i][0] + randVec2[i][0] + userVec[i][1]))% mod)])
    #     tempPolys[1] = np.poly1d([topDeg[1], ((topDeg[1]*(randVec2[i][0] + userVec[i][0]))% mod), ((topDeg[1] * (userVec[i][0] + randVec2[i][0] + randVec1[i][1]))% mod)])
    #     tempPolys[2] = np.poly1d([topDeg[2], ((topDeg[2]*(randVec1[i][0] + userVec[i][0]))% mod), (topDeg[2] * ((userVec[i][0] + randVec1[i][0] + randVec2[i][1]))% mod)])
    #     res[i] = tempPolys[0] + tempPolys[1] + tempPolys[2]
    #     for j in range(3):
    #         res[i].coeffs[j] = res[i].coeffs[j]%mod

    # topDeg = [0, 0, 0]
    # tempPolys = [0, 0, 0]
    # for i in range(4):
    #     topDeg[0] = pow(((xCoor[0]-xCoor[1])*(xCoor[0]-xCoor[2])), -1, mod)
    #     topDeg[1] = pow((xCoor[1]-xCoor[0])*(xCoor[1]-xCoor[2]), -1, mod)
    #     topDeg[2] = pow((xCoor[2]-xCoor[0])*(xCoor[2]-xCoor[1]), -1, mod)
    #     tempPolys[0] = np.poly1d([topDeg[0], ((topDeg[0]*(xCoor[2] + xCoor[1]))% mod), ((topDeg[0] * (xCoor[1] + xCoor[2] + alice[i]))% mod)])
    #     tempPolys[1] = np.poly1d([topDeg[1], ((topDeg[1]*(xCoor[2] + xCoor[0]))% mod), ((topDeg[1] * (xCoor[0] + xCoor[2] + randVec1[1]))% mod)])
    #     tempPolys[2] = np.poly1d([topDeg[2], ((topDeg[2]*(xCoor[1] + xCoor[0]))% mod), (topDeg[2] * ((xCoor[0] + xCoor[1] + randVec2[1]))% mod)])
    #     res[i] = tempPolys[0] + tempPolys[1] + tempPolys[2]
    #     for j in range(3):
    #         res[i].coeffs[j] = res[i].coeffs[j]%mod
        
    # for idx, i in enumerate(userVec):
    #     slope = pow((randVec[idx][0]-userVec[idx][0]), -1, 11) * ((randVec[idx][1] - userVec[idx][1]) % mod)
    #     res[idx] = np.poly1d([slope, userVec[idx][1]])
    # temp = [0, 0, 0]
    # tempPoly = 0
    # for i in range(4):
    #     temp[0] = alice[i]
    #     temp[1] = randVec1[i]
    #     temp[2] = randVec2[i]
    #     poly=lagrange(xCoor, temp)
    #     print(poly)
    #     for idx,j in enumerate(poly.coeffs):
    #         poly.coeffs[idx] = i % mod  
    #     res[i] = np.poly1d(poly.coeffs)
    #     print(poly)
    #     print(poly.coeffs)
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

# 1 Alice wants Elizabeth's largest email
alice = [0, 0, 1, 0]
x=1
print("Alice's wanted index of queries:")
print(x)
print("(size)")
print("Alice wants to see Elizabeth")
print("\n")
#x-coordinates for vectors
xCoor = [0,1,2]
print("Alice's Vector:")
print(alice)
print(xCoor[0])
print("\n")

# 2 generate random points vector
randPoints1 = randomPoints(1)
randPoints2 = randomPoints(2)
print("Random points vector1:")
print(randPoints1)
print(xCoor[1])
print("\n")
print("Random points vector2:")
print(randPoints2)
print(xCoor[2])
print("\n")

# 4 generate polynomial vector out of alice's vector and random point vector
# this is where you use approx lagrange mod
polyVec = createPolynomials(alice, randPoints1, randPoints2, xCoor)
#polyVec = createPolynomials_Recon(userVec, randPoints1)
# tempx = [0 for i in range(2)]
# tempy = [0 for i in range(2)]
# for idx, i in enumerate(userVec):
#         tempx[0] = userVec[idx][0]
#         tempx[1] = userVec[idx][0]
#         tempy[0] = userVec[idx][1]
#         tempy[1] = userVec[idx][1]
# for idx, i in enumberate(userSet)
#polyVec = createPoly(userVec, randPoints)

print("Alice's generate polynomials:")
print(polyVec)
print("\n")

# 5 plug x=3 and x=4 into Alice's polynomial vector to send to the 2 servers
aliceQ1 = computePolyVec(polyVec, 3, 4)
aliceQ2 = computePolyVec(polyVec, 4, 4)
aliceQ3 = computePolyVec(polyVec, 5, 4)
aliceQ4 = computePolyVec(polyVec, 6, 4)
aliceQ5 = computePolyVec(polyVec, 7, 4)
print("Query1 sent to Server 1 with x = 3")
print(aliceQ1)
print("Query2 sent to Server 2 with x = 4")
print(aliceQ2)
print("Query3 sent to Server 3 with x = 5")
print(aliceQ3)
print("Query2 sent to Server 4 with x = 6")
print(aliceQ4)
print("Query3 sent to Server 5 with x = 7")
print(aliceQ5)
print("\n")

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
s1_idxq = computeBatchInput(batchIndServer, 3)
# server 2
s2_idxq = computeBatchInput(batchIndServer, 4)
# server 3
s3_idxq = computeBatchInput(batchIndServer, 5)
# server 4
s4_idxq = computeBatchInput(batchIndServer, 6)
# server 5
s5_idxq = computeBatchInput(batchIndServer, 7)
print("Server 1 index of queries x = 3")
print(s1_idxq)
print("Server 2 index of quereis x = 4")
print(s2_idxq)
print("Server 3 index of quereis x = 5")
print(s3_idxq)
print("Server 4 index of quereis x = 6")
print(s4_idxq)
print("Server 5 index of quereis x = 7")
print(s5_idxq)
print("\n")

# 7 Matrix multiply Alice's respective server query and the batch index of queries calculated then convert to mod n
# server 1
s1_Q1 = np.dot( aliceQ1, s1_idxq)
s2_Q2 = np.dot( aliceQ2, s2_idxq)
s3_Q3 = np.dot( aliceQ3, s3_idxq)
s4_Q4 = np.dot( aliceQ4, s4_idxq)
s5_Q5 = np.dot( aliceQ5, s5_idxq)
s1_Q1 = convertMod(s1_Q1)
s2_Q2 = convertMod(s2_Q2)
s3_Q3 = convertMod(s3_Q3)
s4_Q4 = convertMod(s4_Q4)
s5_Q5 = convertMod(s5_Q5)
print("Matrix Multiply of Alice's Query 1 and server1")
print(s1_Q1)
print("Matrix Multiply of Alice's Query 2 and server2")
print(s2_Q2)
print("Matrix Multiply of Alice's Query 3 and server3")
print(s3_Q3)
print("Matrix Multiply of Alice's Query 4 and server4")
print(s4_Q4)
print("Matrix Multiply of Alice's Query 5 and server5")
print(s5_Q5)
print("\n")

# 8 resulting query(x)*indexofqueries(x) matrix multiply to database and converted to mod n
#server1
s1_Q1_data = np.dot(s1_Q1, snumData)
#server2
s2_Q2_data = np.dot(s2_Q2, snumData)
#server3
s3_Q3_data = np.dot(s3_Q3, snumData)
#server2
s4_Q4_data = np.dot(s4_Q4, snumData)
#server3
s5_Q5_data = np.dot(s5_Q5, snumData)
s1_Q1_data = convertMod2(s1_Q1_data)
s2_Q2_data = convertMod2(s2_Q2_data)
s3_Q3_data = convertMod2(s3_Q3_data)
s4_Q4_data = convertMod2(s4_Q4_data)
s5_Q5_data = convertMod2(s5_Q5_data)
print("Matrix Multiply of Alice's Query 1, server1, and database")
print(s1_Q1_data)
print("Matrix Multiply of Alice's Query 2, server2, and database")
print(s2_Q2_data)
print("Matrix Multiply of Alice's Query 3, server3, and database")
print(s3_Q3_data)
print("Matrix Multiply of Alice's Query 4, server4, and database")
print(s4_Q4_data)
print("Matrix Multiply of Alice's Query 5, server5, and database")
print(s5_Q5_data)
print("\n")

# 9 Alice convert vectors s1_Q1_data and s2_Q2_data to point vectors with respective x to server
# s1_res = vectorToPoint_Server(s1_Q1_data, 3)
# s2_res = vectorToPoint_Server(s2_Q2_data, 4)
# s3_res = vectorToPoint_Server(s3_Q3_data, 5)
# print("Server1 results")
# print(s1_res)
# print("Server2 results")
# print(s2_res)
# print("Server3 results")
# print(s3_res)
# print("\n")

# 10 Alice reconstructs vectors to polynomial vectors
# this is where you use approximate lagrange mod
serverLab = [3, 4, 5, 6, 7]
print("fail")
resPoly = createPolynomials4Deg(s1_Q1_data, s2_Q2_data, s3_Q3_data, s4_Q4_data, s5_Q5_data, serverLab)
print("Reconstructed polynomials from server results:")
print(resPoly)
print("\n")

# 11 Alice inputs x to resultant polynomial vectors to get data
data = computePolyVec(resPoly, x, 5)
print("Final Result:")
print(data)
print("\n")