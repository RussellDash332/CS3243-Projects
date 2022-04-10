# CS3243 Projects
This repository serves as my solutions to the projects assigned on **CS3243: Introduction to Artificial Intelligence**.

## Project 1 - Uninformed and Informed Search
The task is using **BFS, DFS, UCS, and A\*** to implement the King's Maze.
You start with a chessboard, a single king of your side and a bunch of opponent pieces, as well as the cost for your king to move from one square to another. The job is to return a sequence resembling a path from the source to the goal square based on the search algorithm used.

## Project 2 - Local Search and CSP
The task is divided into two parts:
- Given a chessboard and some chess pieces, use **the hill climbing algorithm** to remove some of the pieces such that the remaining pieces will not attack each other.
- Given a bunch of unassigned chess pieces, use **CSP (Constraint Satisfaction Problem)** to assign each piece into some square such that no two pieces will attack each other, provided each square is occupied by at most one piece. Some heuristics to select the variable and value to assign may be implemented to improve the code's performance.

## Project 3 - Adversarial Search
The task is to win a 5x5 chess against different agents where you are a Minimax agent augmented with alpha-beta pruning. The (five) different agents are:
- Dummy agent, picks the first available move regardless of check or checkmate
- Random agent, picks any of the available move randomly regardless of check or checkmate
- Greedy agent, picks the move that results in checkmate, check, or neither in that particular ordering
- Smart agent, picks the move that results in the highest utility, calculated on a certain evaluation function of the grader's
- Minimax agent, of depth exactly 4, picks the move based on the **Minimax algorithm**, where when the depth limit is reached, evaluates the state based on the same evaluation function as the one used in the smart agent

# Disclaimer
- All templates and PDF files are the courtesy of the CS3243 teaching team.
- You have been warned, the code may look so bad. (but it works :D)
- This README might be modified in due course.

# The Actual Twist
As the repository description says, this project is to be done in the fastest way I can think of (not that I'm challenging myself). Since code design is not graded and only algorithm correctness is checked, I have to deeply apologize to CS2030 for totally violating all the existing OOP laws and go with the CS2040 style.

If you can't stand looking at the time spent on working on the project, please ignore the parts below. My biggest apologies for that.

## Project 1: 12+ hours
As long as the algorithm is correct, I don't see any problem. What takes most of the time here is the familiarity of the config files and figuring out the way to parse it, then coming up with a way to store the successor states (and the possible actions). Once it's done, the algorithms can be *yeet*ed straight out from the AIMA book or the lecture slides, whichever we see fit.

## Project 2: 6 hours
Not much parsing issue in this project since we can reuse the ones from Project 1. Again, *yeet* the algorithm from AIMA or lecture slides, and then come up with a good random seed value (this is crucial as it may affect your code's reproducibility). Another thing to take note of is how to model the problem, since the graph approach is more sensible to me, allowing me to model the conflicts simply as edges and count the heuristic from there.

The heuristic I could think of for local search is the number of conflicts, assuming all piece can leap over other pieces. If I don't assume such, it might take more time to compute the heuristic because I have to take into account more conditions. The hill climbing algorithm also had to be slightly modified by incorporating sideway moves and random restart.

For CSP, the heuristic I used is simply a way to order the pieces to check first (similar to least constraining value (LCV) heuristic), the rest is mostly the stochastic version of the sequence with no heuristic.

## Project 3: 9 hours
Spent the first 6 hours to finalize the skeleton code which again consists of parsing and a way to implement the dummy and the random agent, plus enumerating the list of actions for each player. Took an almost-2-week hiatus for no reason and thus I only had one day left to complete the project (starting early indeed).

The final 3 hours is to implement the Minimax algorithm, incorporate alpha-beta pruning, and determine the depth. As stated inside the code, using `depth = 3` will make me exceeding the time limit for the last test case (against minimax agent). However, using `depth = 2` will always make me draw against that same agent. Thus, a mixture of both is used so that **I can win instead of a draw**, and **I can pass the time limit**.

Sadly due to CodePost's constraint, I can only have 5 rounds for each of the first four agents and 1 round for the last one. Hence, the logs processor came to be. See its `README.md` inside `Project 3` for more information.