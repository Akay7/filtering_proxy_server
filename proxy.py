import re
from urllib.parse import urlparse, urljoin

import aiohttp
from aiohttp import web
from bs4 import BeautifulSoup

TARGET_SERVER_BASE_URL = 'https://habr.com/'


def process_page_links(text: str, target_host: str, proxy_host: str) -> str:
    soup = BeautifulSoup(text, "html.parser")
    for link in soup.find_all('a', href=True):
        # proxy_hosts can have and not ending backslash
        link['href'] = urljoin(proxy_host, link['href'].replace(target_host, '', 1))
    result = str(soup)
    return result


def add_copyright_symbol_to_6_letters_words(text: str) -> str:
    soup = BeautifulSoup(text, "html.parser")
    for string in list(soup.strings):
        if string.parent.name in ['script']:
            continue
        string.replace_with(re.sub(r'(\b\w{6}\b(?!™))', r'\g<1>™', string))
    return str(soup)


async def proxy(request: web.Request) -> web.Response:
    target_host = TARGET_SERVER_BASE_URL
    target_url = urljoin(TARGET_SERVER_BASE_URL, request.match_info['path'])
    headers = dict(request.headers)
    headers['Host'] = urlparse(target_host).netloc
    data = await request.read()

    async with aiohttp.request(request.method, target_url, headers=headers, data=data) as resp:
        if resp.content_type == 'text/html':
            text = await resp.text()
            text = process_page_links(text, target_host, str(request.url.origin()))
            text = add_copyright_symbol_to_6_letters_words(text)

            headers = dict(resp.headers)
            headers.pop('Transfer-Encoding', None)
            headers.pop('Content-Length', None)  # aiohttp will automatically set correct Content-Length
            headers.pop('Content-Encoding', None)
            return web.Response(text=text, status=resp.status, headers=headers)
        return web.Response(body=await resp.read(), status=resp.status, headers=resp.headers)


async def proxy_app_factory(*args):
    app = web.Application()
    app.router.add_route('*', '/{path:.*?}', proxy)
    return app

if __name__ == '__main__':
    web.run_app(proxy_app_factory())
