from datetime import datetime
import re
import os
import csv


def parse_thread_dump(file_content):
    thread_pattern = r'^"(.+)"\s'
    state_pattern = r'\s+java.lang.Thread.State:\s+(\w+)'
    last_call_pattern = r'\s+at\s+(.+)'  # Renamed pattern for last call
    thread_type_pattern = r"^(.*?)-\d+$"  # Pattern to extract thread type

    threads = []
    thread_name = None
    thread_type = None
    thread_state = None
    last_call = None  # Renamed from stack_trace

    lines = file_content.splitlines()
    for i, line in enumerate(lines):
        # Match thread name
        thread_match = re.match(thread_pattern, line)
        if thread_match:
            # Append the previously completed thread
            if thread_name:
                threads.append({
                    'name': thread_name,
                    'type': thread_type,
                    'state': thread_state,
                    'last_call': last_call  # Changed field name
                })

            # Reset for the new thread
            thread_name = thread_match.group(1)
            thread_type_match = re.match(thread_type_pattern, thread_name)
            thread_type = thread_type_match.group(1) if thread_type_match else thread_name
            thread_state = None
            last_call = None  # Reset last_call for new thread

        # Match thread state
        state_match = re.match(state_pattern, line)
        if state_match:
            thread_state = state_match.group(1)

        # Match last call (only first line if there are multiple)
        if last_call is None:
            last_call_match = re.match(last_call_pattern, line)
            if last_call_match:
                last_call = last_call_match.group(1)

    # Append the last thread
    if thread_name:
        threads.append({
            'name': thread_name,
            'type': thread_type,
            'state': thread_state,
            'last_call': last_call  # Changed field name
        })

    return threads


# Define the function to extract the thread type
def extract_thread_type(thread_name):
    match = re.match(r"^(.*?)-\d+$", thread_name)
    if match:
        return match.group(1)
    return thread_name


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
            'Last Call'
        ])

        for result in results:
            for thread in result['threads']:
                last_call = thread['last_call'] if thread['last_call'] else ""

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
                    thread['last_call']  # Stack Trace first line
                ])


# Example usage
directory_path = r"D:\Crossjoin Solutions_td_test\Test"
#directory_path = r"D:\Crossjoin Solutions_td_test\Test_no_thread_type"
output_path = r"D:\Crossjoin Solutions_td_test\Test\thread_dump_analysis.csv"
results = analyze_thread_dumps(directory_path)
# print(results)
export_to_csv(results, output_path)
