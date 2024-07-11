import base64
from datetime import datetime

import numpy as np

DIRECTION = {"L2L": [1, 0, 0, 0], "L2R": [0, 1, 0, 0], "R2L": [0, 0, 1, 0], "R2R": [0, 0, 0, 1]}
TCP_FLAGS_DESCRIPTION = {"F": [1, 0, 0, 0, 0, 0, 0, 0, 0], "A": [0, 1, 0, 0, 0, 0, 0, 0, 0], "S": [0, 0, 1, 0, 0, 0, 0, 0, 0],
                            "R": [0, 0, 0, 1, 0, 0, 0, 0, 0], "P": [0, 0, 0, 0, 1, 0, 0, 0, 0], "N/A": [0, 0, 0, 0, 0, 1, 0, 0, 0],
                            "Illegal8": [0, 0, 0, 0, 0, 0, 1, 0, 0], "U": [0, 0, 0, 0, 0, 0, 0, 1, 0], "Illegal7": [0, 0, 0, 0, 0, 0, 0, 0, 1]}
PROTOCOL_NAME = {"igmp": [1, 0, 0, 0, 0, 0], "ip": [0, 1, 0, 0, 0, 0], "tcp_ip": [0, 0, 1, 0, 0, 0],
                 "icmp_ip": [0, 0, 0, 1, 0, 0], "udp_ip": [0, 0, 0, 0, 1, 0], "ipv6icmp": [0, 0, 0, 0, 0, 1]}
TCP_FLAGS_SECOND_CHALLENGE_DESCRIPTION = {"A": [1, 0, 0, 0, 0], "P": [0, 1, 0, 0, 0], "R": [0, 0, 1, 0, 0],
                                     "S": [0, 0, 0, 1, 0], "F": [0, 0, 0, 0, 1]}
PROTOCOL_NAME_SECOND_CHALLENGE = {"TCP": [1, 0, 0, 0], "UDP": [0, 1, 0, 0], "ICMP": [0, 0, 1, 0], "IGMP": [0, 0, 0, 1]}

def vectorized_ip(ip: str):
    """
    The function `vectorize_ip` vectorizes an IP address.
    :param ip: an IP address
    :return: a vectorized IP address
    :rtype: int
    """
    return int(''.join([octet for octet in ip.split(".")]))

def vectorized_tcp_flag(tcp_flag: str):
    """
    The function `vectorize_tcp_flag` vectorizes a TCP flag.
    :param tcp_flag: a TCP flag
    :return: a vectorized TCP flag
    :rtype: list

    >>> print(vectorized_tcp_flag("ASR"))
    [0, 1, 1, 1, 0, 0, 0, 0, 0]
    """
    return np.sum([TCP_FLAGS_DESCRIPTION.get(flag, np.zeros(6)) for flag in tcp_flag.split(",")], axis=0).tolist()

def vectorized_time(datetime: str):
    """
    The function `vectorize_time` vectorizes a time.
    :param datetime: a time
    :return: a vectorized time
    :rtype: list

    >>> print(vectorized_time("2010-06-14T23:59:48"))
    [20100614, 235948]
    """
    date = datetime.split("T")[0].split("-")
    time = datetime.split("T")[1].split(":")

    return [int(''.join(date)), int(''.join(time))]

def vectorized_payload(payload: str):
    """
    The function `vectorize_payload` vectorized a payload. The vectorization process is based on the sum of the ASCII
    value of each character of the payload. The payload is split into 4 subsets. If the payload is less than 8
    characters, the payload is split into 1 subset.
    :param payload: a payload
    :return: a vectorized payload of size 1x4
    :rtype: list

    >>> print(vectorized_payload("Hello"))
    [448, 0, 0, 0]
    """
    try:
        payload = base64.b64decode(payload).decode("utf-8")
    except:
        pass

    vector = np.zeros(8, dtype=int)

    # if len < 4, add the ASCII value of each character and return
    if len(payload) < 8:
        for caract in payload:
            vector[0] += ord(caract)

        return vector

    # split the payload into 4 subsets
    subsets_size = len(payload) // 8
    subsets = [payload[i * subsets_size:(i + 1) * subsets_size] for i in range(0, 8)]

    # Sum the ASCII value of each character of each subset
    for i, subset in enumerate(subsets):
        for caract in subset:
            vector[i] += ord(caract)

    return vector


def vectorized(flow: dict):
    """
    The function `vectorize` vectorizes a flow. The vectorization process is based on the following features:
    - totalSourceBytes                  - totalDestinationBytes
    - totalDestinationPackets           - totalSourcePackets
    - sourcePayloadAsBase64             - destinationPayloadAsBase64
    - direction                         - sourceTCPFlagsDescription
    - destinationTCPFlagsDescription    - protocolName
    - source                            - destination
    - sourcePort                        - destinationPort
    :param flow: a flow
    :return: a vectorized flow
    :rtype: list

    >>> print(vectorized(flow={
    ...     "totalSourceBytes": "384",
    ...     "totalDestinationBytes": "0",
    ...     "totalDestinationPackets": "0",
    ...     "totalSourcePackets": "6",
    ...     "sourcePayloadAsBase64": "",
    ...     "destinationPayloadAsBase64": "",
    ...     "destinationPayloadAsUTF": "",
    ...     "direction": "L2R",
    ...     "sourceTCPFlagsDescription": "F,A",
    ...     "destinationTCPFlagsDescription": "",
    ...     "source": "
    ...     "protocolName": "tcp_ip",
    ...     "sourcePort": "4435",
    ...     "destination": "206.217.198.186",
    ...     "destinationPort": "80",
    ...     "startDateTime": "2010-06-13T23:58:23",
    ...     "stopDateTime": "2010-06-14T00:01:24",
    ...     "Tag": "Normal"
    }))
    [384, 0, 0, 6, 4435, 0, 0, 80, 1921682111, 206217198186, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 20100613, 235823, 20100614, 124]
    """
    source_tcp_flags_description      = flow["sourceTCPFlagsDescription"]
    destination_tcp_flags_description = flow["destinationTCPFlagsDescription"]
    start_date_time                   = flow["startDateTime"]
    stop_date_time                    = flow["stopDateTime"]
    source_payload_as_base64          = flow["sourcePayloadAsBase64"]
    destination_payload_as_base64     = flow["destinationPayloadAsBase64"]

    res = [
        int(flow["totalSourceBytes"]),
        int(flow["totalDestinationBytes"]),
        int(flow["totalDestinationPackets"]),
        int(flow["totalSourcePackets"]),
        int(flow["sourcePort"]),
        int(len(source_payload_as_base64) if source_payload_as_base64 else 0),
        int(len(destination_payload_as_base64) if destination_payload_as_base64 else 0),
        int(flow["destinationPort"]),
        vectorized_ip(ip=flow["source"]),
        vectorized_ip(ip=flow["destination"])
    ]

    res.extend(vectorized_payload(payload=source_payload_as_base64) if source_payload_as_base64 else np.zeros(8, dtype=int).tolist())
    res.extend(vectorized_payload(payload=destination_payload_as_base64) if destination_payload_as_base64 else np.zeros(8, dtype=int).tolist())
    res.extend(DIRECTION[flow["direction"]])
    res.extend(vectorized_tcp_flag(tcp_flag=source_tcp_flags_description) if source_tcp_flags_description else np.zeros(9, dtype=int).tolist())
    res.extend(vectorized_tcp_flag(tcp_flag=destination_tcp_flags_description) if destination_tcp_flags_description else np.zeros(9, dtype=int).tolist())
    res.extend(PROTOCOL_NAME[flow["protocolName"]])
    res.extend(vectorized_time(datetime=start_date_time) if start_date_time else 0)
    res.extend(vectorized_time(datetime=stop_date_time) if stop_date_time else 0)

    return res

def run_vectorization(flows: list[dict], is_second_challenge: bool = False):
    """
    The function `run_vectorization` runs the vectorization process.
    :param flows: a list of flows
    :return: a list of vectors
    :rtype: list
    """
    vectors = []

    for flow in flows:
        vectors.append(vectorized(flow=flow) if not is_second_challenge else vectorized_second_challenge(flow=flow))

    return vectors

#############################################################################
# second challenge
#############################################################################

def vectorize_timestamp(timestamp: float):
    """
    The function `vectorize_timestamp` vectorizes a timestamp.
    :param timestamp: a timestamp
    :return: a vectorized timestamp
    :rtype: list

    >>> print(vectorize_timestamp(1276544388))
    [20100614, 235948]
    """
    date_time = datetime.fromtimestamp(timestamp)
    formatted_date_time = date_time.strftime("%Y-%m-%dT%H:%M:%S") # Format the datetime object as a string

    return vectorized_time(datetime=formatted_date_time)

def vectorize_ip_second_challenge(ip: str):
    """
    The function `vectorize_ip_second_challenge` vectorizes an IP address.
    :param ip: an IP address
    :return: a vectorized IP address
    :rtype: int

    >>> print(vectorize_ip_second_challenge("127.0.0.1"))
    127001
    >>> print(vectorize_ip_second_challenge("EXT_SERVER"))
    69888495836982866982
    >>> print(vectorize_ip_second_challenge("AB_DERF"))
    65669568698270
    """
    if '.' in ip : res = int(''.join([octet for octet in ip.split(".")]))
    elif 'EXT_SERVER' in ip: res = int(''.join([str(ord(elt)) for elt in ip]))
    elif '_' in ip : res = int(ip.replace('_', ''))
    else : res = int(''.join([str(ord(elt)) for elt in ip]))

    return res

def vectorize_flags_second_challenge(flags: str):
    """
    The function `vectorize_flags_second_challenge` vectorizes a flag.
    :param flags: a flag
    :return: a vectorized flag
    :rtype: list

    >>> print(vectorize_flags_second_challenge("A.S.R"))
    [1, 1, 1, 0, 0]
    """
    flags = flags.replace(".", "")
    return np.sum([TCP_FLAGS_SECOND_CHALLENGE_DESCRIPTION.get(flag) for flag in flags], axis=0).tolist()

def vectorized_bytes(bytes: str):
    """
    The function `vectorized_bytes` vectorizes a byte.
    :param bytes: a byte
    :return: a vectorized byte
    :rtype: int

    >>> print(vectorized_bytes("1.2M"))
    1200000
    >>> print(vectorized_bytes("1.2K"))
    1200
    >>> print(vectorized_bytes("1"))
    1
    """
    if 'M' in bytes : res = int(float(bytes.replace('M', '')) * 1000000)
    elif 'K' in bytes : res = int(float(bytes.replace('K', '')) * 1000)
    else : res = int(bytes)

    return res

def vectorized_second_challenge(flow: dict):
    """
    The function `vectorized_second_challenge` vectorizes a flow. The vectorization process is based on the following features:
    - Timestamp                  - Duration
    - Protocol                   - Src_IP_Add
    - Src_Pt                     - Dst_IP_Add
    - Dst_Pt                     - Packets
    - Bytes                      - Flags
    - Tos
    :param flow: a flow
    :return: a vectorized flow
    :rtype: list

    >>> print(vectorized_second_challenge(flow={
    ...     "Timestamp": "1276544388",
    ...     "Duration": "0.000000",
    ...     "Protocol": "TCP",
    ...     "Src_IP_Add": "192.168.2.111",
    ...     "Src_Pt": "4435",
    ...     "Dst_IP_Add": "206.217.198.186",
    ...     "Dst_Pt": "80",
    ...     "Packets": "6",
    ...     "Bytes": "384",
    ...     "Flows": "1",
    ...     "Flags": "A.S.R",
    ...     "Tos": "0",
    ...     "class": "Normal"
    }))
    [0, 4435.0, 80.0, 6, 384, 0, 1921682111, 206217198186, 1, 0, 0, 0, 1, 0, 1, 1, 0, 20100614, 213948]
    """
    dst_pt = int(flow['Dst_Pt'].strip()) if isinstance(flow['Dst_Pt'].strip(), float) else float(flow['Dst_Pt'].strip())
    src_pt = int(flow['Src_Pt'].strip()) if isinstance(flow['Src_Pt'].strip(), float) else float(flow['Src_Pt'].strip())

    res = [
        int(float(flow["Duration"].strip())),
        src_pt,
        dst_pt,
        int(flow["Packets"].strip()),
        vectorized_bytes(flow["Bytes"].strip()) if flow["Bytes"].strip() != "" else 0,
        # int(flow["Flows"].strip()), NOTE : pas mis car que des 1
        int(flow["Tos"].strip()),
        vectorize_ip_second_challenge(flow["Src_IP_Add"].strip()) if flow["Src_IP_Add"].strip() != "" else 0,
        vectorize_ip_second_challenge(flow["Dst_IP_Add"].strip()) if flow["Dst_IP_Add"].strip() != "" else 0
    ]

    flags = flow["Flags"].strip().replace(".", "")

    res.extend(PROTOCOL_NAME_SECOND_CHALLENGE[flow["Protocol"].strip()] if flow["Protocol"].strip() != "" else np.zeros(4, dtype=int).tolist())
    res.extend(vectorize_flags_second_challenge(flags) if flags != "" else np.zeros(5, dtype=int).tolist())
    res.extend(vectorize_timestamp(float(flow["Timestamp"].strip())) if flow["Timestamp"].strip() != "" else np.zeros(2, dtype=int).tolist())

    return res
