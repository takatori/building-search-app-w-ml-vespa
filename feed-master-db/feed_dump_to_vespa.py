#!usr/bin/env python
import bz2
from vespa.application import Vespa


def generate_bulk_buffer():
    buf = []
    with bz2.open("dataset/simplewiki-202109-pages-with-pageviews-20211001.bz2", "rt") as bz2f:
        for line in bz2f:
            id, title, text, pageviews = line.rstrip().split("\t")
            buf.append(
                {
                    "id": id,
                    "fields": {
                        "title": title,
                        "text": text,
                        "pageviews": pageviews
                    }
                }
            )
            if 500 <= len(buf):
                yield buf
                buf.clear()
    if buf:
        yield buf
        

client = Vespa(url = 'http://vespa', port = 8080)

def callback(response, id):
    if not response.is_successful():
        print(
            f"Failed to feed document {id} with status code {response.status_code}: Reason {response.get_json()}"
        )
    
for buf in generate_bulk_buffer():
    client.feed_iterable(buf, schema = "simplewiki", callback=callback)