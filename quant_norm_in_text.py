from quant_norm import QuantNorm
from quant_norm import Normalization_dict
import sys
import pandas as pd
import argparse
import json

def Normalize_Text(text_string, currency_update = {}):
    if isinstance(text_string,str):
        words = text_string.split()
        new_text_string = ''
        skip_next = False

        for i in range(len(words)):
            if skip_next:
                skip_next = False
                continue
            if i < len(words) - 1:           
                first = words[i]
                second = words[i+1]
                try:
                    normalized = QuantNorm(first,second, currency_update)
                    new_text_string = f"{new_text_string} {normalized} "
                    skip_next = True
                except:
                    new_text_string += f"{first} "
            else:
                new_text_string += f"{words[i]}"

        return new_text_string.strip()

#Initialize argument parser
parser = argparse.ArgumentParser(description = "normalize inputs from a text or file")
parser.add_argument("-t", "--text", help = "input text to normalize")
parser.add_argument("-i", "--input_filename", help = "input file with text to be noramlized")
parser.add_argument("-o", "--output_filename", help = "output filename with noramlized text")
parser.add_argument("-m", "--max_lines",type = int, help = "max number of lines in input to be processed")
parser.add_argument("-c", "--currency", type =str, help = "currency in json format")
args = parser.parse_args()

normalized_lines = []

#Load the currency values if present, otherwise it will be empty
if args.currency:
    currency_update = json.loads(args.currency)
else: 
    currency_update = {}

#If -t command, read the text and normalize the line
if args.text:
    new_text = Normalize_Text(args.text, currency_update)
    normalized_lines.append(new_text)

#If there is an input file present, read and normalize the lines, append to the normalized list
elif input_file := args.input_filename:
    #If there is a max number of lines to process
    if max_lines := args.max_lines:
        i = 0
        with open(input_file,'r') as file:
            for line in file:
                if i < max_lines:
                    norm_line = Normalize_Text(line, currency_update)
                    normalized_lines.append(norm_line)
    #If no max lines are specified, read the whole file
    else:
        with open(input_file,'r') as file:
            for line in file:
                norm_line = Normalize_Text(line, currency_update)
                normalized_lines.append(norm_line)

if output_file := args.output_filename:
    with open(output_file,'a') as file:
        for line in normalized_lines:
            file.write(line)
else:
    for line in normalized_lines:
        print(line)








