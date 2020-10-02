Suppose you have a random finite set of colored tokens and you have to arrange them in a grid according to the following set of rules.

1) As many tokens as possible must be used in the grid.
2) A cell can have at most one color of token in it
3) Each row and column cannot have two cells which share the same color
4) For each row, the number of tokens in the first cell must be exactly 1 or 0, in the second cell exactly 2 or 0, ... in the kth cell exactly k or 0 and so on
5) For each row, you cannot fill in a cell if the previous cells have not been filled.

Question: Given a collection of colored tokens, is it possible to fill a grid such that there are no tokens remaining from the collection?

This tool was designed to answer this question.
The primary use is with scenario.main(set_of_tokens)

R G B Y O are the colors supported currently
'*' denotes empty space

ex. Suppose I want to know if starting with 3 red, 3 green, 3 blue tokens if it's possible to fill the grid.
scenario.main((3, 3, 3)) gives the following result (as columns)
(('B', 'G', 'R'), ('R', 'B', 'G'))
(('R', 'G'), ('G', 'R'), ('B', '*'))
(('B', 'R'), ('R', 'B'), ('*', 'G'))
(('B', 'G'), ('G', 'B'), ('R', '*'))

The first solution is shorthand for
B RR
G BB
R GG

The second solution is shorthand for
R GG BBB
G RR

ex 2. (3, 3, 5) is impossible, and so returns no solutions
