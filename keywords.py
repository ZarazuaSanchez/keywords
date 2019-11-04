import sys
from math import floor
from itertools import accumulate

mergelist = lambda x, y: x + y
ifsame = lambda x, y: (y[0], y[1]+x[1]) if x[0]==y[0] else y

def toBool(letter):

    if letter=='Y':
        return True
    elif letter=='N':
        return False
    else:
        raise SyntaxError("Argument must be Y or N")

def makeNoDupList(l):

    it = iter(l)
    prev = next(it)
    w1, cnt1 = prev[0], prev[1]
    cur = next(it)

    while(cur):
        w2, cnt2 = cur[0], cur[1]
        if w1!=w2:
            yield (w1, cnt1)
        prev = cur
        w1, cnt1 = prev[0], prev[1]
        cur = next(it, None)

    yield (w1, cnt1)

def removeStopWords(l, uppercase=False):

        stopwords = []

        with open("stopwords.txt", 'r') as f:
            lines = f.readlines()
            for stopw in lines:
                stopw = stopw.rstrip('\n')
                modw = stopw
                if uppercase:
                    modw = recupper(stopw)
                else:
                    modw = reclower(stopw)
                stopwords.append(modw)

        it = iter(l)
        cur = next(it)

        while(cur):
            if cur[0] not in stopwords:
                yield cur
            cur = next(it, None)

def reclower(s):

    mid = floor(len(s)/2)

    if mid==0:
        return s.lower()
    elif mid>0:
        return reclower(s[:mid]) + reclower(s[mid:])

def recupper(s):

        mid = floor(len(s)/2)

        if mid==0:
            return s.upper()
        elif mid>0:
            return recupper(s[:mid]) + recupper(s[mid:])

def keywords(input, k, output, mostfrequent=True, uppercase=False):
    print()
    allmywords = []
    allmykw = []

    #put all words in a list
    with open(input, 'r') as f:
        for s in f:
            if uppercase:
                s = recupper(s)
            else:
                s = reclower(s)
            somekw = recsplit(s, [], ' .,?;!-()')
            allmywords = mergelist(allmywords, somekw)

    allmywords = sorted(allmywords)
    # print(allmywords)
    tuplist = list(map(lambda x: (x, 1), allmywords))
    # print("tuplist\n****************************")
    # print(tuplist)
    kwcount = list(accumulate(tuplist, ifsame))
    # print("kwcount\n****************************")
    # print(kwcount)
    noDupListMaker = makeNoDupList(kwcount)
    singleEntries = list(next(noDupListMaker) for _ in range(len(kwcount)))
    # print("Final List\n*****************************")
    # print(singleEntries)
    if mostfrequent:
        byfreq = sorted(singleEntries,key=lambda x:x[1],reverse=True)
    else:
        byfreq = sorted(singleEntries,key=lambda x:x[1],reverse=False)
    # print("By Freq List?\n*****************************")
    # print(byfreq)
    noStopWordsMaker = removeStopWords(byfreq, uppercase)
    noStopWords = list(next(noStopWordsMaker) for _ in range(len(byfreq)))
    # print("No Stop Words?\n*****************************")
    # print(noStopWords)

    of = open(output, 'w+')
    # of2 = open('finalwordcount.txt', 'w+')
    j = 0
    for kw in noStopWords:

        w = kw[0]
        c = kw[1]

        ln =  w + " " + str(c) + "\n"

        # of2.write(ln)

        if j < k:
            of.write(ln)

        #at at kth word check if there are other words with same count
        if j == (k-1):
            cap = c

        if j >= k and cap == c:
            of.write(ln)

        j += 1

    of.close()


def recsplit(s, kwlist, seps):

    if s=='':
        return kwlist

    if len(seps) == 1:
        splitList = s.split(seps)

        for s1 in splitList:
            if s1.isalpha():
                kwlist.append(s1)

        return kwlist

    else:

        nxtRndWords = []
        seps2 = seps[1:3]

        if len(seps2) > 1:
            currSep = seps[0]
            nextSep = seps[1]
        else:
            currSep = seps
            nextSep = ''

        splitList = s.split(currSep)

        for s1 in splitList:

            if s1.isalpha():
                kwlist.append(s1)
                splitList.remove(s1)

            elif s1.isdigit():
                splitList.remove(s1)

            elif not s1:
                splitList.remove(s1)

        s = nextSep.join(splitList)

        return recsplit(s, kwlist, seps[1:])

def testRecsplit():
    l = [('bored', 1), ('boring', 1), ('cheese', 1), ('cheese', 2), ('count', 1), ('count', 2), ('count', 3), ('words', 1), ('words', 2), ('final', 1)]
    list1 = ['count', 'words', 'boring', 'cheese']
    print("list1 = ", list1)
    line = "count all the words. all the words count"
    print("line = ", line)
    res = sorted(recsplit(line,[],' .,?;!-()'))
    print("recsplit(line,[],' .,?;!-()') = ",res)
    print("mergelist(list1, recsplit(...)) = ", sorted(mergelist(list1,res)))

if __name__ == '__main__':

    args = sys.argv[1].split(';')

    if len(args) == 5:
        #Run program
        kw_args = {}
        for s in args:
            a = s.split("=")
            if a[0] in ('input', 'k', 'mostfrequent', 'uppercase', 'output'):
                kw_args[a[0]] = a[1]
            else:
                msg = 'Invalid argument keywords: ' + '***' + a[0] + '***' + ' not a keywords'
                raise SyntaxError(msg)

        #find keywords
        mostfrequent = toBool(kw_args['mostfrequent'])
        uppercase = toBool(kw_args['uppercase'])

        keywords(kw_args['input'],
                 int(kw_args['k']),
                 kw_args['output'],
                 mostfrequent,
                 uppercase,
                )
    else:
        raise SyntaxError("Incorrect number of arguments!")
