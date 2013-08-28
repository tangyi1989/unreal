#*_* coding=utf8 *_*
#!/usr/bin/env python

import icu
import cStringIO

def add_html_header(body, headers):
    string_io = cStringIO.StringIO()
    lower_body = body.lower()

    header_index = lower_body.find("</head>")
    if header_index == -1:
        return body

    string_io.write(body[:header_index])
    string_io.write('\r\n'.join(headers))
    string_io.write(body[header_index:])
    string_io.seek(0)

    return string_io.read()

def convert_encoding(data, new_coding='UTF-8'):
    coding = icu.CharsetDetector(data).detect().getName()
    if new_coding.upper() != coding.upper():
        data = unicode(data, coding).encode(new_coding)
    return data