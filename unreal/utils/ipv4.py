# *_* coding=utf8 *_*
#!/usr/bin/env python

def to_int(ip_address):
    ip_v4 = 0
    locs = map(int, ip_address.split("."))
    for i, loc in enumerate(locs):
        ip_v4 += loc << (24 - 8 * i)
    return ip_v4


def to_address(ip_v4):
    ip_bits = []
    for i in xrange(4):
        ip_bits.append(ip_v4 % 256)
        ip_v4 = ip_v4 / 256
        
    ip_bits.reverse()
    return '.'.join(map(str, ip_bits))
