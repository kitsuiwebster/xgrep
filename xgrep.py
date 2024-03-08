import os
import re
import time
from datetime import timedelta
from termcolor import colored
import random
import string
import math

print("""
                         
 __  ____ _ _ __ ___ _ __
 \ \/ / _` | '__/ _ \ '_ \ 
  >  < (_| | | |  __/ |_) |
 /_/\_\__, |_|  \___| .__/
       __/ |        | |
      |___/         |_|

by @kitsuiwebster
""")

def search_files(directory, keyword, context=100, verbose=True, chunk_size=1024 * 1024 * 8):
    results = []
    start_time = time.time()
    last_update = start_time

    try:
        for root, _, files in os.walk(directory):
            if verbose:
                print(f'🔍 Searching in directory: {root}')
            for file in files:
                if file.startswith('xgrep-'): 
                    continue
                if file.endswith(('.txt', '.sql', '.json', '.csv', '.html', 'log', '.php', '.pl', '.css', '.py', '.js', '.ts',
                                  '.cgi', '.xml', 'jsx', '.cfm')):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    if verbose:
                        print(f'👉 {file_path}')
                    if file_size > 5 * 1024 * 1024 * 1024: 
                        print(f'⚠️  This file is large {math.ceil(file_size / (1024 * 1024 * 1024))} GB.')
                        print('⚠️  It can take a moment to be scanned. Be patient amigo.')
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        data = ""
                        keyword_len = len(keyword)

                        while True:
                            chunk = f.read(chunk_size)
                            data += chunk

                            if len(chunk) < chunk_size:
                                matches = re.finditer(keyword, data, re.IGNORECASE)

                                for match in matches:
                                    start, end = match.span()

                                    left_context = max(0, start - context)
                                    right_context = min(len(data), end + context + 1)

                                    context_text = data[left_context:right_context]
                                    keyword_match = colored(data[start:end], 'green')
                                    result = {
                                        'file': file_path,
                                        'match': f"{context_text[:start - left_context]}{keyword_match}{context_text[end - left_context:]}",
                                        'start': start + left_context,
                                        'end': end + left_context,
                                    }
                                    results.append(result)
                                    found_element = colored("Found one element", "green")
                                    print(f"✅ {found_element}")

                                break

                            else:
                                matches = re.finditer(keyword, data[:-keyword_len + 1], re.IGNORECASE)

                                for match in matches:
                                    start, end = match.span()

                                    left_context = max(0, start - context)
                                    right_context = min(len(data), end + context + 1)

                                    context_text = data[left_context:right_context]
                                    keyword_match = colored(data[start:end], 'green')
                                    result = {
                                        'file': file_path,
                                        'match': f"{context_text[:start - left_context]}{keyword_match}{context_text[end - left_context:]}",
                                        'start': start + left_context,
                                        'end': end + left_context,
                                    }
                                    results.append(result)
                                    found_element = colored("Found one element", "green")
                                    print(f"✅ {found_element}")

                                data = data[-keyword_len + 1:]

                    current_time = time.time()
                    elapsed_time = current_time - start_time
                    if elapsed_time >= 10 and current_time - last_update >= 10:
                        elapsed_time_formatted = str(timedelta(seconds=elapsed_time))
                        print(f"⏰ Time elapsed: {elapsed_time_formatted}")
                        last_update = current_time

    except PermissionError as e:
        print(f"⛔ Error: {e}")
    except FileNotFoundError as e:
        print(f"⛔ Error: {e}")
    except Exception as e:
        print(f"⛔ Unexpected error: {e}")

    total_time = time.time() - start_time
    total_time_formatted = str(timedelta(seconds=total_time))
    print("\n✅ Search completed!")
    print(f"⏰ Total time: {total_time_formatted}")

    return results




if __name__ == '__main__':
    current_directory = os.path.abspath(os.curdir)
    keyword = input('👉 Enter the keyword to search for: ')

    context_input = input(f'👉 Enter the number of characters around the keyword (press Enter for default: {100}): ')
    context = 100 if context_input == '' else int(context_input)

    chunk_size_options = [1024 * x for x in [8, 1024, 262144, 1048576, 2097152]]
    print('👉 Enter the chunk size\n')
    print('👉 Options:')
    for i, size in enumerate(chunk_size_options):
        print(f'   Press {i} for  {size // 1024} x 1024')
    print('\n👉 Press Enter for default (8 x 1024): \n')

    chunk_size_input = input('👉 Your choice: ')
    chunk_size = 1024 if chunk_size_input == '' else chunk_size_options[int(chunk_size_input)]

    if chunk_size_input.isdigit() and int(chunk_size_input) in range(len(chunk_size_options)):
        chunk_size = chunk_size_options[int(chunk_size_input)]

    results = search_files(current_directory, keyword, context, True, chunk_size)

    print(f'\n👉 Results for keyword "{keyword}":')
    directory = os.path.basename(os.path.abspath(os.curdir))
    with open(f'xgrep-{keyword}-{directory}-{"".join(random.choices(string.digits, k=10))}.txt', 'w') as f:
        for result in results:
            print(f'👉 File: {result["file"]}')
            print(f'👉 Match (surrounded by {context} characters of context):')
            print(result['match'])
            print()

            f.write(f'File: {result["file"]}\n')
            f.write(f'Match (surrounded by {context} characters of context):\n')
            f.write(f'{result["match"]}\n\n')
