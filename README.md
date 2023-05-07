![Mindfeeder 2 Logo](https://mindfeederllc.com/mindfeeder2.png)

# Mindfeeder-2 OpenAI (Instruction Input Output) Generator

This program is designed to generate new instruction, input, and output (IIO) pairs using OpenAI's GPT-3.5-turbo (Or any specified model). Given an input dataset containing IIO pairs, the script will generate new variations for each pair using the provided API key.

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
python mindfeeder2-open-ai-gen.py --apikey API_KEY --model MODEL_NAME --input INPUT_FILE --output OUTPUT_FILE --num_instructions NUM_INSTRUCTIONS --start_index START_INDEX --max_workers MAX_WORKERS --prompt_input PROMPT_INPUT --filter FILTER_RESULTS
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
    "instruction": "What is \"viewable CPM\" in relation to Display ads?",
    "input": "\"Viewable CPM\" refers to how much it costs for 1000 impressions of your ad. While many different bidding strategies are available for Display ads, it is important to remember that certain domains will command different rates for real estate on their sites. SEMrush found that the average rate was $2.80, so experimenting around that rate may be beneficial.",
    "output": "\"Viewable CPM\" refers to how much it costs for 1000 impressions of your ad."
  }
]
```

# Output Data Format

The generated data will be saved in the specified output file in JSON format, similar to the input data format.

# Frequently Asked Questions (FAQs)

### What is the purpose of this script?

This script is designed to generate instruction, input and output pairs based on a given instruction, input and output JSON using OpenAI's GPT-3.5-turbo model. It's useful for creating datasets for AI training and testing purposes, as well as generating question, context and answer pairs for various applications.

### Can I use other OpenAI models with this script?

Yes, you can use other OpenAI models by changing the ```--model``` command line argument. However, the script has been optimized for the GPT-3.5-turbo model, and using other models may produce unexpected results. However, all chat completetion models are supposed below:


```--model gpt-3.5-turbo``` (8,192 max tokens)

```--model gpt-4``` (8,192 max tokens)

```--model gpt-4-32k``` (32,768 max tokens)


### What does the --filter command line argument do?

The ```--filter``` argument enables or disables the filtering of generated instruction and output pairs based on certain keywords. By default, this is set to true, meaning that pairs containing specified keywords or phrases will be excluded from the output. Set this argument to false if you want to include all generated pairs, regardless of their content.


### How can I improve the quality of the generated instruction and output pairs?

You can try adjusting the ```--prompt_input``` command line argument to provide additional context or guidance for the model. This may help in generating more relevant and accurate instruction and output pairs. See the sample below:

```
python mindfeeder1-open-ai-gen.py --apikey=your_api_key --input=input.txt --prompt_input "Be very detailed with your responses and use bullet points in necessary to organize the outputs."
```

### How can I obtain an API key for OpenAI?

To obtain an API key, you will need to sign up for an OpenAI account. Visit the OpenAI API Pricing page for more information on available plans and pricing.


### What is --max_workers and its recommended settings?

Depending on how quickly / acuritly you want the output from this scrip to be. You will set accordinly. Higher settings yeild quicker results. Lower setting yield higher quality results.

```--max_workers 12``` = Optimal Performance wirhout errors

```--max_workers 20``` = Optimal Speed & Performance wirhout errors

```--max_workers 30``` = Optimal Speed Performance with minimal errors

#### What is --max_workers and its recommended settings?

The key to this setting is to keep in mind the length of your responses from openai and they will stay under token length

```--num_instructions 5``` = Optimal Performance wirhout errors

#### What is --prompt_input and its recommended settings?

Used to inject a specified prompt right before the main insrruction to openai

```--prompt_input "Be as detailed as possible in your responses and use bullet points if needed to organize material."```


# Credits
Developed by Kyle Altenderfer ```altenderfer@gmail.com```



## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

## Donate

Venmo ```@altenderfer```
