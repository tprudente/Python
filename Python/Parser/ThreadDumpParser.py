from datetime import datetime
import re
import os
import csv

def parse_thread_dump(file_content):
    thread_pattern = r'^"(.+)"\s' #Matches the thread name. It captures the text between double quotes at the start of each thread's information.
    state_pattern = r'\s+java.lang.Thread.State:\s+(\w+)' # Matches the thread state, such as "RUNNABLE" or "WAITING," which appears after java.lang.Thread.State.
    last_call_pattern = r'\s+at\s+(.+)'  # Matches the last method call in the stack trace (i.e., the line starting with "at").
    custom_call_pattern = r'\s+at\s+(com\.crossjointest\..+)'  # Captures method calls from the specific package com.crossjointest, indicating custom code.
    thread_type_pattern = r"^(.*?)-\d+$"  # Extracts the general type of the thread by removing any numeric suffixes at the end of the thread name.

    threads = []
    thread_name = None
    thread_type = None
    thread_state = None
    last_call = None
    last_custom_call = None

    lines = file_content.splitlines()
    for line in lines:
        # Match thread name
        thread_match = re.match(thread_pattern, line)
        if thread_match:
            if thread_name:
                threads.append({
                    'name': thread_name,
                    'type': thread_type,
                    'state': thread_state,
                    'last_call': last_call,
                    'last_custom_call': last_custom_call
                })

            # Reset for the new thread
            thread_name = thread_match.group(1)
            thread_type_match = re.match(thread_type_pattern, thread_name)
            thread_type = thread_type_match.group(1) if thread_type_match else thread_name
            thread_state = None
            last_call = None
            last_custom_call = None

        # Match thread state
        state_match = re.match(state_pattern, line)
        if state_match:
            thread_state = state_match.group(1)

        # Match last call (first call found)
        last_call_match = re.match(last_call_pattern, line)
        if last_call_match and last_call is None:
            last_call = last_call_match.group(1)

        # Capture the most recent custom call in the thread stack trace
        custom_call_match = re.match(custom_call_pattern, line)
        if custom_call_match:
            last_custom_call = custom_call_match.group(1)

    # Append the last thread
    if thread_name:
        threads.append({
            'name': thread_name,
            'type': thread_type,
            'state': thread_state,
            'last_call': last_call,
            'last_custom_call': last_custom_call
        })

    return threads

def extract_thread_instance_and_timestamp(filename):
    thread_instance = filename.split('-')[-1].split('_')[0]
    raw_timestamp = filename.split('_')[-1]

    # Parse the timestamp in the format "yyyyMMddHHmmss"
    timestamp_obj = datetime.strptime(raw_timestamp, "%Y%m%d%H%M%S")

    # Format the timestamp in various formats
    timestamp_date = timestamp_obj.strftime("%Y-%m-%d")
    timestamp_hour = timestamp_obj.strftime("%Y-%m-%d %H:00:00")
    timestamp_minute = timestamp_obj.strftime("%Y-%m-%d %H:%M:00")
    timestamp_second = timestamp_obj.strftime("%Y-%m-%d %H:%M:%S")

    return {
        'thread_instance': thread_instance,
        'timestamp_date': timestamp_date,
        'timestamp_hour': timestamp_hour,
        'timestamp_minute': timestamp_minute,
        'timestamp_second': timestamp_second
    }

def analyze_thread_dumps(directory_path):
    results = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                file_content = file.read()
                threads = parse_thread_dump(file_content)

                timestamp_info = extract_thread_instance_and_timestamp(filename)

                results.append({
                    'file': filename,
                    'timestamp_info': timestamp_info,
                    'threads': threads
                })
    return results

def export_to_csv(results, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';')
        csv_writer.writerow([
            'Timestamp (yyyy-mm-dd)',
            'Timestamp (yyyy-mm-dd hh24:00:00)',
            'Timestamp (yyyy-mm-dd hh24:mi:00)',
            'Timestamp (yyyy-mm-dd hh24:mi:ss)',
            'Instance',
            'Thread Type',
            'Thread Name',
            'State',
            'Last Call',
            'Last Custom Call'
        ])

        for result in results:
            for thread in result['threads']:
                last_call = thread['last_call'] if thread['last_call'] else ""
                last_custom_call = thread['last_custom_call'] if thread['last_custom_call'] else ""

                # Write the row with the various timestamp formats and thread details
                csv_writer.writerow([
                    result['timestamp_info']['timestamp_date'],  # Timestamp (yyyy-mm-dd)
                    result['timestamp_info']['timestamp_hour'],  # Timestamp (yyyy-mm-dd hh24:00:00)
                    result['timestamp_info']['timestamp_minute'],  # Timestamp (yyyy-mm-dd hh24:mi:00)
                    result['timestamp_info']['timestamp_second'],  # Timestamp (yyyy-mm-dd hh24:mi:ss)
                    result['timestamp_info']['thread_instance'],  # Thread Instance
                    thread['type'],
                    thread['name'],  # Thread Name
                    thread['state'],  # State
                    last_call,        # Last Call
                    last_custom_call  # Last Custom Call with "com.crossjointest"
                ])

# Example usage
directory_path = r"D:\Crossjoin Solutions_td_test\Test"
output_path = r"D:\Crossjoin Solutions_td_test\Test\thread_dump_analysis.csv"
results = analyze_thread_dumps(directory_path)
export_to_csv(results, output_path)
