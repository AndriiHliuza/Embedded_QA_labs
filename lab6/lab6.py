import subprocess
import re

ip = '192.168.56.101'


def client(server):
    try:
        result = subprocess.run(['iperf', '-c', server], capture_output=True, text=True, check=True)
        return result.stdout, None
    except subprocess.CalledProcessError as e:
        return None, f"Error: {e.stderr}"


def parse(text):
    result = []

    # Use regular expressions to find intervals in the iperf output
    intervals = re.findall(r'\[\s*(\d+)\]\s+(\d+\.\d+-\d+\.\d+)\s+sec\s+(\d+\.\d+)\s+GBytes\s+(\d+\.\d+)\s+Gbits/sec', text)

    for interval in intervals:
        result_dict = {
            # 'ID': int(interval[0]),  # ID field is commented out as it is not used
            'Interval': interval[1],
            'Transfer': float(interval[2]),
            'Bitrate': float(interval[3])
        }

        result.append(result_dict)

    return result


result, error = client(ip)

result_list = parse(result)

for value in result_list:
    if value['Transfer'] > 2 and value['Bitrate'] > 20:
        print(value)
