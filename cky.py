# Sylvan Avery Dekker
# University of Massachusetts, Amherst
# LINGUIST 492B
# 1 May 2021

import sys
import math
from collections import defaultdict
from nltk.tree import Tree


PRINT_TREE = False  # Set True to print trees w/ nltk

def getGrammar(grammar):  #
    f = open(grammar)
    CNF_rules = []

    for line in f.readlines():
        rule = line.split()
        if not line.strip():
            continue
        if len(rule) == 3:
            rule = {"prob": float(rule[0]), "parent": rule[1], "child": rule[2]}
        elif len(rule) == 4:
            rule = {"prob": float(rule[0]), "parent": rule[1], "child": tuple(rule[2:])}
        CNF_rules.append(rule)

    return CNF_rules


def getSentences(sen):
    f = open(sen)
    sentences = []

    for line in f.readlines():
        sentences.append(line.strip())

    f.close()

    return sentences


def getNonterminals(grammar):  # Each parent (A) is a key to a list of tuples of possible children [(B, C), (B, C), etc.]
    nonterminals = defaultdict(lambda: [])

    for rule in grammar:
        if type(rule["child"]) is tuple:
            nonterminals[rule["parent"]].append(rule["child"])

    return nonterminals


def isParsable(grammar, sentence, nonterminals):  # Creates table (w/o probs) to check parsability of current sentence
    words = sentence.split()
    word_count = len(words)
    table = defaultdict(lambda:[])

    for i in range(word_count):
        for j in range(word_count - i):

            if i == 0:
                rules = []
                for rule in grammar:
                    if rule["child"] == words[j]:
                        rules.append(rule)
                for rule in rules:  # Adds preterminals to table
                    table[j, j].append(rule["parent"])

            else:
                for k in range(j, j + i):
                    bees = table[k, j]
                    cees = table[j + i, k + 1]
                    for B in bees:
                        for C in cees:
                            for A, children in nonterminals.items():  # Adds nonterminals to table
                                if (B, C) in children:
                                    table[j + i, j].append(A)

    return "ROOT" in table[word_count - 1, 0]  # Returns True if sentence is parsable


def ckyParse(grammar, sentence, nonterminals):
    words = sentence.split()
    word_count = len(words)
    table = defaultdict(lambda:defaultdict(lambda:[]))

    print("PARSING: " + str("{} "*len(words)).format(*words).rstrip())

    if isParsable(grammar, sentence, nonterminals) is True:  # Checks for parsability of current sentence
        pass
    else:
        print("\t> > > No parse.\n")
        print("~" * 128 + "\n")
        return 0

    for i in range(word_count):
        for j in range(word_count - i):

            if i == 0:  # Adds preterminals, associated terminals, & probs to table
                rules = []
                for rule in grammar:
                    if rule["child"] == words[j]:
                        rules.append(rule)
                for rule in rules:
                    p = rule["prob"]
                    p = (0 - math.log(p)) if p != 0 else 0.0
                    table[j][j].append((rule["parent"], p, (words[j], "terminal")))

            else:
                for k in range(j, j + i):
                    bees = table[k][j]
                    cees = table[j + i][k + 1]
                    for B in bees:
                        for C in cees:
                            for rule in grammar:
                                if rule["child"] == (B[0], C[0]):
                                    p = rule["prob"]
                                    p = (0 - math.log(p)) if p != 0 else 0.0
                                    p += B[1]
                                    p += C[1]
                                    bp = (B, C)
                                    table[j + i][j].append((rule["parent"], p, bp))

    parses = table[word_count - 1][0]  # Collect all possible parses

    b, r = 1, 1  # Counters (best, runner-up)

    for parse in parses:  # Print each possible parse
        if parse[1] == (bestParse(parses))[1]:
            print("\n\nBEST PARSE {}: {}\n\t> > > Parse weight: {}".format(b, makeTree(parse), parse[1]))
            if PRINT_TREE:  # Displays nltk trees if True
                t = Tree.fromstring(str(makeTree(parse)))
                t.draw()
            b += 1
        else:
            print("\n\nRUNNER-UP {}: {}\n\t> > > Parse weight: {}".format(r, makeTree(parse), parse[1]))
            if PRINT_TREE:
                t = Tree.fromstring(str(makeTree(parse)))
                t.draw()
            r += 1

    print("\n" + "~" * 128 + "\n")


def makeTree(parse):  # Creates & formats parse based on backpointers
    if parse[2][1] == "terminal":
        return "({} {})".format(parse[0], parse[2][0])
    else:
        tree1 = makeTree(parse[2][0])
        tree2 = makeTree(parse[2][1])
        return "({} {} {})".format(parse[0], tree1, tree2)


def bestParse(parses):
    return min(parses, key=lambda parse: parse[1])


def main():
    grammar = getGrammar(sys.argv[1])
    sentences = getSentences(sys.argv[2])
    nonterminals = getNonterminals(grammar)

    print("\n" + "/ "*25 + "PCKY PARSER " + "/ "*35 + "\n")

    for sentence in sentences:
        ckyParse(grammar, sentence, nonterminals)


if __name__ == "__main__":
    main()
