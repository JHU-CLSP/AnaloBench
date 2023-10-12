import json
import random
import config
import requests


def generate_chat_completion(messages, temperature: float, top_p: float, model="gpt-4",
                             max_tokens: int = 3000):
    API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
    API_KEY = config.GPT4KEY["API_KEY"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
    }

    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


def generate_analogies(story1, story2):
    prompt = f"""
    List the analogous mentions between the following two sentences:

    Here is an example: 
    ========================
    - Story1: The boy is lucky to have the man's lifelong support to win all the soccer games since they hoped it would spread the sport.
    
    - Story2: Women are supportive of the girls in their mission to get the dance competition prize since they hoped it would benefit the girls.

    Analogies:
    - Man <-> Woman | Explanation: they're the supporters in the two stories
    - Boy <-> Girl | Explanation: they're both being supported in the two stories
    - Winning the soccer game <-> Winning the dance competition prize | Explanation: these two mentions are the goal of winning in both stories
    ========================
    - Story1: The water is flowing fast from a large beaker to a smaller one through a narrow pipe. It was all done in 15 minutes.
    
    - Story2: The parents try to slowly instill bits of knowledge in their child through simple communication. This often takes repetition.
    
    Analogies:
    - flow <-> instill | Explanation: They're both the action being described.
    - large beaker <-> parent | Explanation: they're both the source of the action.
    - small beaker <-> child | Explanation: they're both the target of the action in both stories
    - water <-> knowledge | Explanation: they're both the object of the action (the content of the flow).
    - narrow pipe <-> communication | Explanation: they're both the means of the action (how the flow happens).
    ========================
    - Story1: {story1}
    
    - Story2: {story2}
    
    Analogies:
    """
    prompt = [
        {"role": "user", "content": prompt}
    ]
    return generate_chat_completion(prompt, temperature=2.0, top_p=0.95)


# def sentence_incorrect(sentence1, sentence2):
#     prompt = f"""
#     Given two sentences, incorrectly identify the analogous elements without considering the subjects and their experiences in both scenarios. Remember to mismatch the subjects and their struggles.

#     E.g.
#     Sentence1: The boy is lucky to have the man's lifelong support to win all the soccer games since they hoped it would spread the sport.

#     Sentence2: Women are supportive of the girls in their mission to get the dance competition prize since they hoped it would benefit the girls.

#     Incorrect Analogies:
#     - Winning the soccer game <-> Girls | Explanation: Winning the soccer game is the goal in the first story, girls are the subject in the second story.
#     - Boy <-> Winning the dance competition prize | Explanation: Boy is the subject being supported in the first story, whereas winning the dance competition is the goal in the second story.
#     - Man <-> Dance competition | Explanation: Man is the supporter in the first story, dance competition is the event in the second story.
#     ...

#     Sentence1: {sentence1}

#     Sentence2: {sentence2}

#     Analogies:
#     """
#     prompt = [
#         {"role": "user", "content": prompt}
#     ]
#     return generate_chat_completion(prompt)

# def comnbine_shuffle_options(correct_output, incorrect_output):
#     correct_output_items = correct_output.split("\n")
#     incorrect_output_items = incorrect_output.split("\n")

#     combined_output_items = correct_output_items + incorrect_output_items
#     indexed_list = list(enumerate(combined_output_items))

#     # Shuffle the list
#     random.shuffle(indexed_list)

#     # Extract the shuffled values
#     shuffled_values = [item[1] for item in indexed_list]

#     # Extract the original indices for the first k items
#     original_indices_for_correct = [chr(ord('A') + item[0]) for item in indexed_list[:len(correct_output)]]
#     options = []
#     for i, item in enumerate(shuffled_values):
#         index_label = chr(ord('A') + i)
#         options.append(f"{index_label}. {item}")
#     options = "\n".join(options)
#     return options, original_indices_for_correct

# def sentence_evaluation(sentence1, sentence2, correct_output, incorrect_output):
#     options, correct_indices = comnbine_shuffle_options(correct_output, incorrect_output)

#     prompt = f"""
#     The following is a multiple-choice question. Please select all options that you believe are correct.
#     NOTE: Only generate the index.

#     Identify the analogies between the following 2 sentences:

#     Sentence1: {sentence1}

#     Sentence2: {sentence2}

#     Options:
#     {options}
#     """
#     prompt = [
#         {"role": "user", "content": prompt}
#     ]

#     return prompt, correct_indices

def generate_diverse_story(sentence, cur_style):
    prompt = f"""
    Given the following sentence, expand it into a 10-sentence story  in a {cur_style} style. 

    Sentence: {sentence}
    """

    prompt = [
        {"role": "user", "content": prompt}
    ]

    return generate_chat_completion(prompt, temperature=1.9, top_p=0.95)


# def story_incorrect(story1, story2):
#     prompt = f"""
#     Given two stories, incorrectly identify the analogous elements without considering the subjects and their experiences in both scenarios. Remember to mismatch the subjects and their struggles.

#     E.g.
#     Story1: The boy is lucky to have the man's lifelong support to win all the soccer games since they hoped it would spread the sport.

#     Story2: Women are supportive of the girls in their mission to get the dance competition prize since they hoped it would benefit the girls.

#     Incorrect Analogies:
#     - Winning the soccer game <-> Girls | Explanation: Winning the soccer game is the goal in the first story, girls are the subject in the second story.
#     - Boy <-> Winning the dance competition prize | Explanation: Boy is the subject being supported in the first story, whereas winning the dance competition is the goal in the second story.
#     - Man <-> Dance competition | Explanation: Man is the supporter in the first story, dance competition is the event in the second story.
#     ...

#     Story1: {story1}
#     Story2: {story2}

#     Incorrect Analogies:
#     """
#     prompt = [
#         {"role": "user", "content": prompt}
#     ]
#     return generate_chat_completion(prompt)

# def story_evaluation(story1, story2, correct_output, incorrect_output):
#     options, correct_indices = comnbine_shuffle_options(correct_output, incorrect_output)

#     prompt = f"""
#     The following is a multiple-choice question. Please select all options that you believe are correct.
#     NOTE: Only generate the index.

#     Identify the analogies between the following 2 stories:

#     Story1: {story1}
#     Story2: {story2}

#     Options:
#     {options}
#     """
#     prompt = [
#         {"role": "user", "content": prompt}
#     ]
#     return prompt, correct_indices


def generate_stories_with_human_names(name_set, story):
    prompt = f"""
    In the given story, assign human names (e.g., James) to each mention in the given story. You should use only the names in the provided "Name Set" and must use at least 5 names.
    Here is the Name Set: {name_set}

    Here are a few examples:
    - Story: 
    A forest grew near the river.
    
    - Modified Story: 
    A forest named James grew near the river named Thomas.
    ==========
    - Story: 
    A forest grew near the river, a haven where nature thrived and the interconnected chain of life flourished. It was a land in which each living being had a place in the perpetual cycle of existence, an intricate balance between the many species found within its depths. Towering trees guarded the landscape, symbolizing the majesty and authority of the forest.
    The river itself was a life-giving force, coursing through the forest like veins, and connecting the many habitats in a cohesive, symbiotic relationship. The abstract hierarchy within this forest was a beautifully arranged symphony filled with diverse players, each contributing their individual melodies to the overall harmony. Its theme was rooted in resilience, perseverance, and the delicate interrelationship between every living inhabitant.
    As the seemingly chaotic landscape extended from the river, it offered a stunning reminder of the ever-present theme, binding all its living creatures through the hierarchy of life and ensuring their survival for generations to come.
    
    - Modified Story: 
    A forest named Jessica grew near the river named Jeffrey, a haven where nature thrived and the interconnected chain of life, personified as Elaine, flourished. It was a land in which each living being, symbolized by Will, had a place in the perpetual cycle of existence, an intricate balance between the many species, represented by Gabriella, found within its depths. Towering trees named Charles guarded the landscape, symbolizing the majesty and authority of the forest.
    The river itself, Jeffrey, was a life-giving force, coursing through the forest, Jessica, like veins, and connecting the many habitats in a cohesive, symbiotic relationship. The abstract hierarchy, represented by Sophia, within this forest was a beautifully arranged symphony filled with diverse players, each contributing their individual melodies to the overall harmony. Its theme was rooted in resilience, perseverance, and the delicate interrelationship, embodied by Edward, between every living inhabitant.
    As the seemingly chaotic landscape, known as Dean, extended from the river, Jeffrey, it offered a stunning reminder of the ever-present theme, binding all its living creatures through the hierarchy of life, Sophia, and ensuring their survival for generations to come.
    ==========
    - Story: 
    {story}
    
    - Modified Story:
    """

    prompt = [
        {"role": "user", "content": prompt}
    ]

    return generate_chat_completion(prompt, temperature=1.1, top_p=0.96)


def extract_analogies_between_named_stories(story1, story2):
    prompt = f"""
    Extract all analogous elements in the two given stories in the following format, while excluding specific entities mentioned in the stories:

    - Name 1 (from Story 1) <-> Name 2 (from Story 2) | Explanation: ...

    E.g.
    Story1:
    A forest named Jessica grew near the river named Jeffrey, a haven where nature thrived and the interconnected chain of life, personified as Elaine, flourished. It was a land in which each living being, symbolized by Will, had a place in the perpetual cycle of existence, an intricate balance between the many species, represented by Gabriella, found within its depths. Towering trees named Charles guarded the landscape, symbolizing the majesty and authority of the forest.
    The river itself, Jeffrey, was a life-giving force, coursing through the forest, Jessica, like veins, and connecting the many habitats in a cohesive, symbiotic relationship. The abstract hierarchy, represented by Sophia, within this forest was a beautifully arranged symphony filled with diverse players, each contributing their individual melodies to the overall harmony. Its theme was rooted in resilience, perseverance, and the delicate interrelationship, embodied by Edward, between every living inhabitant.
    As the seemingly chaotic landscape, known as Dean, extended from the river, Jeffrey, it offered a stunning reminder of the ever-present theme, binding all its living creatures through the hierarchy of life, Sophia, and ensuring their survival for generations to come.
    Story2:
    Many students, represented by Clara, came to study under the guru, referred to as Samuel, eager to learn ancient wisdom and gain spiritual enlightenment. The guru, Samuel, a wise and humble figure, welcomed them to his serene abode, named Nora, situated on the edge of a lush, green valley embodied by Martin. The students, Clara, hailing from different corners of the world, followed a strict hierarchy, personified by Bella, with newcomers at the base and veteran disciples, epitomized by Leo, occupying higher echelons.
    Beneath this hierarchy, Bella, was a deeper structure, characterized by Amy, that emphasized personal growth and self-improvement; each level came with a set of specific practices and lessons tailored to the individual's progress. This abstract hierarchical theme, represented by Jared, allowed the students' collective knowledge and experiences, symbolized by Rebecca, to not only rise to the surface but also merge seamlessly, creating a cohesive foundation for their personal development, Eleanor.
    As they climbed the ranks, students, Clara, found their understanding deepening, and their worlds expanding in ways they never thought possible. The guru's teachings, Samuel's insights, resonated within their souls, symbolizing Elias, as they embraced the interconnected relationships, culminating in the ultimate realization that this abstract hierarchical theme, Jared, had led them to the truth, embodied by Max, buried within themselves. This encapsulates the overall harmony and progression within the community, captured by the name Mila.
    Output:
    - Jessica <-> Clara | Explanation: Both Jessica and Clara represent the main body or community where numerous entities reside and interact in each story. Jessica is the forest where various species coexist while Clara symbolizes the group of students seeking wisdom from the guru.
    - Jeffrey <-> Samuel | Explanation: Jeffrey as the river is the life-giving force in the forest, connecting habitats allows for the survival of many species. In a similar way, Samuel as the guru connects the disciples, imparting wisdom and guidance that nourish their spiritual growth.
    - Elaine <-> Bella | Explanation: Elaine as the chain of life and Bella as the hierarchy both embody the structure within each community. They dictate how entities interact and what roles they play.
    - Charles <-> Leo | Explanation: Both Charles and Leo represent authority inside their respective environment. Charles stands for the towering trees which are the majestic symbol of the forest. Leo corresponds to the veteran disciples who are higher in the hierarchy of students.
    - Sophia <-> Jared | Explanation: Sophia and Jared symbolize the abstract hierarchical theme in each setting. They illustrate the interconnectedness and order within the forest and the learning community respectively.
    - Edward <-> Max | Explanation: Edward, as the interrelationship in the forest, and Max, as the truth found in the spiritual journey, denote the crucial realization or goal in each story. They represent the ultimate purpose or result of being part of the forest or studying under the guru.
    - Dean <-> Mila | Explanation: Dean as the seemingly chaotic landscape extending from the river, and Mila as the harmony within the students' community, both demonstrate the overall landscape or environment where their respective inhabitants reside. They encapsulate the entire scene and its entities, displaying how it all comes together.


    Story1: {story1}
    Story2: {story2}
    Output:
    """
    prompt = [
        {"role": "user", "content": prompt}
    ]
    return generate_chat_completion(prompt, temperature=2.0, top_p=0.95)


def random_names():
    # extarcted from: https://www.soybomb.com/tricks/words/
    names = [
        "junkhavents",
        "pedistrings",
        "ablesselles",
        "logyroing",
        "repewter",
        "subcons",
        "denonpoite",
        "ormistiroyd",
        "clemor",
        "loaffeed",
        "wrigott",
        "signatmoured",
        "staffleezing",
        "patturusly",
        "reprain",
        "winnonals",
        "unexcraw",
        "canordent",
        "cravians",
        "assectur",
        "exanalyze",
        "dispreinters",
        "heigate",
        "belloverhayn",
        "waldnes",
        "contanizes",
        "wisele",
        "compats",
        "ponessedandy",
        "propier",
        "bushocracushel",
        "haysic",
        "ficided",
        "contramently",
        "searines",
        "profity",
        "avence",
        "calcully",
        "docted",
        "vinize",
        "prephammer",
        "wiellizes",
        "movated",
        "aggripations",
        "fleciah",
        "icalized",
        "odiescring",
        "mizationts",
        "creansy",
        "boulating",
        "shoundedoms",
        "paperfoilstor",
        "ciently",
        "elegankles",
        "mcinteled",
        "bufficle",
        "gregar",
        "comeand",
        "distrum",
        "shievely",
        "bibbleters",
        "bitate",
        "concie",
        "begullian",
        "manproges",
        "favoicas",
        "tracceaned",
        "piloves",
        "evilets",
        "physia",
        "insimulty",
        "austumbright",
        "agrably",
        "flamule",
        "buking",
        "bewidths",
        "mckafka",
        "orstic",
        "rapenizing",
        "calify",
        "clathetizes",
        "sclizers",
        "strichble",
        "subobbed",
        "alized",
        "alition",
        "alyzers",
        "storountly",
        "suitudiew",
        "scorifie",
        "garrously",
        "astions",
        "westruse",
        "digiracts",
        "equinoterse",
        "setturnfult",
        "obtatops",
        "guranences",
        "thorbiker",
    ]
    return names


def generate_stories_with_random_names(name_set, story):
    prompt = f"""
    In the given story, replace each entity with one of names in the provided list "Name Set" and must use at least 5 names.
    Here is the Name Set: {name_set}

    Here are a few examples:
    - Story: 
    A forest grew near the river.

    - Modified Story: 
    An unexcraw grew near the assectur.
    ==========
    - Story: 
    A forest grew near the river, a haven where nature thrived and the interconnected chain of life flourished. It was a land in which each living being had a place in the perpetual cycle of existence, an intricate balance between the many species found within its depths. Towering trees guarded the landscape, symbolizing the majesty and authority of the forest.
    The river itself was a life-giving force, coursing through the forest like veins, and connecting the many habitats in a cohesive, symbiotic relationship. The abstract hierarchy within this forest was a beautifully arranged symphony filled with diverse players, each contributing their individual melodies to the overall harmony. Its theme was rooted in resilience, perseverance, and the delicate interrelationship between every living inhabitant.
    As the seemingly chaotic landscape extended from the river, it offered a stunning reminder of the ever-present theme, binding all its living creatures through the hierarchy of life and ensuring their survival for generations to come.

    - Modified Story: 
    A canordent grew near the assectur, a haven where nature thrived and the interconnected chain of life flourished. It was a land in which each living being had a place in the perpetual cycle of existence, an intricate balance between the many species found within its depths. Towering dispreinters guarded the landscape, symbolizing the majesty and authority of the canordent.
    The assectur itself was a life-giving force, coursing through the canordent like veins, and connecting the many habitats in a cohesive, symbiotic relationship. The abstract hierarchy within this canordent was a beautifully arranged symphony filled with diverse players, each contributing their individual melodies to the overall harmony. Its theme was rooted in resilience, perseverance, and the delicate interrelationship between every living inhabitant.
    As the seemingly chaotic landscape extended from the assectur, it offered a stunning reminder of the ever-present theme, binding all its living creatures through the hierarchy of life and ensuring their survival for generations to come.
    ==========
    - Story: 
    {story}

    - Modified Story:
    """
    prompt = [
        {"role": "user", "content": prompt}
    ]
    return generate_chat_completion(prompt, temperature=1.1, top_p=0.95)


def QA_generate_questions(sent1, sent2):
    prompt = f"""
    Given the following two sentences, pose a set of questions and answers that relate the two sentences to each other. 
    Here is an example: 

    - Story 1: Adam did not understand the root of the crisis.	
    - Story 2: The child could not reach the top shelf.

    Questions: 
    1. "Adam" in story 1 is analogous to what in story 2?
    2. The relationship between "child" and "top shelf" in story 2 is analogous to to anything in story 2? (If so, what?)
    3. What is the analogous mention of "understand" (story2) in story 1?
    4. Why are "understand" (story1) and "reach" (story2) analogous to each other?
    5. What is the common element between Adam's situation in story 1 and the child's situation in story 2?
    6.  What are the obstacles in each story?
    Answers:
    1. The child
    2. Yes, it is analogous to the relationship between "Adam" and "crisis" 
    3. Reach 
    4. Because they convey actions that require notable amount of difficulty on the side of their executor.   
    5. They both experience difficulty in achieving something.
    6. The root of the crisis for Adam, and the high placement of the top shelf for the child.

    - Story1: {sent1}
    - Story2: {sent2}

    Questions:
    """
    prompt = [
        {"role": "user", "content": prompt}
    ]
    return generate_chat_completion(prompt, temperature=1.1, top_p=0.95)

def QA_generate_answers(story1, story2, questions):
    prompt = f"""
    Answer the following questions based on the given two stories.

    Story1:
    {story1}

    Story 2:
    {story2}

    Questions:
    {questions}
    """
    prompt = [
        {"role": "user", "content": prompt}
    ]
    return generate_chat_completion(prompt, temperature=1.1, top_p=0.95)
