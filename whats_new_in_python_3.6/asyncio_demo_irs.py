import asyncio
import os
import urllib.request
from typing import List
 
async def download_coroutine(url):
    """
    A coroutine to download the specified url
    """
    print("In download_coroutine: Downloading URL {url}".format(url=url))
    request = urllib.request.urlopen(url)
    filename = os.path.basename(url)

    with open(filename, 'wb') as file_handle:
        while True:
            chunk = request.read(1024)
            if not chunk:
                break
            file_handle.write(chunk)
    msg = 'Finished downloading {filename}'.format(filename=filename)
    return msg
 
async def main(urls):
    """
    Creates a group of coroutines and waits for them to finish
    """

    coroutines = [download_coroutine(url) for url in urls]  # type: List[Any]
    print("Preparing to call asyncio.wait")
    completed, pending = await asyncio.wait(coroutines) # type: Tuple[Any, Any]
    print("asyncio.wait returned")
    for item in completed:
        print(item.result())
 
 
if __name__ == '__main__':
    urls = ["http://www.irs.gov/pub/irs-pdf/f1040.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
            "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"]
 
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(urls))
    finally:
        event_loop.close()

