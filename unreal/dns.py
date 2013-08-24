backend_list = [("www.zhaosf.com", "113.105.175.221"),
                ("www.163.com", "113.107.76.19")]

BACKEND_DICT = dict()

def get_backend(host):
    return BACKEND_DICT.get(host)

def init():
    for (host, ip) in backend_list:
        BACKEND_DICT.setdefault(host, ip)
        
init()
