import json
import random
import config
import requests

def generate_chat_completion(messages, model="gpt-4", temperature=1, top_p=1, max_tokens=3000):
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

def sentence_analogy(sentence1, sentence2):
    prompt = f"""
    List the analogous elements between the following 2 sentences:

    E.g.
    Sentence1: The boy is lucky to have the man's lifelong support to win all the soccer games since they hoped it would spread the sport.

    Sentence2: Women are supportive of the girls in their mission to get the dance competition prize since they hoped it would benefit the girls.

    Analogies:
    - Man <-> Woman | Explanation: they're the supporters in both stories
    - Boy <-> Girl | Explanation: they're both being supported in both stories
    - Winning the soccer game <-> Winning the dance competition prize | Explanation: the goal of winning in both stories
    ...

    Sentence1: {sentence1}

    Sentence2: {sentence2}

    Analogies:
    """
    prompt = [
        {"role": "user", "content": prompt}
    ]
    return generate_chat_completion(prompt, temperature=1.6, top_p=0.95)

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

def story_diverse(sentence):
    style = ["Narrative", "Descriptive", "Expository", "Persuasive", "Creative", "Objective", "Subjective", "Review", "Poetry", "Technical"]
    prompt = f"""
    Generate a 7-10 sentence {random.choice(style)} style story with respect to the following sentence:

    Sentence: {sentence}

    """
    prompt = [
        {"role": "user", "content": prompt}
    ]
    return generate_chat_completion(prompt, temperature=1.6, top_p=0.95)

def story_analogy(story1, story2):
    prompt = f"""
    List the analogous elements between the following 2 stories:

    E.g.
    Story1: The boy is lucky to have the man's lifelong support to win all the soccer games since they hoped it would spread the sport.

    Story2: Women are supportive of the girls in their mission to get the dance competition prize since they hoped it would benefit the girls.

    Analogies:
    - Man <-> Woman | Explanation: they're the supporters in both stories
    - Boy <-> Girl | Explanation: they're both being supported in both stories
    - Winning the soccer game <-> Winning the dance competition prize | Explanation: the goal of winning in both stories
    ...

    Story1: The water is flowing fast from a large beaker to a smaller one through a narrow pipe. It was all done in 15 minutes.

    Story2: The parents try to slowly instill bits of knowledge in their child through simple communication. This often takes repetition.

    Analogies:
    - flow <-> instill | Explanation: They're both the action being described.
    - large beaker <-> parent | Explanation: they're both the source of the action.
    - small beaker <-> child | Explanation: they're both the target of the action in both stories
    - water <-> knowledge | Explanation: they're both the object of the action (the content of the flow).
    - narrow pipe <-> communication | Explanation: they're both the means of the action (how the flow happens).
    ...

    Story1: {story1}
    Story2: {story2}

    Analogies:
    """
    prompt = [
        {"role": "user", "content": prompt}
    ]
    return generate_chat_completion(prompt, temperature=1.6, top_p=0.95)

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

def story_names(name_set, story):
    prompt = f"""
    Can you assign human names(like James) to different objects inside of the story? NOTE: You should only use names in the Name Set and use at least 5 names.

    E.g.
    Story:
    A forest grew near the river.
    Output:
    A forest named James grew near the river named Thomas.

    Name Set: {name_set}

    Story: {story}
    """
    prompt = [
        {"role": "user", "content": prompt}
    ]
    return generate_chat_completion(prompt)

def name_analogy(story1, story2):
    prompt = f"""
    Extract all analogous elements in the two given stories in the following format:

    - Name 1 (from Story 1) <-> Name 2 (from Story 2) | Explanation: ...

    Story1: {story1}
    Story2: {story2}
    """
    prompt = [
        {"role": "user", "content": prompt}
    ]
    return generate_chat_completion(prompt)

def name_incorrect():
    #TODO
    pass

def name_evaluation():
    #TODO
    pass