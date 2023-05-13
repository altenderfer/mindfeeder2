import argparse
import json
import openai
import sys
import re
import time
import concurrent.futures
import traceback
import threading
import tkinter as tk
from tkinter import ttk, filedialog
import asyncio
import aiohttp

stop_flag = [False]

def animate_connection():
    chars = "|/-\\"
    while True:
        for char in chars:
            sys.stdout.write(f"\r{char} Connected to OpenAI {char}")
            sys.stdout.flush()
            time.sleep(0.1)

def connect_to_openai(api_key, api_base):
    openai.api_key = api_key
    openai.api_base = api_base

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

def process_input_data(input_data, model, output_file, num_instructions, start_index, max_workers=5, timeout=300, prompt_input="", filter_results=True, stop_flag=None):
    def save_to_file(new_dataset):
        with open(output_file, 'w') as f:
            json.dump(new_dataset, f, indent=2, sort_keys=False)

    new_dataset = []

    total_items = len(input_data)
    start_time = time.time()

    save_interval = 10  # Save every 10 items

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {executor.submit(generate_new_iio_pairs, item['instruction'], item['input'], item['output'], model, num_instructions, prompt_input): index for index, item in enumerate(input_data[start_index:], start_index + 1)}

        try:
            for future in concurrent.futures.as_completed(future_to_index):
                if stop_flag and stop_flag[0]:
                    print("\nStopping the script...")
                    raise RuntimeError("Script stopped by the user")

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

        except RuntimeError as e:
            if str(e) == "Script stopped by the user":
                executor.shutdown(wait=False, cancel_futures=True)  # Forcefully shutdown the executor
            else:
                raise

    # Save final output if not stopped
    if not (stop_flag and stop_flag[0]):
        save_to_file(new_dataset)
        print(f"Processing completed. Results saved to {output_file}")



def stop_and_close():
    global stop_flag
    stop_flag[0] = True
    root.destroy()


def browse_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)


def browse_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)


async def main_async(api_key, api_base, model, input_file, output_file, num_instructions, start_index, max_workers, prompt_input=False, filter_results=False, stop_flag=None):
    connect_to_openai(api_key, api_base)

    input_data = load_input_data(input_file)
    process_input_data(input_data, model, output_file, num_instructions, start_index, max_workers, prompt_input=prompt_input, filter_results=filter_results, stop_flag=stop_flag)


def main(stop_flag):
    api_key = apikey_entry.get()
    api_base = api_base_entry.get()
    model = model_var.get()
    input_file = input_entry.get()
    output_file = output_entry.get()
    num_instructions = int(num_instructions_entry.get())
    start_index = int(start_index_entry.get())
    max_workers = int(max_workers_entry.get())
    prompt_input = prompt_input_entry.get()
    filter_results = filter_var.get()

    asyncio.run(main_async(api_key, api_base, model, input_file, output_file, num_instructions, start_index, max_workers, prompt_input, filter_results, stop_flag=stop_flag))

def main_thread():
    global stop_flag
    try:
        main(stop_flag)
    except Exception as e:
        if stop_flag[0]:
            print("\nScript stopped by the user.")
        else:
            print(f"\nError occurred: {e}")
            traceback.print_exc()
    finally:
        root.after(1000, root.destroy)  # Schedule the application to close after 1 second (1000ms)


# GUI code
root = tk.Tk()
root.title("Mindfeeder2 OpenAI Gen GUI")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# API Key
apikey_label = ttk.Label(frame, text="API Key:")
apikey_label.grid(column=0, row=0, sticky=tk.W)
apikey_entry = ttk.Entry(frame, width=30)
apikey_entry.grid(column=1, row=0, sticky=tk.W)

# API Base URL
api_base_label = ttk.Label(frame, text="API Base URL:")
api_base_label.grid(column=0, row=1, sticky=tk.W)
api_base_entry = ttk.Entry(frame, width=30)
api_base_entry.grid(column=1, row=1, sticky=tk.W)
api_base_entry.insert(0, "https://api.openai.com/v1") # Default value


# Model
model_label = ttk.Label(frame, text="Model:")
model_label.grid(column=0, row=2, sticky=tk.W)
model_var = tk.StringVar()
model_var.set("gpt-3.5-turbo")
model_dropdown = ttk.OptionMenu(frame, model_var, "gpt-3.5-turbo", "gpt-3.5-turbo", "gpt-4", "gpt-4-32k")
model_dropdown.grid(column=1, row=2, sticky=tk.W)

# Input File
input_label = ttk.Label(frame, text="Input File:")
input_label.grid(column=0, row=3, sticky=tk.W)
input_entry = ttk.Entry(frame, width=30)
input_entry.grid(column=1, row=3, sticky=tk.W)
input_browse = ttk.Button(frame, text="Browse", command=browse_input_file)
input_browse.grid(column=2, row=3, sticky=tk.W)

# Output File
output_label = ttk.Label(frame, text="Output File:")
output_label.grid(column=0, row=4, sticky=tk.W)
output_entry = ttk.Entry(frame, width=30)
output_entry.grid(column=1, row=4, sticky=tk.W)
output_browse = ttk.Button(frame, text="Browse", command=browse_output_file)
output_browse.grid(column=2, row=4, sticky=tk.W)

# Num Instructions
num_instructions_label = ttk.Label(frame, text="Num Instructions:")
num_instructions_label.grid(column=0, row=5, sticky=tk.W)
num_instructions_entry = ttk.Spinbox(frame, from_=1, to=100, width=5)
num_instructions_entry.grid(column=1, row=5, sticky=tk.W)
num_instructions_entry.delete(0, tk.END)
num_instructions_entry.insert(0, "6")

# Start Index
start_index_label = ttk.Label(frame, text="Start Index:")
start_index_label.grid(column=0, row=6, sticky=tk.W)
start_index_entry = ttk.Spinbox(frame, from_=0, to=10000, width=5)
start_index_entry.grid(column=1, row=6, sticky=tk.W)
start_index_entry.delete(0, tk.END)
start_index_entry.insert(0, "0")

# Max Workers
max_workers_label = ttk.Label(frame, text="Max Workers:")
max_workers_label.grid(column=0, row=7, sticky=tk.W)
max_workers_entry = ttk.Spinbox(frame, from_=1, to=100, width=5)
max_workers_entry.grid(column=1, row=7, sticky=tk.W)
max_workers_entry.delete(0, tk.END)
max_workers_entry.insert(0, "3")

# Prompt Input
prompt_input_label = ttk.Label(frame, text="Prompt Input:")
prompt_input_label.grid(column=0, row=8, sticky=tk.W)
prompt_input_entry = ttk.Entry(frame, width=30)
prompt_input_entry.grid(column=1, row=8, sticky=tk.W)

# Filter
filter_label = ttk.Label(frame, text="Filter:")
filter_label.grid(column=0, row=9, sticky=tk.W)
filter_var = tk.StringVar()
filter_var.set("True")
filter_dropdown = ttk.OptionMenu(frame, filter_var, "True", "True", "False")
filter_dropdown.grid(column=1, row=9, sticky=tk.W)

# Run Button
run_button = ttk.Button(frame, text="Run", command=lambda: threading.Thread(target=main_thread, daemon=True).start())
run_button.grid(column=1, row=10, pady=10)

# Stop Button
stop_button = ttk.Button(frame, text="Stop & wait until workers finish", command=stop_and_close)
stop_button.grid(column=2, row=10, pady=10)

root.mainloop()
