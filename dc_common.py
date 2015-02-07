import urllib

def get_deb_name_by_url(url):
    ret = ""
    pos = url.rfind("/")
    if pos < 0:
        return ret
    ret = url[pos+1:]
    return ret

def get_deb_name_by_path(url):
    ret = ""
    pos = url.rfind("\\")
    if pos < 0:
        return ret
    ret = url[pos+1:]
    return ret

def get_content(url):
    print "Caught url : " + url
    content = None
    flag = 0
    for i in range(10):
        try:
            content = urllib.urlopen(url).read()
            flag = 1
        except IOError, e:
            print e
        else:
            break
        if flag == 1:
            break
        print "URLError occured, tried {0} time.".format(i)

    if flag == 0:
        print "URLError timeout."
        self.successed = "false"
        content = None
    return content
