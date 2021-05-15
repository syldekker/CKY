# CKY

This is a simple implementation of the probabilistic CKY algorithm.

## Description:

* Applies bottom-up parsing and dynamic programming
* Takes context-free grammar in Chomsky Normal Form (CNF) as first command line argument
* Parser runs on second command line argument "sentences.sen"
* Program prints out all valid parses with option for displaying NLTK parse trees (NLTK tree drawing module)

### Known Issues:

* Probabilities are all technically incorrect
  * Mistakenly took log of scores in grammar file (they are already log probabilities)
