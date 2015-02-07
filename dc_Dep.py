from HTMLParser import HTMLParser as Html

class dc_Dep(Html):

    def __init__(self):
        Html.__init__(self)
        self.dep_links = []
        self.rec_links = []
        self.sug_links = []
        self.in_dep_flag = 0
        self.in_rec_flag = 0
        self.in_sug_flag = 0
        self.in_dep_div = 0
        self.in_download = 0
        self.download_amd64 = ""
        self.download_i386 = ""

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            if len(attrs) == 0:
                pass
            else:
                for (attr_name, attr_value) in attrs:
                    if attr_name == "id":
                        if attr_value == "pdeps":
                            self.in_dep_div = 1
                        else:
                            if attr_value == "pdownload":
                                self.in_download = 1
                            else:
                                self.in_download = 0
                            self.in_dep_div = 0
                            self.in_dep_flag = 0
                            self.in_rec_flag = 0
                            self.in_sug_flag = 0
        if tag == "ul":
            if len(attrs) == 0 or self.in_dep_div == 0:
                pass
            else:
                for (attr_name, attr_value) in attrs:
                    if attr_name == "class" and attr_value == "uldep":
                        self.in_dep_flag = 1
                        self.in_rec_flag = 0
                        self.in_sug_flag = 0
                    if attr_name == "class" and attr_value == "ulrec":
                        self.in_dep_flag = 0
                        self.in_rec_flag = 1
                        self.in_sug_flag = 0
                    if attr_name == "class" and attr_value == "ulsug":
                        self.in_dep_flag = 0
                        self.in_rec_flag = 0
                        self.in_sug_flag = 1
        if tag == "a":
            if self.in_dep_flag == 1:
                for (attr_name, attr_value) in attrs:
                    if attr_name == "href":
                        self.dep_links.append(attr_value)
            if self.in_rec_flag == 1:
                for (attr_name, attr_value) in attrs:
                    if attr_name == "href":
                        self.rec_links.append(attr_value)
            if self.in_sug_flag == 1:
                for (attr_name, attr_value) in attrs:
                    if attr_name == "href":
                        self.sug_links.append(attr_value)
            if self.in_download == 1:
                for (attr_name, attr_value) in attrs:
                    if attr_name == "href":
                        if attr_value.find("amd64") != -1 and\
                           attr_value.find("download") != -1:
                            self.download_amd64 = attr_value
                        if attr_value.find("i386") != -1 and \
                           attr_value.find("download") != -1:
                            self.download_i386 = attr_value
                        if attr_value.find("all") != -1 and \
                           attr_value.find("download") != -1:
                            self.download_i386 = attr_value
                            self.download_amd64 = attr_value
