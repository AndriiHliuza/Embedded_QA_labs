import re


def parse(text):
    regexp = r'\[\s*(\d+)\]\s+(\d+\.\d+-\d+\.\d+)\s+sec\s+(\d+(?:\.\d+)?)\s+(G|M)Bytes\s+(\d+(?:\.\d+)?)\s+(G|M)bits/sec\s+(\d+)\s+(\d+)\s+KBytes'
    KEYS = ('ID', 'Interval', 'Transfer', 'Bitrate', 'Retr', 'Cwnd')

    result_list = []

    intervals = re.findall(regexp, text)

    for interval in intervals:
        id_, interval, transfer, transfer_unit, bitrate, bitrate_unit, retr, cwnd = interval
        id_ = int(id_)

        transfer = float(transfer)
        if transfer_unit == 'G':
            transfer *= 1000

        bitrate = float(bitrate)
        if bitrate_unit == 'G':
            bitrate *= 1000

        retr = int(retr)
        cwnd = int(cwnd)

        result_dict = dict(zip(KEYS[1:], (id_, interval, transfer, bitrate, retr, cwnd)[1:]))
        result_list.append(result_dict)

    return result_list
