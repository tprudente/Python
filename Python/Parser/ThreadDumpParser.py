import re
import os
import csv


def parse_thread_dump(file_content):
    thread_pattern = r'^"(.+)"\s'
    state_pattern = r'\s+java.lang.Thread.State:\s+(\w+)'
    stack_trace_pattern = r'\s+at\s+(.+)'

    threads = []
    current_thread = {}

    lines = file_content.splitlines()
    for i, line in enumerate(lines):
        thread_match = re.match(thread_pattern, line)
        if thread_match:
            if current_thread:
                threads.append(current_thread)
            current_thread = {
                'name': thread_match.group(1),
                'state': None,
                'stack_trace': None
            }

        state_match = re.match(state_pattern, line)
        if state_match and current_thread:
            current_thread['state'] = state_match.group(1)

        if current_thread and current_thread['stack_trace'] is None:
            stack_trace_match = re.match(stack_trace_pattern, line)
            if stack_trace_match:
                current_thread['stack_trace'] = stack_trace_match.group(1)

    if current_thread:
        threads.append(current_thread)

    return threads


def extract_thread_type_and_timestamp(filename):
    # Extract thread type and timestamp based on the format of the filename
    thread_type = filename.split('-')[-1].split('_')[0]  # After last dash and before underscore
    timestamp = filename.split('_')[-1]  # After underscore
    return thread_type, timestamp


def analyze_thread_dumps(directory_path):
    results = []
    for filename in os.listdir(directory_path):
        with open(os.path.join(directory_path, filename), 'r') as file:
            file_content = file.read()
            threads = parse_thread_dump(file_content)

            # Extract thread type and timestamp
            thread_type, timestamp = extract_thread_type_and_timestamp(filename)

            results.append({
                'file': filename,
                'timestamp': timestamp,
                'thread_type': thread_type,
                'threads': threads
            })
    return results


def export_to_csv(results, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';')
        csv_writer.writerow(['Timestamp', 'Thread Type', 'File', 'Thread Name', 'State', 'Stack Trace'])

        for result in results:
            for thread in result['threads']:
                stack_trace = thread['stack_trace'] if thread['stack_trace'] else ""
                csv_writer.writerow([
                    result['timestamp'],  # Timestamp column
                    result['thread_type'],  # Thread Type column
                    result['file'],  # Original file name
                    thread['name'],  # Thread Name
                    thread['state'],  # Thread State
                    stack_trace  # Stack Trace
                ])


# Example usage
directory_path = r"D:\Crossjoin Solutions_td_test\Test"
output_path = r"D:\Crossjoin Solutions_td_test\Test\thread_dump_analysis.csv"
results = analyze_thread_dumps(directory_path)
# print(results)
export_to_csv(results, output_path)
