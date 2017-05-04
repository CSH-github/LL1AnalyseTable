
# Author:    Wind-Wing
# Time:     2017/04/30

# Readme
# 1. Default use Capital Letters as non-terminal
#         use non-Capital Letters as terminal
#         use char "e" to represent "ε"
# 2. Use char "S" to represent Start non-terminal for Getting FOLLOW set
# 3. The output must have less than 26 non-terminals( for 26 Capital Letters )
# 4. Please do not add unnecessary blanks
# 5. Please ensure you use the right form to input productions
# or you will get the wrong output

import string
import copy

def Getproductions():
    productions = {}
    print("Please input productionss.\n "
          "Use 's' to represent the Start non-terminal\n" \
          "use 'e' to represent 'ε'" \
          "Split by enter \n" \
          "end by char q : ")
    while True:
        inputSentence = input()
        if inputSentence == "q":
            break
        productions[inputSentence.split("->")[0].strip()] = set(inputSentence.split("->")[1].strip().split("|"))
    return productions

def DisplayProductions(productions):
    for i in productions:
        print(i,end="->")
        for j in productions[i]:
            print(j,end="|")
        print()

def GetNonTerminals(productions):
    ReturnSet = set()
    for i in productions:
        ReturnSet.add(i)
    return ReturnSet

def GetTerminals(productions):
    ReturnSet = set("#")
    for i in productions:
        for j in productions[i]:
            for k in j:
                if not k.isupper():
                    ReturnSet.add(k)
    return ReturnSet

def GetNewNonTerminal(productions):
    nonTerminals = GetNonTerminals(productions)
    newNonTerminal = ""
    for i in string.ascii_uppercase:
        if i not in nonTerminals:
            newNonTerminal = i
            break
    if not newNonTerminal: raise Exception("Too many nonTerminals")
    return newNonTerminal

def EliminateLeftReduction(productions):
    NonTerminals = list(GetNonTerminals(productions))
    n = 0
    for i in NonTerminals:          # Item to be brought in
        for j in NonTerminals[:n]:  # Item to brought in
            # Copy
            newSet = set(productions[i])
            for k in productions[i]:
                # Check whether can be brought in
                if k[0] == j:
                    newSet.update([ x+k[1:] for x in productions[j] ])
                    if not ("e" in productions[j]):
                        newSet.remove(k)
            productions[i] = newSet
            EliminateDirectLeftReduction(i,productions)
        n += 1

# This function is prepared for "EliminateLeftReduction"
def EliminateDirectLeftReduction(nonTerminal,productions):
    a = productions[nonTerminal]
    # Find LeftReductions
    leftReductions = set()
    for i in a:
        if i[0] == nonTerminal:
            if len(i) > 1:
                leftReductions.add(i)
            else: raise Exception("Exist Loop production:\n"+str(productions[nonTerminal]))
    # Check whether find LeftReductions
    if not leftReductions:return
    # Find a new nonTerminal
    newNonTerminal = GetNewNonTerminal(productions)
    # Change the origin production
    a = a.difference(leftReductions)
    productions[nonTerminal] = set([x+newNonTerminal for x in a])
    # Create a new RightRecurse production
    productions[newNonTerminal] = set()
    for i in leftReductions:
        productions[newNonTerminal].add(i[1:]+newNonTerminal)
    productions[newNonTerminal].add("e")

def ExtractLeftFactor(productions):
    #productions = copy.deepcopy(productions)
    nonTerminalSet = GetNonTerminals(productions)
    for i in nonTerminalSet:
        # Use loop to extra many levels of left common factors
        stack = [i]
        while stack:
            # Init
            count = {}
            nonTerminal = stack.pop()
            for j in productions[nonTerminal]:
                count[j[0]] = set()
            # Count
            for j in productions[nonTerminal]:
                count[j[0]].add(j)
            # Check
            if len(count) == len(productions[nonTerminal]):break
            # Extra
            Cflag = False
            for j in count:
                if len(count[j]) <= 1:continue
                newNonTerminal = GetNewNonTerminal(productions)
                productions[nonTerminal] = productions[nonTerminal].difference(count[j])
                productions[nonTerminal].add(j+newNonTerminal)
                newSet = set([x[1:] for x in count[j] if len(x) > 1])
                if len(newSet) < len(count[j]):
                    newSet.add("e")
                productions[newNonTerminal] = newSet
                Cflag = True
                stack.append(newNonTerminal)
            # Second check
            if Cflag:
                stack.append(nonTerminal)

def GetFIRST(productions):
    FIRST = {}
    # Init
    for i in productions:
        FIRST[i] = set()
    # Generate
    flag = True
    while flag:
        # use flag to mark whether there is new elements
        flag = False
        for i in productions:        # i -> k1|k2...
            for k in productions[i]:
                a = k               # A -> α
                X = a[0]            # α = XYZ...
                if not X.isupper():
                    # A -> a...
                    if not X in FIRST[i]:flag = True
                    FIRST[i].add(X)
                else:
                    # A -> Y...
                    newSet = GetStringFIRST(a,FIRST)
                    if newSet.difference(FIRST[i]):flag = True
                    FIRST[i].update(newSet)
    return FIRST

def DisplayFIRST(FIRST):
    for i in FIRST:
        print(i,end="\t|")
        for j in FIRST[i]:
            print(j,end=" ,")
        print()

# Warning!!!
# The input string should begin with Capital Letter
# This function is prepared for "GetFIRST" and "GetFOLLOW"
# Please do not call this function in other place unless you
# understand what happens inside
def GetStringFIRST(String,FIRST):
    if not String:
         returnSet = set()
    elif not String[0].isupper():
        returnSet = set(String[0])
    else:
        returnSet = set(e for e in FIRST[String[0]] if e != "e")
        # Check whether there is e in FIRST[X],FIRST[Y]...
        eflag = True
        for j in String:
            if j.isupper() and 'e' in FIRST[j]:
                jwithoute = set(e for e in FIRST[j] if e != "e")
                returnSet.update(jwithoute)
            else:
                eflag = False
                break
        if eflag:
            returnSet.add("e")
    return returnSet


def GetFOLLOW(productions,FIRST):
    # Init
    FOLLOW = {}
    for i in productions:
        FOLLOW[i] = set()
    # Generate
    FOLLOW['S'].add('#')
    flag = True
    while flag:
        flag = False
        for i in productions:        # A -> X|Y|Z
            for j in productions[i]:             # X
                for index in range(len(j)):    # Spilt j into three part ABC
                    B = j[index]
                    C = j[index+1:]
                    if not B.isupper(): continue
                    FIRSTC = GetStringFIRST(C, FIRST)
                    Cwithoute = set(x for x in FIRSTC if x != "e")
                    if Cwithoute.difference(FOLLOW[B]):flag = True
                    FOLLOW[B].update(Cwithoute)

                    if (not C) or ("e" in FIRSTC):
                        if  FOLLOW[i].difference(FOLLOW[B]):flag =True
                        FOLLOW[B].update(FOLLOW[i])
    return FOLLOW

def DisplayFOLLOW(FOLLOW):
    for i in FOLLOW:
        print(i,end="\t|")
        for j in FOLLOW[i]:
            print(j,end=" ,")
        print()

# Only can apply to LL1
# Because one block in table are designed to store only one production
def GetAnalyseTable(productions,FIRST,FOLLOW,Terminals,NonTerminals):
    #Init
    ReturnTable = {}
    # Create an empty table
    for j in NonTerminals:
        ReturnTable[j] = {}
        for i in Terminals:
            ReturnTable[j][i] = "error"
    # Fill in the table
    for i in productions:                       # i = A,  A->X|Y|Z
        for j in productions[i]:                # j = X, j may be a char or string
            FIRSTA = GetStringFIRST(j,FIRST)
            for k in FIRSTA:                    # k ∈ FIRST(j)
                if k != "e":
                    ReturnTable[i][k] = {i:j}
            if "e" in FIRSTA:
                for k in FOLLOW[i]:
                    ReturnTable[i][k] = {i:j}
    return ReturnTable

def DisplayAnalyseTable(Table,Terminals):
    print("\t|",end ="")
    for i in Terminals:
        print("{0:8}|".format(i),end = "")
    print()
    for V in Table:
        print(V,end = "\t|")
        for T in Table[V]:
            #print(Table[V][T],end="\t|")
            if isinstance(Table[V][T],dict):
                print("{0:1}->{1:5}|".format(list(Table[V][T].keys())[0],list(Table[V][T].values())[0]),end = "")
            else:
                print("{0:8}|".format(Table[V][T]), end="")

        print()

if __name__ == "__test__":
    productions = Getproductions()
    ExtractLeftFactor(productions)
    DisplayProductions(productions)


if __name__ == "__main__":
    choice = 0
    flag = False
    while choice != '8':
        print()
        print("1.Input Productions")
        print("2.Show Productions")
        print("3.Eliminate Left Reduction")
        print("4.Extra Left Common items")
        print("5.Get FIRST Set")
        print("6.Get FOLLOW Set")
        print("7.Get Analyse Table")
        print("8.Quit")
        print()
        choice = input("your choice:")
        if choice == '1':
            productions = Getproductions()
            FIRST = GetFIRST(productions)
            FOLLOW =GetFOLLOW(productions,FIRST)
            Terminals = GetTerminals(productions)
            NonTerminals = GetNonTerminals(productions)
            AnalyseTable = GetAnalyseTable(productions,FIRST,FOLLOW,Terminals,NonTerminals)
            flag = True
        elif flag == False:
            print("Please input Productions")
        elif choice == '2':
            DisplayProductions(productions)
        elif choice == '3':
            EliminateLeftReduction(productions)
            DisplayProductions(productions)
        elif choice == '4':
            ExtractLeftFactor(productions)
            DisplayProductions(productions)
        elif choice == '5':
            DisplayFIRST(FIRST)
        elif choice == '6':
            DisplayFOLLOW(FOLLOW)
        elif choice == '7':
            DisplayAnalyseTable(AnalyseTable, Terminals)


