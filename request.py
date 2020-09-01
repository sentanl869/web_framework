from urllib.parse import unquote_plus
from json import loads


class Request:

    __slots__ = ['raw', 'body', 'method', 'path', 'query', 'headers', 'cookies']

    def __init__(self, raw_data: str) -> None:
        self.raw = raw_data
        headers, self.body = raw_data.split('\r\n\r\n', 1)
        h = headers.split('\r\n')
        p = h[0].split()
        path = p[1]
        self.method = p[0]
        self.path = ''
        self.query = {}
        self.headers = {}
        self.cookies = {}

        self.headers_add(h[1:])
        self.path_parse(path)

    def __repr__(self) -> str:
        return self.raw

    def headers_add(self, header: list) -> None:
        all_lines = header

        for line in all_lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v

        if 'Cookie' in self.headers:
            all_cookies: str = self.headers['Cookie']
            cookies = all_cookies.split('; ')
            for cookie in cookies:
                k, v = cookie.split('=', 1)
                self.cookies[k] = v

    def path_parse(self, path: str) -> None:
        index = path.find('?')
        if index == -1:
            self.path = path
        else:
            path, query_content = path.split('?', 1)
            args = query_content.split('&')
            query = {}
            for arg in args:
                k, v = arg.split('=', 1)
                query[k] = v

            self.path = path
            self.query = query

    def form(self) -> dict:
        body = unquote_plus(self.body)
        args = body.split('&')
        form = {}
        for arg in args:
            k, v = arg.split('=', 1)
            form[k] = v
        return form

    def json(self) -> dict:
        return loads(self.body)
