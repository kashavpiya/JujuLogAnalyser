import argparse
import re
from collections import defaultdict, Counter


# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Process Juju log files.")
    parser.add_argument('filename', type=str, help='The log file to process')
    parser.add_argument('--charm', type=str, help='Filter logs by charm name', required=False)
    return parser.parse_args()


# Function to parse individual log lines
def parse_line(line):
    match = re.match(r'^(?P<charm_name>\S+): (?P<timestamp>\S+) (?P<severity>\w+)\s+juju\.\w+.*(?P<message>.*)$',
                     line.strip())
    if match:
        return match.group('charm_name'), match.group('timestamp'), match.group('severity'), match.group('message')
    return None


# Function to process the entire log file
def process_log_file(filename, charm_filter=None):
    charm_logs = defaultdict(lambda: defaultdict(list))
    total_logs = defaultdict(list)

    with open(filename, 'r') as file:
        for line in file:
            parsed = parse_line(line)
            if parsed:
                charm, _, severity, message = parsed
                if charm_filter and charm_filter != charm:
                    continue  # Skip logs not matching the filter
                charm_logs[charm][severity].append(message)
                total_logs[severity].append(message)

    return charm_logs, total_logs


# Function to analyze the processed logs
def analyze_logs(charm_logs, total_logs):
    charm_warnings = [charm for charm, logs in charm_logs.items() if "WARNING" in logs]
    duplicate_counts = Counter()

    # Count duplicates and total messages
    for logs in charm_logs.values():
        for messages in logs.values():
            duplicate_counts.update(Counter(messages))

    total_messages = sum(len(messages) for messages in total_logs.values())
    severity_counts = {severity: len(messages) for severity, messages in total_logs.items()}
    severity_proportions = {severity: count / total_messages for severity, count in severity_counts.items()}

    return charm_warnings, severity_counts, duplicate_counts, severity_proportions, total_messages


# Function to print the analysis results
def print_results(charm_warnings, severity_counts, duplicate_counts, severity_proportions, total_messages, charm_logs):
    if charm_warnings:
        print("Charms with warnings:")
        for charm in charm_warnings:
            print(f"  {charm}")

    print("\nSeverity Counts:")
    for severity, count in severity_counts.items():
        print(f"  {severity}: {count}")

    print("\nDuplicate Messages:")
    for message, count in duplicate_counts.items():
        print(f"  {message} (x{count})")

    print("\nSeverity Proportions:")
    for severity, proportion in severity_proportions.items():
        print(f"  {severity}: {proportion:.2%}")

    print("\nTotal Messages Per Charm:")
    for charm, logs in charm_logs.items():
        print(f"  {charm}: {sum(len(messages) for messages in logs.values())} messages")

    print(f"\nTotal Number of Log Messages: {total_messages}")


# Main function to integrate all components and run the program
def main():
    args = parse_arguments()
    charm_logs, total_logs = process_log_file(args.filename, args.charm)
    charm_warnings, severity_counts, duplicate_counts, severity_proportions, total_messages = analyze_logs(charm_logs,
                                                                                                           total_logs)
    print_results(charm_warnings, severity_counts, duplicate_counts, severity_proportions, total_messages, charm_logs)


# Ensure the program runs only when executed directly
if __name__ == '__main__':
    main()
