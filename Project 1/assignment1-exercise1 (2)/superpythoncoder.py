import random
import subprocess
from openai import OpenAI
from colorama import init, Fore, Style
from tqdm import tqdm
import black


init(autoreset=True)
PROGRAMS_LIST = [
'''Given two strings str1 and str2, prints all interleavings of the given
    two strings. You may assume that all characters in both strings are
    different. Input: str1 = "AB", str2 = "CD"
    Output:
    ABCD
    ACBD
    ACDB
    CABD
    CADB
    CDAB
    Input: str1 = "AB", str2 = "C"
    Output:
    ABC
    ACB
    CAB''',
"A program that checks if a number is a palindrome",
"A program that finds the kth smallest element in a given binary search tree.",
"A program that merge k Sorted Lists",
"A program that write N-Queens game code"

]


def get_ai_response(question):
    client = OpenAI(
        api_key="put your api key here",
        organization="put your organization id here",
    )

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}],
    )
    return stream.choices[0].message.content


def format_code(code):
    return black.format_str(code, mode=black.FileMode())


def run_code_and_check_errors(code):
    try:
        formatted_code = format_code(code)
        with open("output-superpythoncoder.py", "w") as file:
            file.write(formatted_code)
        with tqdm(total=100, unit="%", desc="\nRunning Code") as progress_bar:
            subprocess.run(["python", "output-superpythoncoder.py"], check=True)
            progress_bar.update(100)
        return None
    except subprocess.CalledProcessError as e:
        return str(e)


# Main execution
user_input = input("Tell me, which program would you like me to code for you? If you don't have an idea, just press enter and I will choose a random program to code: ")

chosen_program = random.choice(PROGRAMS_LIST) if user_input == "" else user_input

MAX_ATTEMPT = 5
attempt = 0
error_message = None

while attempt < MAX_ATTEMPT:
    response = get_ai_response(chosen_program)
    start_marker = "```python\n"
    end_marker = "\n```"
    start_index = response.find(start_marker)
    end_index = response.find(end_marker, start_index)

    if start_index != -1 and end_index != -1:
        start_index += len(start_marker)
        extracted_code = response[start_index:end_index].strip()
        print(extracted_code)

        if extracted_code:
            error_message = run_code_and_check_errors(extracted_code)
            if error_message:
                print(f"{Fore.RED}Error running generated code! Error: {error_message}{Style.RESET_ALL}")
                chosen_program += f"\n\nError encountered: {error_message}\nPlease fix and regenerate the code."
                attempt += 1
            else:
                print(f"{Fore.GREEN}Code run successfully!{Style.RESET_ALL}")
                break

        else:
            print(f"{Fore.RED}No code extracted.{Style.RESET_ALL}")
            break
    else:
        print(f"{Fore.RED}Code block not found in response.{Style.RESET_ALL}")
        break

if attempt == 5:
    print(f"{Fore.RED}Code generation FAILED{Style.RESET_ALL}")



