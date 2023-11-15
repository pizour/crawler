#!/usr/bin/python3

import re
import time
import asyncio
import aiohttp
import argparse


async def run_crawler(urls_list, deep_level=0, final_list=[], concurrent_sessions=100):
  # Limit the number of concurrent sessions
  semaphore = asyncio.Semaphore(concurrent_sessions)

  # Fetch URL content   
  print(f'Deep level: {deep_level}, Getting content...')
  async with aiohttp.ClientSession() as session:
    tasks = []
    for url in urls_list:
      task = asyncio.create_task(fetch_url(session, semaphore, url))
      tasks.append(task)
    raw_content = await asyncio.gather(*tasks)

  # Parse raw content
  print(f'Deep level: {deep_level}, Parsing content...')
  discovered_urls = find_urls(raw_content)
  
  # Sanitize discovered_urls by removing the ones already existing in final_list
  discovered_urls_sanitized = [url for url in discovered_urls if url not in final_list]

  # Compose final list
  print(f'Deep level: {deep_level}, List length: {len(discovered_urls_sanitized)}')
  for url in discovered_urls_sanitized:
    final_list.append(url)
  print(f'Deep level: {deep_level}, Final List length: {len(final_list)}')
 
  # Export iteration outputs
  file_path_disc = f'output-{deep_level}.txt'
  discovered_urls_sanitized_formatted = [f'{url}\n' for url in discovered_urls_sanitized]
  with open(file_path_disc, 'w') as file:
    file.writelines(discovered_urls_sanitized_formatted)
    print(f"Content-{deep_level} has been saved to '{file_path_disc}'")
      
  # Exit script decision
  if not discovered_urls_sanitized or deep_level >= 6:
    print(f'Discovered: {len(final_list)}')
    file_path = 'output.txt'
    final_list_formatted = [f'{url}\n' for url in final_list]
    with open(file_path, 'w') as file:
      file.writelines(final_list_formatted)
      print(f"Content has been saved to '{file_path}'")
    return None
  else:
  # Resursive call
    await run_crawler(discovered_urls_sanitized, deep_level + 1, final_list)
 
  
async def fetch_url(session, semaphore, url):
  async with semaphore:
    try:
      async with session.get(url,timeout=2) as response:
          return await response.text()
    except Exception as e:
      return f"Error accessing {url}: {e}"


def find_urls(raw_content): 
  SCHEME = r'(https?://)'
  FQDN = r'((?:www\.)?[a-zA-Z0-9._]{2,256}\.[a-zA-Z]{2,6})\b'
  PORT = r'(?:\:[0-9]*)?'
  PATH = r'([-a-zA-Z0-9@:%_\+/]*)'
  url_pattern = re.compile( SCHEME + FQDN + PORT + PATH, re.IGNORECASE)

  discovered_urls = []
  for url_content in raw_content:  
    urls = re.findall(url_pattern, url_content)
    for url in urls:
      discovered_urls.append(''.join(url))

  return list(set(discovered_urls))


# Main flow starts here

if __name__ == "__main__":

  start_time = time.time()
  
  # Format CLI input
  parser = argparse.ArgumentParser(description='Crawler')
  parser.add_argument('--url', help='input URL')
  args = parser.parse_args()

  # Validate input URL
  validated_root_url_list = find_urls([args.url])
  
  # Lets do the job
  asyncio.run(run_crawler(validated_root_url_list))

  # Script measurements
  end_time = time.time()
  duration = (end_time - start_time)
  print(f"Script duration: {duration:.3f} secs")
