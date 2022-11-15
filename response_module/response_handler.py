import time
from requests import get,post, exceptions
HTTP_PREFIX = ''.join(['http', '://'])


class Response:

    def __init__(self, source_config):
        self.source_config = source_config
        self.request_config = self.source_config.get('parser_schema', dict())
        self.request_parameter = self.request_config.get('request_parameter', {})
        self.request_details = self.request_config.get('request_details', {})
        self.headers = self.request_parameter.get('headers')
        self.response_method = self.request_details.get('response_type')
        self.response_type = self.request_config.get('request_type')
        self.timeout = self.request_parameter.get('timeout')
        self.verify_ssh_flag = self.request_parameter.get('verify_ssh_flag')
        self.proxy_domain = self.request_config.get('proxy_details',{}).get('proxy_domain')

    def time_out_response(self,search_link, headers, data=None, verify_flag=True, proxy_flag=False):
        method = 'get' if data is None else "post"

        if proxy_flag:
            res = self.requests_proxy(search_link,self.proxy_domain,**{'data':data,'method':method})
            return res
        if method == "post":
            res = post(search_link, headers=headers, data=data, verify=verify_flag)
        else:
            res = get(search_link, headers=headers, verify=verify_flag)
        return res

    def get_response(self, search_link, retries = 3):
        headers = self.headers
        data = self.request_details.get('data',None)
        try:
            time.sleep(0.01)
            res = self.time_out_response(search_link, headers, data=data, verify_flag=self.verify_ssh_flag)
            if res.status_code == 200:
                return res
        except Exception as e:
            res = None
        if not res and retries > 0:
            time.sleep(1 * 60)
            return self.get_response(search_link, self.headers, retries - 1, data)
        return res

    def requests_proxy(self, url='', domain='non-google', *args, **kwargs):
        proxy_prefix = HTTP_PREFIX + 'lum-customer-c_34f0a16d-zone-'
        proxy_path = {
            'google':
                {
                    'https':
                        proxy_prefix + 'static:nsbmyz5qhcyc@zproxy.lum-superproxy.io:22225',
                    'http':
                        proxy_prefix + 'static:nsbmyz5qhcyc@zproxy.lum-superproxy.io:22225'
                },
            'scraping':
                {
                    'http': proxy_prefix + 'scraping_pr:bqkbxwmgcqkf@zproxy.lum-superproxy.io:22225',
                    'https': proxy_prefix + 'scraping_pr:bqkbxwmgcqkf@zproxy.lum-superproxy.io:22225'
                },
        }
        kwargs['proxies'] = proxy_path.get(domain, proxy_path['non-google'])
        method = kwargs.get('method', 'get')
        if 'method' in kwargs.keys():
            del kwargs['method']
        try:
            response = None
            if method == "get":
                response = get(url, *args, **kwargs)
            elif method == "post":
                response = post(url, *args, **kwargs)
        except exceptions.ProxyError as Error:
            raise Error
        return response
























