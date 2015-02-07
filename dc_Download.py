from HTMLParser import HTMLParser as html


class dc_Download(html):

    def __init__(self):
        html.__init__(self)
        self.downloaded = 0
        self.download_url = ""

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            if len(attrs) == 0:
                pass
            else:
                for (attr_name, attr_value) in attrs:
                    if attr_name == "href":
                        if attr_value.find(".deb") != -1 and\
                            (attr_value.find("kr.archive.ubuntu.com") != -1 or
                             attr_value.find("security.ubuntu.com") != -1):
                            self.download_url = attr_value
                            self.downloaded = 1
