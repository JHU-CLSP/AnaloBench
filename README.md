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

### Step 3: Evaluation 

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

### Step 1: Generate Diverse Texts 

**Settings**: Temperature=1.6, Top P=0.95

**Style**: Narrative, Descriptive, Expository, Persuasive, Creative, Objective, Subjective, Review, Poetry, Technical 

**Prompt**:

Generate a 7-10 sentence X style story with respect to the following sentence:

Sentence: ...

[**Exmaples**](./Task2Step1.md)

### Step 2: Extract Analogous Elements 

**Settings**: Temperature=1, Top P=1

**Prompt**:

List the analogous elements between the following 2 stories:

E.g.\
Story1: The boy is lucky to have the man's lifelong support to win all the soccer games since they hoped it would spread the sport.

Story2: Women are supportive of the girls in their mission to get the dance competition prize since they hoped it would benefit the girls.

Analogies: \
 \- Man <-> Woman | Explanation: they're the supporters in both stories \
 \- Boy <-> Girl | Explanation: they're both being supported in both stories \
 \- Winning the soccer game <-> Winning the dance competition prize | Explanation: the goal of winning in both stories \
...

Story1: The water is flowing fast from a large beaker to a smaller one through a narrow pipe. It was all done in 15 minutes. 

Story2: The parents try to slowly instill bits of knowledge in their child through simple communication. This often takes repetition. 

Analogies: \
\- flow <-> instill | Explanation: They're both the action being described.\
 \- large beaker <-> parent | Explanation: they're both the source of the action.\
 \- small beaker <-> child | Explanation: they're both the target of the action in both stories \
 \- water <->  knowledge | Explanation: they're both the object of the action (the content of the flow).\
 \- narrow pipe <-> communication | Explanation: they're both the means of the action (how the flow happens).\
 ...

Story1: ... \
Story2: ... 

[**Exmaples**](./Task2Step2.md)

### Step 3: Generate Incorrect Analogous Elements 

Given two stories, incorrectly identify the analogous elements without considering the subjects and their experiences in both scenarios. Remember to mismatch the subjects and their struggles.

E.g.\
Story1: The boy is lucky to have the man's lifelong support to win all the soccer games since they hoped it would spread the sport. 

Story2: Women are supportive of the girls in their mission to get the dance competition prize since they hoped it would benefit the girls.

Incorrect Analogies: \
 \- Winning the soccer game <-> Girls | Explanation: Winning the soccer game is the goal in the first story, girls are the subject in the second story. \
 \- Boy <-> Winning the dance competition prize | Explanation: Boy is the subject being supported in the first story, whereas winning the dance competition is the goal in the second story.\
 \- Man <-> Dance competition | Explanation: Man is the supporter in the first story, dance competition is the event in the second story.\
...

Story1: ...\
Story2: ...

[**Exmaples**](./Task2Step3.md)

### Step 4: Evaluation

**Settings**: Temperature=1, Top P=1

**Prompt**:

The following is a multiple-choice question. Please select all options that you believe are correct.\
NOTE: Only generate the index.

Identify the analogies between the following 2 stories:

Story1: ...\
Story2: ...

A. ...\
...

[**Exmaples**](./Task2Step4.md)

### Discussion:

Regarding Step 1: Story Generation, my current idea is to randomly assign 10 different styles when generating various stories. Also, should we limit the length of some stories? Some stories would be too long for human participants.

Regarding Step 2: Analogy Extraction, I am currently concerned about whether we should set a maximum limit on the number of analogy elements.

Regarding Step 3: Incorrect Analogy, I've observed that the current incorrect options seem too easy for GPT-4. I am experimenting with prompting GPT-4 but am uncertain about the types of incorrect analogies that would effectively mislead it.

Regarding Step 4: Evaluation, I've attempted to shuffle the order of options, but the results have remained consistent.


## Task 3: Human Names Analogy Extraction

### Step 1: Add Names

**Settings**: Temperature=1, Top P=1

**Prompt**:

### Step 2: Extract Analogous Elements 

### Step 3: Generate Incorrect Analogous Elements

### Step 4: Evaluation 