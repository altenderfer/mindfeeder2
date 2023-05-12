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

## Command Line

To use this program, run the following command:

```bash
python mindfeeder2-open-ai-gen.py --apikey API_KEY --input INPUT_FILE --output OUTPUT_FILE --num_instructions 9 --max_workers 12 --prompt_input "Be very detailed with your responses and use bullet points as necessary to organize the material."
```

The script accepts the following command line arguments:
```
--api_key: Your OpenAI API key.
--api_base: Used to change the default openai endpoint, defaults to openai
--model: The name of the OpenAI model to use (default: "gpt-3.5-turbo").
--input: The path to the JSON file containing the input data.
--output: The path to the JSON file where the generated data will be saved.
--num_instructions: The number of new variations to generate for each IIO pair (default: 5).
--start_index: The index in the input data to start processing from (default: 0).
--max_workers: The maximum number of worker threads to use for processing (default: 3).
--prompt_input: An optional string to add at the beginning of the prompt.
--filter: Whether to filter results based on certain phrases (default: True).
```

## GUI

To use the GUI version of the script, run the following command:


```bash
python mindfeeder2-open-ai-gen-gui.py
```

This will open a window where you can input the required information:

- API Key - Your OpenAI API key.
- Model - The OpenAI language model you want to use (default is gpt-3.5-turbo).
- Input File - The path to the JSON file containing the IIO pairs to generate new variations for.
- Output File - The path to the JSON file where the new IIO pairs will be saved.
- Num Instructions - The number of new variations to generate for each input/output pair.
- Start Index - The index of the IIO pair to start generating new variations from.
- Max Workers - The maximum number of workers to use for parallel processing.
- Prompt Input - The prompt to use for generating new variations (optional).
- Filter - Whether to filter out generated variations that do not contain enough information (default is True).

Once you have filled in the required information, click the "Run" button to start generating new instruction/input/output pairs. You can stop the generation process at any time by clicking the "Stop & Wait Until Workers Finish" button.



# Input Data Format

The input data should be in JSON format, with each element containing an "instruction", "input", and "output" field. For example:

```
[
  {
    "instruction": "What kind of YouTube campaign is ideal for Max Conversion or Target CPA?",
    "input": "Max Conversion or Target CPA are bidding strategies that can be leveraged for TrueView for action or conversion-oriented YouTube campaigns. However, you will not be able to select this campaign type unless you have already configured conversion in your account.",
    "output": "Max Conversion or Target CPA are ideal for TrueView for action or conversion-oriented YouTube campaigns, but can only be selected if you have already configured conversion in your account."
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
python mindfeeder2-open-ai-gen.py --apikey=your_api_key --input=input.txt --prompt_input "Be very detailed with your responses and use bullet points as necessary to organize the material."
```

### How can I obtain an API key for OpenAI?

To obtain an API key, you will need to sign up for an OpenAI account. Visit the OpenAI API Pricing page for more information on available plans and pricing.


### What is --max_workers and its recommended settings?

Depending on how quickly / acuritly you want the output from this scrip to be. You will set accordinly. Higher settings yeild quicker results. Lower setting yield higher quality results.

```--max_workers 12``` = Optimal Performance wirhout errors

```--max_workers 20``` = Optimal Speed & Performance wirhout errors

```--max_workers 30``` = Optimal Speed Performance with minimal errors

#### What is --num_instructions and its recommended settings?

The key to this setting is to keep in mind the length of your responses from openai and they will stay under token length

```--num_instructions 5``` = Optimal Performance wirhout errors

#### What is --prompt_input and its recommended settings?

Used to inject a specified prompt right before the main insrruction to openai

```--prompt_input "Be as detailed as possible in your responses and use bullet points if needed to organize material."```


# Credits
Developed by Kyle Altenderfer ```altenderfer@gmail.com```



## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

