import glob
import sys
import urllib
import xml.etree.ElementTree as ET
import ConfigParser as Config

from dc_DebList import *
from dc_common import *

config = Config.ConfigParser()
config.read("config.ini")
url_head = config.get("Downloader", "url_head")
data_path = config.get("Data", "data_path")
deb_path = config.get("Deb", "deb_path")

def callbackfunc(blocknum, blocksize, totalsize):
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    print "downloading %.2f%%" % percent,
    sys.stdout.write("\r")

in_stack = []
except_stack = []
def mktree(url, mask=3):
    if in_stack.count(url) > 0:
        return
    name = get_deb_name_by_url(url)
    if except_stack.count(name) > 0:
        return
    in_stack.append(url)
    deblist = dc_DebList()
    deblist.init("local", url, name)
    if (mask&1):
        for url_nxt in deblist.dependance_url:
            mktree(url_nxt, mask)
    if (mask&2):
        for url_nxt in deblist.recommand_url:
            mktree(url_nxt, mask)
    if (mask&4):
        for url_nxt in deblist.suggest_url:
            mktree(url_nxt, mask)

downloaded_stack = []
def download(platform):
    deb_list = glob.glob(deb_path+"*.deb")
    for deb_path_tmp in deb_list:
        deb_name = get_deb_name_by_path(deb_path_tmp)
        downloaded_stack.append(deb_name)
    xml_list = glob.glob(data_path+"*.xml")
    for xml_path in xml_list:
        #xml_name = get_deb_name_by_path(xml_path)
        tree = ET.parse(xml_path)
        data = tree.getroot()
        download_url = ""
        if platform == "amd64":
            download_url = data.find("download_amd64_url").text
        elif platform == "i386":
            download_url = data.find("download_i386_url").text
        else:
            download_url = ""
        if download_url == None:
            download_url = ""
        deb_name = get_deb_name_by_url(download_url)
        if downloaded_stack.count(deb_name) > 0 or download_url=="":
            pass
        else:
            print download_url
            urllib.urlretrieve(download_url, deb_path+deb_name, callbackfunc)
            downloaded_stack.append(deb_name)

def init_except_file():
    except_file = open("package.list", "r")
    read_list = except_file.readlines()
    for item in read_list:
        except_stack.append(item[:len(item)-1])
    except_file.close()
    #print except_stack

def init_package_file():
    package_file = open("package.txt", "r")
    read_list = package_file.readlines()
    package_file.close()
    for item in read_list:
        mktree(item[:len(item)-1])

def main():
    init_except_file()
    init_package_file()
    download("amd64")

if __name__ == '__main__':
    main()
