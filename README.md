# Analogical-Reasoning
This project focus on curating a robust analogical reasoning dataset for research and development.

## Task 1: Sentence Analogy Extraction

### Step 1: Extract Analogous Elements
**Settings**: Temperature=1, Top P=1

**Prompt**: 

List the analogous elements between the following 2 sentences:

E.g.\
Sentence1: The boy is lucky to have the man's lifelong support to win all the soccer games since they hoped it would spread the sport. 

Sentence2: Women are supportive of the girls in their mission to get the dance competition prize since they hoped it would benefit the girls.

Analogies: \
 \- Man <-> Woman | Explanation: they're the supporters in both stories \
 \- Boy <-> Girl | Explanation: they're both being supported in both stories \
 \- Winning the soccer game <-> Winning the dance competition prize | Explanation: the goal of winning in both stories \
...

Sentence1: ... \
Sentence2: ... 

[**Exmaples**](./Task1Step1.md)

### Step 2: Generate Incorrect Analogous Elements

**Settings**: Temperature=1, Top P=1

**Prompt**:

Given two sentences, incorrectly identify the analogous elements without considering the subjects and their experiences in both scenarios. Remember to mismatch the subjects and their struggles.

E.g.\
Sentence1: The boy is lucky to have the man's lifelong support to win all the soccer games since they hoped it would spread the sport. 

Sentence2: Women are supportive of the girls in their mission to get the dance competition prize since they hoped it would benefit the girls.

Incorrect Analogies: \
 \- Winning the soccer game <-> Girls | Explanation: Winning the soccer game is the goal in the first story, girls are the subject in the second story. \
 \- Boy <-> Winning the dance competition prize | Explanation: Boy is the subject being supported in the first story, whereas winning the dance competition is the goal in the second story.\
 \- Man <-> Dance competition | Explanation: Man is the supporter in the first story, dance competition is the event in the second story.\
...

Sentence1: ...\
Sentence2: ...

[**Exmaples**](./Task1Step2.md)

### Step 3: Evaluation ###

**Settings**: Temperature=1, Top P=1

**Prompt**:

The following is a multiple-choice question. Please select all options that you believe are correct.\
NOTE: Only generate the index.

Identify the analogies between the following 2 sentences:

Sentence1: ...\
Sentence2: ...

A. ...\
...

[**Exmaples**](./Task1Step3.md)

TLDR; As expected, this task is simple to GPT4

## Task 2: Diverse Story Analogy Extraction



## Task 3: Human Names Analogy Extraction
