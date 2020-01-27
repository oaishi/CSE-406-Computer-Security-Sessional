import math

f = open("transposition-37.txt", "r")
content = f.readlines()
content = [x.strip() for x in content]
content = [x.split() for x in content if x != '']
cipherText = content[0][0]
keyWords = content[1][0:]
columnSize = []

def inputformat():
    for x in range(0,len(keyWords)-1):
        keyWords[x] = keyWords[x][:-1].upper()
    keyWords[len(keyWords)-1] = keyWords[len(keyWords)-1].upper()
    # print(cipherText)
    # print(keyWords)

def findColumnSize():

    cipherLength = len(cipherText)
    for i in range(2,cipherLength):
        if cipherLength%i == 0 and i*i<=cipherLength:
            columnSize.append(i);
            columnSize.append(int(cipherLength / i))

    columnSize.sort()

    return columnSize
    #print(columnSize)

def next_permutation(a):
    for i in reversed(range(len(a) - 1)):
        if a[i] < a[i + 1]:
            break  # found
    else:  # no break: not found
        return False  # no next permutation
    j = next(j for j in reversed(range(i + 1, len(a))) if a[i] < a[j])
    a[i], a[j] = a[j], a[i]
    a[i + 1:] = reversed(a[i + 1:])
    return True

def rearrange(permut, s, row, col):
    ret = ''
    for i in range(len(permut)):
        b = permut[i]*row
        e = b+row
        temp = s[b:][:row]
        #print(str(b) + " " + str(row))
        #print("temp: "+ temp)
        #print("old ret: "+ ret)
        ret += temp
        #print("new ret: "+ ret)
    return ret

def transpose(row, col, s):
    plain = ''

    for r in range(row):
        for c in range(col):
            plain += s[r + row * c]

    return plain


def findKeys(row, col, s):

    tempplain = transpose(row,col, s);

    for i in range(len(keyWords)):
        found = tempplain.find(keyWords[i])
        if found == -1:
            return False

    return True

def decrypt():
    plaintext = ''

    for i in range(len(columnSize)-1):
        flag = False
        tempColSize = columnSize[i]
        row = int(len(cipherText) / tempColSize)
        permut = [x for x in range(tempColSize)]

        while True:
            #print(permut)
            temp = rearrange(permut, cipherText, row, tempColSize);
            #print("temp: " + temp)
            flag = findKeys(row, tempColSize, temp)

            if flag:
                plaintext = transpose(row, tempColSize, temp)
                key = permut
                break

            if next_permutation(permut) == False:
                break

        if flag:
            break

    return plaintext,key

def encrypt(s,key):

    col = len(key)
    row = int(len(s)/col)

    ret = ''

    for c in range(col):
        for r in range(row):
            ret += s[c+r*col]

    ret = rearrange(key, ret, row, col)

    return ret

def accuracy(cipher, cipherText):

    errorcount = 0;

    for i in range(len(cipher)):
        if cipher[i] != cipherText[i]:
            errorcount += 1

    return ((len(cipherText) - errorcount)/(len(cipherText)*1.0))*100.0



inputformat()
columnSize = findColumnSize()
plaintext,key = decrypt()
print("plaintext :" + plaintext)
print("key size :"+ str(len(key)))
print("key :")
print(key)
cipher = encrypt(plaintext,key)
print("ciphered text :" + cipher)
print("accuracy :" + str(accuracy(cipher, cipherText)))
