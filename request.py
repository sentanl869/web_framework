class Request:

    def __init__(self, raw_data: str):
        headers, self.body = raw_data.split('\r\n\r\n', 1)
        h = headers.split('\r\n')
        p = h[0].split()
        path = p[1]
        self.method = p[0]
        self.path = ''
        self.query = dict()
        self.headers = dict()
        self.cookies = dict()

        self.headers_add(h[1:])
        self.path_parse(path)

    def headers_add(self, header: list):
        all_lines = header

        for line in all_lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v

        if 'Cookie' in self.headers:
            all_cookies: str = self.headers['Cookie']
            cookies = all_cookies.split('; ')
            for cookie in cookies:
                k, v = cookie.split('=')
                self.cookies[k] = v

    def path_parse(self, path: str):
        index = path.find('?')
        if index == -1:
            self.path = path
        else:
            path, query_content = path.split('?', 1)
            args = query_content.split('&')
            query = dict()
            for arg in args:
                k, v = arg.split('=')
                query[k] = v

            self.path = path
            self.query = query
