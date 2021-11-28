# importing the requests library
import requests
import xml.etree.ElementTree as ET

# Debug flags
show_debug_prints = False

def debug_print(printable):
    if show_debug_prints:
        print(printable)

# api variables
domain_name = # Domain URL goes here - e.g. "google.com"
api_key = # API Key from Name Silo goes here

# api-endpoint
get_dns_records_url = f"https://www.namesilo.com/api/dnsListRecords?version=1&type=xml&key={api_key}&domain={domain_name}"
update_dns_records_url = f"https://www.namesilo.com/api/dnsUpdateRecord?version=1&type=xml&key={api_key}&domain={domain_name}" + "&rrid={record_id}&rrhost={host_address}&rrvalue={host_ip}&rrttl={host_ttl}"
delete_dns_records_url = f"https://www.namesilo.com/api/dnsDeleteRecord?version=1&type=xml&key={api_key}&domain={domain_name}" + "&rrid={record_id}"

# Get the list of current DNS records under the current domain
print("Requesting list of DNS records")
dns_records_response = requests.get(url=get_dns_records_url)
debug_print(get_dns_records_url)
dns_records_xml_root = ET.fromstring(dns_records_response.content)
dns_records_response_status = dns_records_xml_root.find('./reply/code').text

# A code of 300 returns on successful record retrieval. Assorted other codes (including 200) are returned otherwise
if dns_records_response_status != "300":
    dns_records_response_detail = dns_records_xml_root.find('./reply/detail').text
    raise ConnectionError(f"Something went wrong retrieving the DNS Records: {dns_records_response_detail}")
print("DNS records retrieved")

# Get the IP address that this script is running from (on a server in the network in question)
requestor_ip = dns_records_xml_root.find('./request/ip').text
print(f"Current external IP is {requestor_ip}")

# Get the list of existing DNS records
print("Checking for records with outdated IP addresses")
dns_records_list = []
for dns_record in dns_records_xml_root.findall('./reply/resource_record'):
    record_type = dns_record.find('./type').text
    record_id = dns_record.find('./record_id').text
    host_address = dns_record.find('./host').text
    host_ip = dns_record.find('./value').text
    host_ttl = dns_record.find('./ttl').text

    # We only need to worry about updating "A" records, where the ip does not match the requestor_ip
    if record_type == 'A' and host_ip != requestor_ip:
        print(f"Found outdated record for host {host_address} with listed IP {host_ip}")
        # print(host_address.replace(f".{domain_name}", ""))
        dns_records_list.append({
            "record_id": record_id,
            "full_host_address": host_address,
            "host_address": host_address.replace(f".{domain_name}", "").replace(domain_name, ""),
            "original_host_ip": host_ip,
            "host_ip": requestor_ip,
            "host_ttl": host_ttl
        })

# Update the existing DNS records that are using an outdated IP address
for dns_record in dns_records_list:
    print(f"Updating record for host {dns_record['full_host_address']} with listed IP {dns_record['original_host_ip']}")
    debug_print(update_dns_records_url.format(**dns_record))
    update_record_response = requests.post(url=update_dns_records_url.format(**dns_record))
    update_record_xml_root = ET.fromstring(update_record_response.content)
    update_record_response_status = update_record_xml_root.find('./reply/code').text

    if update_record_response_status != "300":
        update_record_response_detail = dns_records_xml_root.find('./reply/detail').text
        raise ConnectionError(f"Something went wrong updating the DNS Records: {update_record_response_detail}")

    # I think that the below observed behavior was lag in running DB operations? Commented out for now...
    # For some reason the update request makes NEW records, so I guess we need to remove the old records?? Odd database...
    # print(f"Deleting original record for host {dns_record['full_host_address']}")
    # debug_print(delete_dns_records_url.format(**dns_record))
    # delete_record_response = requests.post(url=delete_dns_records_url.format(**dns_record))
    # delete_record_xml_root = ET.fromstring(delete_record_response.content)
    # delete_record_response_status = delete_record_xml_root.find('./reply/code').text
    #
    # if delete_record_response_status != "300":
    #     delete_record_response_detail = delete_record_xml_root.find('./reply/detail').text
    #     raise ConnectionError(f"Something went wrong updating the DNS Records: {delete_record_response_detail}")
