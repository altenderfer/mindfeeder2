import argparse
import json
import openai
import sys
import re
import time
import concurrent.futures
import traceback
import threading

def animate_connection():
    chars = "|/-\\"
    while True:
        for char in chars:
            sys.stdout.write(f"\r{char} Connected to OpenAI {char}")
            sys.stdout.flush()
            time.sleep(0.1)

def connect_to_openai(api_key):
    openai.api_key = api_key

    t = threading.Thread(target=animate_connection, daemon=True)
    t.start()

    time.sleep(5)  # You can adjust the sleep time as needed

def load_input_data(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    return data

def generate_new_iio_pairs(instruction, input, output, model, num_instructions, prompt_input):
    prompt = f"{prompt_input}. Per set of instructions, inputs, and output pairs there can only be 1 instruction, 1 input, and 1 output. Instruction will always be questions or statements that command an answer, Input will always provide context based on the input or output and context below, and output will always provide the full detailed answer. Based on the text below, generate {num_instructions} more variations based on the original content of \"Instruction\" \"Context\" and \"Output\" in the format 'I:' for instruction (always a questions or a command to do something), 'i:' for context (which should be long and detailed and always provide context for input and output), and 'O:' for output (which will provide the full detailed answer).\n\nInstruction: {instruction}\nContext: {input}\nOutput: {output}"

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )

    content = response['choices'][0]['message']['content']
    content += "\n"
    print(f"\n{content}\n")

    io_pairs = parse_io(content)
    io_pairs_with_input = []
    for pair in io_pairs:
        ordered_pair = {"instruction": pair["instruction"], "input": pair["context"], "output": pair["output"]}
        io_pairs_with_input.append(ordered_pair)
    return io_pairs_with_input

def parse_io(content, filter_results=True):
    # Use regex to extract instruction, context, and output pairs
    regex_pattern = r"I:((?:(?!I:|i:|O:).)*)(?:\ni:((?:(?!I:|i:|O:).)*))?(?:\nO:((?:(?!I:|i:|O:).)*))?(?:\n\n|$)"
    matches = re.findall(regex_pattern, content, re.DOTALL)

    io_pairs = []
    keywords_phrases = [
        "the text",
        "is not specified",
        "is not mentioned",
        "does not mention",
        "does not provide",
        "does not indicate",
        "cannot provide",
        "is not stated",
        "is not provided",
        "without further",
        "are not provided",
        "i'm sorry,",
        "the article did not",
        "no information was provided",
    ]

    for match in matches:
        instruction = match[0].strip()
        context = match[1].strip()
        output = match[2].strip()

        if filter_results:
            if any(keyword.lower() in instruction.lower() or keyword.lower() in output.lower() for keyword in keywords_phrases):
                continue

        if instruction and context and output:
            io_pairs.append({"instruction": instruction, "context": context, "output": output})

    return io_pairs

def process_input_data(input_data, model, output_file, num_instructions, start_index, max_workers=5, timeout=300, prompt_input="", filter_results=True):
    def save_to_file(new_dataset):
        with open(output_file, 'w') as f:
            json.dump(new_dataset, f, indent=2, sort_keys=False)

    new_dataset = []

    total_items = len(input_data)
    start_time = time.time()

    save_interval = 10  # Save every 10 items

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {executor.submit(generate_new_iio_pairs, item['instruction'], item['input'], item['output'], model, num_instructions, prompt_input): index for index, item in enumerate(input_data[start_index:], start_index + 1)}

        for future in concurrent.futures.as_completed(future_to_index):
            index = future_to_index[future]
            try:
                new_io_pairs = future.result()
                new_dataset.extend(new_io_pairs)
            except Exception as e:
                print(f"\nError processing item {index}: {e}")
                traceback.print_exc()
                continue

            # Calculate the percentage of completion and elapsed time
            percentage_complete = (index / total_items) * 100
            elapsed_time = time.time() - start_time

            # Calculate the estimated time remaining
            time_remaining = (elapsed_time / index) * (total_items - index)
            hours, rem = divmod(time_remaining, 3600)
            minutes, seconds = divmod(rem, 60)

            # Create a progress bar
            progress_bar_length = 50
            progress = int(progress_bar_length * (index / total_items))
            progress_bar = f"[{'#' * progress}{'-' * (progress_bar_length - progress)}]"

            print(f"\n\rItem {index} of {total_items} processed - {percentage_complete:.2f}% complete - ETA: {int(hours):02}:{int(minutes):02}:{int(seconds):02} {progress_bar}", end="\n")

            # Save to file every save_interval items
            if index % save_interval == 0:
                save_to_file(new_dataset)

    # Save final output
    save_to_file(new_dataset)
    print(f"Processing completed. Results saved to {output_file}")

def main(api_key, model, input_file, output_file, num_instructions, start_index, max_workers, prompt_input, filter_results):
    connect_to_openai(api_key)

    input_data = load_input_data(input_file)
    process_input_data(input_data, model, output_file, num_instructions, start_index, max_workers, prompt_input=prompt_input, filter_results=filter_results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apikey", default="your_api_key")
    parser.add_argument("--model", default="gpt-3.5-turbo")
    parser.add_argument("--input", default="input.json")
    parser.add_argument("--output", default="output.json")
    parser.add_argument("--num_instructions", default=5, type=int)
    parser.add_argument("--start_index", default=0, type=int)
    parser.add_argument("--max_workers", default=3, type=int)
    parser.add_argument("--prompt_input", default="", type=str)
    parser.add_argument("--filter", default=True, type=lambda x: (str(x).lower() == 'true'))

    args = parser.parse_args()

    main(
        api_key=args.apikey,
        model=args.model,
        input_file=args.input,
        output_file=args.output,
        num_instructions=args.num_instructions,
        start_index=args.start_index,
        max_workers=args.max_workers,
        prompt_input=args.prompt_input,
        filter_results=args.filter,
    )
