## URL scanning tool CRAWLER


The python script code exercise to recursively gather URLs from publicly available websites

### Schema:
1. The script requires root URL as an the only input
2. It scans the returned content and searches for all the URLs
3. The scanned URLs are used as an input for next iteration of the script
4. The script should finish once no new URLs are scanned from the fresh content or by hardcoded iteration count

### Usage: From linux CLI
```
crawler.py --url https://example.com
```


### Results:
1. The test has been performed on Ubuntu WSL distro running on top of common office laptop
2. The script experienced an exponential grow of newly discovered URLs
2. The script runs have failed usually around 6th loop iteration, reaching discovered URLs ~ 50k
3. The script bootleneck has been identified in getting content from remote websites
4. At peak time, the HW/OS resource were reaching its limits: Network 30Mbps, TCP conns 200, mem/cpu intermittenly close to 100percent

### Lessons learned:
1. HW/OS resources are a hard limit
2. Python asyncio library can be explored a deeper to tune the script behavior
3. The script execution may trigger some IPS pattern and be dropped as malicious

### Future improvements:
1. pytest integration - Ensure all parts of the script provide expected outputs
2. URL regex corner cases - include regex for URL corner cases(like 'w3.' extensions)
3. Re-use TCP connections for URLs with the same destination
4. Test behavior on resourcefull hardware with tuned OS (file descriptors, tcp reuse, tcp recycle,...)
5. Build production grade distributed Crawler system
    - Brake system into smaller single-functional micro-services
    - Build micro-services communication channels (APIs)
    - In the beginning, offload 'getting_content' service
    - build a scalable getting_content' architecture exposed via API and with L4 loadbalancer layer in front
    - it can be based on on-prem/public-cloud VMs, container systems or fully serverless (i.e. AWS API gateway/Lambda/SQS)
    - If required. other parts of the script can be micro-serviced (i.e. parsing function)
6. Improve script output - implement tree view
7. Migrate script output to suistanable format (i.e. NoSQL db, K/V store)