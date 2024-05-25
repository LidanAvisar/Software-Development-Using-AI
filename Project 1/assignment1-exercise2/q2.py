import csv
import time
from gpt4all import GPT4All
import wolframalpha
import redis
import matplotlib.pyplot as plt


# Initialize the models
model1 = GPT4All("orca-mini-3b-gguf2-q4_0.gguf", "/Users/lydnbysr/Library/Application Support/nomic.ai/GPT4All/")
model1.name = "orca-mini-3b-gguf2-q4_0.gguf"

model2 = GPT4All("gpt4all-falcon-q4_0.gguf",
                 "/Users/lydnbysr/Library/Application Support/nomic.ai/GPT4All/")
model2.name = "gpt4all-falcon-q4_0.gguf"

model3 = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf", "/Users/lydnbysr/Library/Application Support/nomic.ai/GPT4All/")
model3.name = "mistral-7b-instruct-v0.1.Q4_0.gguf"

# Initialize the Wolfram Alpha client
app_id = 'AAR872-9PUX772XAQ'
wolfram_client = wolframalpha.Client(app_id)


def load_questions(filename):
    questions = []
    with open(filename, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            questions.append(row['Question'])
    return questions


def get_answer_from_model(question, model):
    start_time = time.time()
    answer = model.generate(question)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    return answer, time_taken


def fetch_wolfram_alpha_answer(question):
    # Check if the answer is in Redis cache
    cache_key = f"wolfram_{question}"
    cached_answer = redis_client.get(cache_key)

    if cached_answer:
        return cached_answer.decode('utf-8')  # Decoding from bytes to string

    try:
        res = wolfram_client.query(question)
        answer = next(res.results).text

        # Cache the answer
        redis_client.setex(cache_key, 14400, answer)
        return answer
    except StopIteration:
        redis_client.setex(cache_key, 14400, "")
        return None


def evaluate_correctness(question, answer_to_evaluate):
    wolfram_alphas_answer = fetch_wolfram_alpha_answer(question)
    if wolfram_alphas_answer is None:
        return None

    prompt = (f"I am going to present two different answers to the same question. "
              f"Please assess how similar these two answers are on a scale from 0 to 1.0, "
              f"where 0 means completely different and 1.0 means exactly the same. "
              f"Do not solve the question itself. "
              f"\n\nQuestion: {question}"
              f"\n\nAnswer 1 (Wolfram Alpha's Answer): {wolfram_alphas_answer}"
              f"\nAnswer 2: {answer_to_evaluate}"
              f"\n\nSimilarity Score (0.0-1.0):")

    response = model3.generate(prompt)

    # Extracting numerical value from the response
    similarity_score = 0
    for word in response.split():
        try:
            similarity_score = float(word)
            break
        except ValueError:
            continue

    correctness_score = similarity_score
    return correctness_score


redis_client = redis.Redis(host='localhost', port=6379, db=0)


def generate_bar_chart(model_names, avg_ratings, save_path):
    plt.figure(figsize=(10, 6))
    plt.bar(model_names, avg_ratings, color=['blue', 'green'])
    plt.xlabel('Model')
    plt.ylabel('Average Correctness Score')
    plt.title('Average Correctness Score per Model')
    plt.savefig(save_path)
    plt.close()


def main():
    general_questions = load_questions('/Users/lydnbysr/Desktop/pythonProj/HW1/General_Knowledge_Questions.csv')
    harder_questions = load_questions('/Users/lydnbysr/Desktop/pythonProj/HW1/Harder_Questions.csv')

    number_of_general_questions_answered = 0
    number_of_harder_questions_answered = 0

    models = [model1, model2]
    results = []

    # Initializing variables for calculating averages and finding lowest-rated answers
    total_ratings = {model.name: 0 for model in models}
    count_ratings = {model.name: 0 for model in models}
    lowest_rating = {model.name: float('inf') for model in models}
    lowest_rated_answer = {model.name: ("", "") for model in models}  # (question, answer)

    for question in harder_questions:
        wolfram_answer = fetch_wolfram_alpha_answer(question)
        if wolfram_answer is None:
            continue
        number_of_harder_questions_answered += 1

    for question in general_questions:
        wolfram_answer = fetch_wolfram_alpha_answer(question)
        if wolfram_answer is None:
            continue
        number_of_general_questions_answered += 1

        for model in models:
            answer, time_taken = get_answer_from_model(question, model)
            correctness = evaluate_correctness(question, answer)
            correctness_display = '{:.2f}'.format(correctness) if correctness is not None else 'N/A'

            # Update ratings calculations
            if correctness is not None:
                total_ratings[model.name] += correctness
                count_ratings[model.name] += 1
                if correctness < lowest_rating[model.name]:
                    lowest_rating[model.name] = correctness
                    lowest_rated_answer[model.name] = (question, answer)

            results.append({
                "Question": question,
                "Model": model.name,
                "Answer": answer,
                "Time (ms)": int(time_taken),
                "Correctness": correctness_display
            })

    # Write results to a CSV file
    with open('/Users/lydnbysr/Desktop/pythonProj/HW1/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Question", "Model", "Answer", "Time (ms)", "Correctness"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

    percent_general = (number_of_general_questions_answered / len(general_questions)) * 100
    percent_harder = (number_of_harder_questions_answered / len(harder_questions)) * 100

    print(f"\nNumber of questions answered from General Knowledge file: {number_of_general_questions_answered}")
    print(f"\nNumber of questions answered from Harder Questions file: {number_of_harder_questions_answered}")

    print(f"\nPercentage of General Knowledge questions solved: {percent_general:.2f}%")
    print(f"\nPercentage of Harder Questions solved: {percent_harder:.2f}%\n")

    for model in models:
        avg_rating = total_ratings[model.name] / count_ratings[model.name] if count_ratings[model.name] > 0 else 0
        print(f"Average answer rating of {model.name}: {avg_rating:.2f}")
        lowest_q, lowest_a = lowest_rated_answer[model.name]
        print(f"Lowest rating question and answer of {model.name}: {lowest_q}\n{lowest_a}")

    model_names = [model.name for model in models]
    avg_ratings = [total_ratings[model.name] / count_ratings[model.name] if count_ratings[model.name] > 0 else 0 for model in models]
    generate_bar_chart(model_names, avg_ratings, '/Users/lydnbysr/Desktop/pythonProj/HW1/average_correctness_chart.png')


if __name__ == "__main__":
    main()
