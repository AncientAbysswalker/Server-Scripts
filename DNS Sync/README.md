# DNS Sync
Periodically the external IP address assigned to me by my ISP changes. Oddly, my ISP offers no way to change this, which causes alot of problems. One problem is that any DNS records (A type) linked to my domain no longer are valid once the external IP address changes. In order to counteract this, I wrote a python script to interact with the API provided by my domain provider (namesilo). I can run this python script as a CRON job on my server, and if the external IP address of my network differs from the DNS records, the script will send requests to update said records.

![DNS Logo](https://raw.githubusercontent.com/AncientAbysswalker/Server-Scripts/main/.readme/dns.png "DNS Logo")
