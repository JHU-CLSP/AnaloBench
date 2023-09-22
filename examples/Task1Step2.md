Settings: Temparature=1, Top p=1
# Example 1:
## Input: 
Given two sentences, incorrectly identify the analogous elements without considering the subjects and their experiences in both scenarios. Remember to mismatch the subjects and their struggles.

E.g.\
Sentence1: The boy is lucky to have the man's lifelong support to win all the soccer games since they hoped it would spread the sport. 

Sentence2: Women are supportive of the girls in their mission to get the dance competition prize since they hoped it would benefit the girls.

Incorrect Analogies:\
 \- Winning the soccer game <-> Girls | Explanation: Winning the soccer game is the goal in the first story, girls are the subject in the second story. \
 \- Boy <-> Winning the dance competition prize | Explanation: Boy is the subject being supported in the first story, whereas winning the dance competition is the goal in the second story.\
 \- Man <-> Dance competition | Explanation: Man is the supporter in the first story, dance competition is the event in the second story.\
...

Sentence1: A forest grew near the river. \
Sentence2: Many students came to study under the guru. 

## 1st Output:

Incorrect Analogies:

 \- Forest <-> Guru | Explanation: Forest is a natural element in the first sentence, while Guru is a human figure in the second sentence.\
 \- River <-> Study | Explanation: River is a water body in the first sentence, whereas study is an activity in the second sentence. \
 \- Grew <-> Students | Explanation: Grew is an action in the first sentence, and students are human figures in the second one.

## 2nd Output: (This one is a correct analogy)

Incorrect Analogies: 

 \- Forest <-> Students | Explanation: Forest is the subject in the first story, while students are the subject in the second story.\
 \- River <-> Guru | Explanation: River is a natural element in the first story, Guru is a human in the second story.\
 \- Growing of the forest <-> Came to study | Explanation: Growing of the forest describes a natural process in the first story, while 'came to study' describes an action performed by students in the second story.

 # Example 2:
## Input: 
Given two sentences, incorrectly identify the analogous elements without considering the subjects and their experiences in both scenarios. Remember to mismatch the subjects and their struggles.

E.g.\
Sentence1: The boy is lucky to have the man's lifelong support to win all the soccer games since they hoped it would spread the sport. 

Sentence2: Women are supportive of the girls in their mission to get the dance competition prize since they hoped it would benefit the girls.

Incorrect Analogies:\
 \- Winning the soccer game <-> Girls | Explanation: Winning the soccer game is the goal in the first story, girls are the subject in the second story. \
 \- Boy <-> Winning the dance competition prize | Explanation: Boy is the subject being supported in the first story, whereas winning the dance competition is the goal in the second story.\
 \- Man <-> Dance competition | Explanation: Man is the supporter in the first story, dance competition is the event in the second story.\
...

Sentence1: A forest grew near the river. \
Sentence2: Many students came to study under the guru. 

## 1st Output:

Incorrect Analogies:

\- Adam <-> Top Shelf | Explanation: Adam is the subject experiencing the struggle in the first story, whereas the top shelf is the object the subject is struggling to reach in the second story.\
\- Understanding the root of the crisis <-> Child | Explanation: Understanding the root of the crisis is the struggle in the first story, child is the subject in the second story.\
\- Crisis <-> Reaching the top shelf | Explanation: Crisis is the struggle in the first story, reaching the top shelf is the task in the second story.

## 2nd Output:

Incorrect Analogies: 

\- Adam <-> The top shelf | Explanation: Adam is the subject who is encountering a problem in the first story, whereas the top shelf is the object in the second story.\
\- Crisis <-> Child | Explanation: Crisis is the problem that needs to be understood in the first story, child is the subject in the second story who is having a difficult time in reaching the top shelf.\
\- Understand the root <-> Reach top shelf | Explanation: Understanding the root is the action needed to solve the problem in the first story, reaching the top shelf is the action which the child can't achieve in the second story.
