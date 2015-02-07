import os
import urllib
import xml.etree.ElementTree as ET
import ConfigParser as Config

from dc_common import *
from dc_Dep import *
from dc_Download import *

config = Config.ConfigParser()
config.read("config.ini")
url_head = config.get("Downloader", "url_head")
data_path = config.get("Data", "data_path")


class dc_DebList:

    def __init__(self):
        self.url = ""
        self.name = ""
        self.successed = "false"
        self.dependance = []
        self.dependance_url = []
        self.recommand = []
        self.recommand_url = []
        self.suggest = []
        self.suggest_url = []
        self.download_amd64_url = ""
        self.download_i386_url = ""

    def setup_by_url(self, url):
        content = get_content(url)
        if content == None:
            return

        print "Resovling url : " + self.url
        dep = dc_Dep()
        dep.feed(content)
        dep.close()

        for link in dep.dep_links:
            link_all = url_head + link
            self.dependance_url.append(link_all)
            self.dependance.append(get_deb_name_by_url(link_all))

        for link in dep.rec_links:
            link_all = url_head + link
            self.recommand_url.append(link_all)
            self.recommand.append(get_deb_name_by_url(link_all))

        for link in dep.sug_links:
            link_all = url_head + link
            self.suggest_url.append(link_all)
            self.suggest.append(get_deb_name_by_url(link_all))

        content = get_content(url_head + dep.download_amd64)
        if content == None:
            return
        download = dc_Download()
        download.feed(content)
        download.close()
        self.download_amd64_url = download.download_url

        content = get_content(url_head + dep.download_i386)
        if content == None:
            return
        download = dc_Download()
        download.feed(content)
        download.close()
        self.download_i386_url = download.download_url

        self.successed = "true"
        print "Finish dealing with url : " + self.url

    def init(self, mode, url="", name=""):
        if mode == "local":
            self.name = name
            path = data_path + self.name + ".xml"
            if os.path.isfile(path) == False:
                self.url = url
                self.setup_by_url(self.url)
                self.write(path)
                return
            self.dependance = []
            self.dependance_url = []
            tree = ET.parse(path)
            data = tree.getroot()
            self.url = data.find("name").text
            self.successed = data.find("successed").text
            if (self.successed == "false"):
                self.setup_by_url(self.url)
                self.write(path)
            else:
                self.download_i386_url = data.find("download_i386_url").text
                self.download_amd64_url = data.find("download_amd64_url").text
                dependance_list = data.find("dependance_list")
                for dep in dependance_list.findall("dependance"):
                    self.dependance.append(dep.find("dependance_name").text)
                    self.dependance_url.append(dep.find("dependance_url").text)
                recommand_list = data.find("recommand_list")
                for rec in recommand_list.findall("recommand"):
                    self.recommand.append(rec.find("recommand_name").text)
                    self.recommand_url.append(rec.find("recommand_url").text)
                suggest_list = data.find("suggest_list")
                for sug in suggest_list.findall("suggest"):
                    self.suggest.append(sug.find("suggest_name").text)
                    self.suggest_url.append(sug.find("suggest_url").text)
        else:
            self.url = url
            self.name = get_deb_name_by_url(self.url)
            self.setup_by_url(self.url)
            self.write()

    def write(self, path=""):
        if path == "":
            path = data_path + self.name + ".xml"
        file_output = open(path, "w")
        file_output.write('<?xml version="1.0"?>\n<data>\n</data>')
        file_output.close()

        tree = ET.parse(path)
        data = tree.getroot()
        successed = ET.SubElement(data, "successed")
        successed.text = self.successed
        if self.successed == "false":
            tree.write(path)
            return

        name = ET.SubElement(data, "name")
        name.text = self.name
        url = ET.SubElement(data, "url")
        url.text = self.url
        download_amd64_url = ET.SubElement(data, "download_amd64_url")
        download_amd64_url.text = self.download_amd64_url
        download_i386_url = ET.SubElement(data, "download_i386_url")
        download_i386_url.text = self.download_i386_url

        dep_list = ET.SubElement(data, "dependance_list")
        i = 0
        for dep_name_str in self.dependance:
            dep_item = ET.SubElement(dep_list, "dependance")
            dep_name = ET.SubElement(dep_item, "dependance_name")
            dep_name.text = dep_name_str
            dep_url = ET.SubElement(dep_item, "dependance_url")
            dep_url.text = self.dependance_url[i]
            i = i + 1

        dep_list = ET.SubElement(data, "recommand_list")
        i = 0
        for dep_name_str in self.recommand:
            dep_item = ET.SubElement(dep_list, "recommand")
            dep_name = ET.SubElement(dep_item, "recommand_name")
            dep_name.text = dep_name_str
            dep_url = ET.SubElement(dep_item, "recommand_url")
            dep_url.text = self.recommand_url[i]
            i = i + 1

        dep_list = ET.SubElement(data, "suggest_list")
        i = 0
        for dep_name_str in self.suggest:
            dep_item = ET.SubElement(dep_list, "suggest")
            dep_name = ET.SubElement(dep_item, "suggest_name")
            dep_name.text = dep_name_str
            dep_url = ET.SubElement(dep_item, "suggest_url")
            dep_url.text = self.suggest_url[i]
            i = i + 1

        tree.write(path)
