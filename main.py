import httpx
import asyncio
import re

scrapedproxies = []


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'referer': "https://www.google.com/"}

def source():
    list = []
    for data in open('sources.txt', 'r'):
        data = data.strip()
        list.append(data)
    return [*set(list)]


def save(name, data):
    cleaned = [*set(data)]
    print(f'{len(cleaned)} Proxies has been scraped!')
    with open(name, 'w') as fp:
        for line in cleaned:
            fp.write("%s\n" % line)

async def scraper(url):
    regexs = [r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]*?(?=\n| |$)", r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b:\d{2,5}"]
    async with httpx.AsyncClient(headers=headers) as client:
        try:
            r = await client.get(url)
            for regex in regexs:
                proxies = re.findall(regex, r.text)
                for proxy in proxies:
                    scrapedproxies.append(proxy)
        except:
            pass


async def main(urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(scraper(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    urls = source()
    proxies = asyncio.run(main(urls))
    save('ScrapedProxies.txt', scrapedproxies)