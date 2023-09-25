import config
import prompts
import generate
import argparse

def parse_args():
    parser=argparse.ArgumentParser(description="analogy tasks")
    parser.add_argument('-t', '--task', type=str, help='the task that you want to do', required=True)
    parser.add_argument('-s1', '--sent1', type=str, help='input1, it could either be sentence or story', required=True)
    parser.add_argument('-s2', '--sent2', type=str, help='input2, it could either be sentence or story', required=True)
    args=parser.parse_args()
    return args

if __name__ == '__main__': 
    args = parse_args()
    task = args.task
    s1 = args.sent1
    s2 = args.sent2
    p = None
    key = config.GPT4KEY["API_KEY"]
    if task == "sentence":
        p = prompts.sentence_analogy(s1, s2)
        correct_out = generate.generate_chat_completion(p, key)
        p = prompts.sentence_incorrect(s1, s2)
        incorrect_out = generate.generate_chat_completion(p, key)
        p, correct_indices = prompts.sentence_evaluation(s1, s2, correct_out, incorrect_out)
        result = generate.generate_chat_completion(p, key)
        print(f"GPT4 prediction: {result}")
        print(f"GPT4 True Value: {correct_indices}")
    if task == "story":
        p = prompts.story_diverse(s1)
        story1 = generate.generate_chat_completion(p, key)
        p = prompts.story_diverse(s2)
        story2 = generate.generate_chat_completion(p, key)
        p = prompts.story_analogy(story1, story2)
        correct_out = generate.generate_chat_completion(p, key)
        p = prompts.story_incorrect(story1, story2)
        incorrect_out = generate.generate_chat_completion(p, key)
        p, correct_indices = prompts.story_evaluation(story1, story2)
        result = generate.generate_chat_completion(p, key)
        print(f"GPT4 prediction: {result}")
        print(f"GPT4 True Value: {correct_indices}")
    if task == "name":
        #TODO: currently no high quality incorrect
        pass
