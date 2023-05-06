# Mindfeeder-2 OpenAI Generator

This program is designed to generate new instruction, input, and output (IIO) pairs using OpenAI's GPT-3.5-turbo. Given an input dataset containing IIO pairs, the script will generate new variations for each pair using the provided API key.

## Requirements

- Python 3.6 or higher
- `openai` Python package

To install the `openai` package, run the following command:

```bash
pip install openai
```

# Usage

To use this program, run the following command:

```bash
python generator.py --apikey API_KEY --model MODEL_NAME --input INPUT_FILE --output OUTPUT_FILE --num_instructions NUM_INSTRUCTIONS --start_index START_INDEX --max_workers MAX_WORKERS --prompt_input PROMPT_INPUT --filter FILTER_RESULTS
```

Replace the placeholders with the appropriate values:
```
API_KEY: Your OpenAI API key.
MODEL_NAME: The name of the OpenAI model to use (default: "gpt-3.5-turbo").
INPUT_FILE: The path to the JSON file containing the input data.
OUTPUT_FILE: The path to the JSON file where the generated data will be saved.
NUM_INSTRUCTIONS: The number of new variations to generate for each IIO pair (default: 5).
START_INDEX: The index in the input data to start processing from (default: 0).
MAX_WORKERS: The maximum number of worker threads to use for processing (default: 3).
PROMPT_INPUT: An optional string to add at the beginning of the prompt.
FILTER_RESULTS: Whether to filter results based on certain phrases (default: True).
```

# Input Data Format

The input data should be in JSON format, with each element containing an "instruction", "input", and "output" field. For example:

```
[
  {
    "instruction": "What is the capital of France?",
    "input": "France is a country in Western Europe with a rich history and diverse culture.",
    "output": "The capital of France is Paris."
  }
]
```

# Output Data Format

The generated data will be saved in the specified output file in JSON format, similar to the input data format.

# Credits
Developed by Kyle Altenderfer ```altenderfer@gmail.com```



## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

## Donate

Venmo ```@altenderfer```
