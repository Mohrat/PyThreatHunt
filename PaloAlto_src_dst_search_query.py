# Reading IOC's from Text file, repalcing [.] with . and creating PaloAlto Search query
def replace_ip_format(ip_addresses):
    formatted_ips = []

    for ip in ip_addresses:
        formatted_ips.append(ip.replace('[.]', '.'))

    return formatted_ips

def create_query(ip_addresses):
    query = ""
    for ip in ip_addresses:
        query += f"(addr.src in {ip}) or (addr.dst in {ip}) or\n"

    return query

if __name__ == "__main__":
    file_path = "ip_addresses.txt"

    # Step 1: Read IP addresses from the file
    with open(file_path, "r") as file:
        ip_addresses = [line.strip() for line in file.readlines()]

    # Step 2: Replace [.] with .
    formatted_ips = replace_ip_format(ip_addresses)

    # Step 3: Create the query
    query = create_query(formatted_ips)

    print(query)
