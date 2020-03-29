# coding:utf-8
# author:YJ.Li 2019-06-17
# version:0.0.2.0
##
# bib -> Dict -> bbl -> pdf | iitool.exe


import os
import re
import inlp.convert.chinese as cv  # 简体转繁体库
import refTextDict


# 创建 bibPyItem 类
class BIBPYITEM:
    # 用于参考文献作者排序的字典
    gDic = refTextDict.refDic

    def __init__(self, bibItemStr, style="mustAPA"):
        """
        初始化
        """
        self.gDic = ""
        # 初始化时传入的字符转繁体
        self.bibitemStr = cv.s2t(bibItemStr)
        # 表示 bib文件中每一个item 格式后的文本
        self.__bibTex = ""
        # 表示参考文献的序号
        self.__bibIndex = -1
        # bib 字典
        self.__bibDict = {"bibType": "", "citelabel": "",
                          "author": "", "editor": "", "title": "",
                          "journal": "", "volume": "", "number": "",
                          "pages": "", "chapter": "", "institution": "",
                          "year": "", "school": "", "university": "",
                          "location": "", "publisher": "", "booktitle": "",
                          "issn": "", "doi": "", "type": "",
                          "organization": "", "url": "", "note": "",
                          "description": "", "date": ""}

        # 初始化执行 转字典 方法
        self.__to_bibDict()
        # 获取作者姓名序号
        self.__getbibIndex()
        # 默认参考文献样式为　MUST　APA
        if style == "mustAPA":
            self.__to_bibStyle_mustAPA()
        else:
            pass  # to do

    @property
    def bibIndex(self):
        """
        返回一个作者名的排序号
        """
        return self.__bibIndex

    @property
    def bibDict(self):
        """
        返回格式后的 bibPyItem 字典
        """
        return self.__bibDict

    @property
    def bibStyle_mustAPA(self):
        """
        获取已转换化mustAPA格式的参考文献文本
        """
        return self.__bibTex

    def __to_bibDict(self, P=1):
        """
        私有方法
        方法:对已按@分割后的 bib 文本内容进行解析 \n
        返回值:bibItem字典\n
        参数:P=1(表示简体转繁体)P=0(表示不转换)
        """
        bibitemStr = self.bibitemStr
        # 简体转繁体
        if P == 1:
            bibitemStr = cv.s2t(bibitemStr)
        for i in self.__bibDict.keys():
            y = re.findall(i + ".*?{(.*?)}", bibitemStr, re.I)
            self.__bibDict[i] = ("" if y == [] else y[0])

        # 提取 bibitem中的 引用标签字符串
        x = bibitemStr.split(",")[0].split("{")
        self.__bibDict["bibType"] = x[0].strip().lower()
        self.__bibDict["citelabel"] = x[1].strip()
        # re 判断是否包含中文
        zhmodel = re.compile(u'[\u4e00-\u9fa5]')
        if self.__bibDict["author"] != "":
            match = zhmodel.search(self.__bibDict["author"])
            self.__bibDict["lang"] = ('chinese' if match else "")
        else:
            match = zhmodel.search(self.__bibDict["title"])
            self.__bibDict["lang"] = ('chinese' if match else "")

    def __getbibIndex(self):
        """
        私有方法
        按作者姓排序的实现
        """
        if self.__bibDict["author"] == "":
            tag = self.__bibDict["title"][0].upper()
        else:
            tag = self.__bibDict["author"][0].upper()
        if tag in BIBPYITEM.gDic.values():
            self.__bibIndex = list(BIBPYITEM.gDic.keys())[
                list(BIBPYITEM.gDic.values()).index(tag)]

    def __to_bibStyle_mustAPA(self):
        """
        私有方法
        返回MUST APA Style 的格式化 bbl 文本
        """
        if self.__bibDict['lang'] == 'chinese':
            self.__chParser()
        else:
            self.__enParser()

    def __enParser(self):
        """
        英文类 bibItem 解析器
        """
        self.__bibTex = ""
        # 對 pd 格式的數據進行處理
        authorlist = [si.strip().title()
                      for si in self.__bibDict["author"].split(" and ")]

        # 出現在正文中的引用標籤作者名
        citeauthor = authorlist[0].split(",")[0] if authorlist[0].split(",")[
                                                        0] != "" else "Null"
        if len(authorlist) >= 3:
            citeauthor += " et al."
        elif len(authorlist) == 2:
            citeauthor += r" \& "
            citeauthor += authorlist[1].split(",")[0]
        
        # 定义一个方法用于处理英文名
        def fun(name):
            n = name.strip()
            if "," in n:
                n = n.replace(",", " ")
                n = n.strip()
            if " " in n:
                a = [i for i in n.split(" ") if i != ""]
                b = a[0] + ","
                for ne in a[1:]:
                    b += ne[0].upper() + '.'
                n = b
            return n
        # 出現在參考文獻中的作者信息
        refauthor = authorlist[0] if authorlist[0] != "" else "Null"
        # 取出第一位作者的信息
        refauthor = fun(refauthor)
        counts_author=len(authorlist)
        if counts_author >= 7:
            for j in authorlist[1:6]:
                js = fun(j)
                refauthor += ", "
                refauthor += js.strip()
            refauthor += ", et al"
        elif counts_author >= 3 and counts_author <= 6:
            if counts_author > 2:
                for j in authorlist[1:-1]:
                    js = fun(j)
                    refauthor += ", "
                    refauthor += js
            refauthor += r", \& "
            refauthor += fun(authorlist[-1])
    

        # type I  ------->>普通文章类
        if self.__bibDict["bibType"] in ["article", "misc", "manual"]:
            # 格式化文本
            self.__bibTex += (r"\bibitem[" + citeauthor + ", ")
            self.__bibTex += (self.__bibDict["year"] + r"]{")
            self.__bibTex += (self.__bibDict["citelabel"] + "}\n")
            self.__bibTex += (refauthor +
                              r" (" + self.__bibDict["year"] + ").\n")
            self.__bibTex += (r"\newblock " +
                              self.__bibDict["title"].capitalize())

            #  判斷是否存在期刊名
            if self.__bibDict["journal"] != "":
                self.__bibTex += (".\n" +
                                  r"\newblock {\em " + self.__bibDict['journal'] + r"}")

            if self.__bibDict["number"] != "" or self.__bibDict["volume"] != "":
                self.__bibTex += ", "
                if self.__bibDict["volume"] != "":
                    self.__bibTex += (r"{\em " +
                                      self.__bibDict["volume"] + r"}")
                # 判斷是否存卷,卷號
                if self.__bibDict["number"] != "":
                    self.__bibTex += (r"(" +
                                      self.__bibDict['number'] + r")")
            # 判斷是否存在頁碼
            if self.__bibDict["pages"] != "":
                self.__bibTex += f", {self.__bibDict['pages']}"
            self.__bibTex += "."
            if self.__bibDict["doi"] != "":
                self.__bibTex = self.__bibTex + f" doi:{self.__bibDict['doi']}"
            self.__bibTex += "\n\n"

        elif self.__bibDict["bibType"] in ["online"]:
            endate = {
                1: "January",
                2: "February",
                3: "March",
                4: "April",
                5: "May",
                6: "June",
                7: "July",
                8: "August",
                9: "September",
                10: "October",
                11: "November",
                12: "December"
            }
            if self.__bibDict["date"] != "":
                date = self.__bibDict["date"].split("-")
                if len(date) == 3:
                    date = f"{date[0]},{endate[int(date[2])]} {date[1]}"
                elif len(date) == 2:
                    date = f"{date[0]},{endate[int(date[2])]}"
                elif len(date) == 1:
                    date = f"{date[0]}"
            else:
                date = "n.d."
            self.__bibTex += (r"\bibitem[" +
                              self.__bibDict["citelabel"] + ", ")
            self.__bibTex += (date + r"]{")
            self.__bibTex += (self.__bibDict["citelabel"] + "}\n")
            if self.__bibDict["author"] == "":
                self.__bibTex += (self.__bibDict["title"] + ",(")
                self.__bibTex += (date + "), Retrieved from ")
                self.__bibTex += self.__bibDict["url"]
            else:
                self.__bibTex += (self.__bibDict["author"] + "(")
                self.__bibTex += (date + ")[" +
                                  self.__bibDict["description"] + "]." + self.__bibDict["title"])
                self.__bibTex += (", Retrieved from " + self.__bibDict["url"])
            self.__bibTex += "\n\n"

        # type II  ------->>畢業論文
        elif self.__bibDict["bibType"] in ["thesis", "phdthesis", "mastersthesis"]:
            self.__bibTex += (r"\bibitem[" + citeauthor + ", ")
            self.__bibTex += (self.__bibDict["year"] + r"]{")
            self.__bibTex += (self.__bibDict["citelabel"] + "}\n")
            self.__bibTex += (refauthor +
                              r" (" + self.__bibDict["year"] + ").\n")
            self.__bibTex += r"\newblock {\em "
            self.__bibTex += self.__bibDict["title"].capitalize() + "}."

            if self.__bibDict["bibType"] == "phdthesis":
                self.__bibTex += " Doctoral dissertation"
            elif self.__bibDict["bibType"] == "mastersthesis":
                self.__bibTex += " Master dissertation"
            elif self.__bibDict["bibType"] == "thesis":
                self.__bibTex += " Dissertation"
            # 判断是否存在学校信息
            if self.__bibDict["school"] != "":
                self.__bibTex += (", " + self.__bibDict["school"])
            elif self.__bibDict["university"] != "":
                self.__bibTex += (", " + self.__bibDict["university"])
            self.__bibTex += ".\n\n"

        #
        elif self.__bibDict["bibType"] in ["proceedings", "inproceedings", "conference"]:
            self.__bibTex += (r"\bibitem[" + citeauthor + ", ")
            self.__bibTex += (self.__bibDict["year"] + r"]{")
            self.__bibTex += (self.__bibDict["citelabel"] + "}\n")
            self.__bibTex += (refauthor +
                              r" (" + self.__bibDict["year"] + ").\n")
            self.__bibTex += r"\newblock "
            self.__bibTex += self.__bibDict["title"].capitalize()
            # 判断会议是否存在
            if self.__bibDict["organization"] != "":
                self.__bibTex += (". " + self.__bibDict["organization"])
            if self.__bibDict["pages"] != "":
                self.__bibTex += (" (pp. " + self.__bibDict["pages"] + ")")
            # 判断是否存在出版社
            if self.__bibDict["location"] != "" and self.__bibDict["publisher"] != "":
                self.__bibTex += (". " +
                                  self.__bibDict["location"] + ":" + self.__bibDict["publisher"])
            elif self.__bibDict["location"] != "":
                self.__bibTex += (". " + self.__bibDict["location"])
            elif self.__bibDict["publisher"] != "":
                self.__bibTex += (". " + self.__bibDict["publisher"])
            self.__bibTex += ".\n\n"

        # type III  ------->>书籍类
        elif self.__bibDict["bibType"] in ["book", "booklet"]:
            self.__bibTex += (r"\bibitem[" + citeauthor + ", ")
            self.__bibTex += (self.__bibDict["year"] + r"]{")
            self.__bibTex += (self.__bibDict["citelabel"] + "}\n")
            self.__bibTex += (refauthor +
                              r" (" + self.__bibDict["year"] + ").\n")
            self.__bibTex += r"\newblock {\em "
            self.__bibTex += self.__bibDict["title"].capitalize() + "}"
            # 判断是否存在出版社
            if self.__bibDict["location"] != "" and self.__bibDict["publisher"] != "":
                self.__bibTex += (". " +
                                  self.__bibDict["location"] + ":" + self.__bibDict["publisher"])
            elif self.__bibDict["location"] != "":
                self.__bibTex += (". " + self.__bibDict["location"])
            elif self.__bibDict["publisher"] != "":
                self.__bibTex += (". " + self.__bibDict["publisher"])
            self.__bibTex += ".\n\n"
        # type III  ------->>书籍类
        elif self.__bibDict["bibType"] in ["inbook"]:
            self.__bibTex += (r"\bibitem[" + citeauthor + ", ")
            self.__bibTex += (self.__bibDict["year"] + r"]{")
            self.__bibTex += (self.__bibDict["citelabel"] + "}\n")
            self.__bibTex += (refauthor +
                              r" (" + self.__bibDict["year"] + ").\n")
            self.__bibTex += r"\newblock  "
            self.__bibTex += self.__bibDict["booktitle"].capitalize()
            if self.__bibDict["editor"] != "":
                self.__bibTex += (". In " +
                                  self.__bibDict["editor"] + " (Ed.)")
            self.__bibTex += (r", {\em " +
                              self.__bibDict["title"].capitalize() + r"}")
            if self.__bibDict["pages"] != "":
                self.__bibTex += (" (pp. " + self.__bibDict["pages"] + ")")
            # 判断是否存在出版社
            if self.__bibDict["location"] != "" and self.__bibDict["publisher"] != "":
                self.__bibTex += (". " + self.__bibDict["editor"] +
                                  ": " + self.__bibDict["publisher"])
            elif self.__bibDict["location"] != "":
                self.__bibTex += (". " + self.__bibDict["location"])
            elif self.__bibDict["publisher"] != "":
                self.__bibTex += (". " + self.__bibDict["publisher"])
            self.__bibTex += ".\n\n"

    def __chParser(self):
        """
        # 解析中文类 bib
        """
        self.__bibTex = ""
        if "and" in self.__bibDict["author"]:
            authorlist = [si.strip()
                          for si in self.__bibDict["author"].split(" and ")]
        elif "," in self.__bibDict["author"]:
            authorlist = [si.strip()
                          for si in self.__bibDict["author"].split(" , ")]
        else:
            authorlist = [self.__bibDict["author"]]
        # 出現在正文中的引用標籤作者名
        citeauthor = authorlist[0]
        if len(authorlist) >= 3:
            citeauthor += "等人"
        elif len(authorlist) == 2:
            citeauthor += "與"
            citeauthor += authorlist[1]
        # ---- 出現在參考文獻中的作者信息
        # 取出第一位作者的信息
        refauthor = authorlist[0]
        counts_author=len(authorlist)
        if counts_author >= 7:
            # 如果作者数量大于6位时
            for j in authorlist[1:6]:
                refauthor += "、"
                refauthor += j.strip()
            refauthor += "等人"
        elif counts_author >= 2 and counts_author <= 6:
        #     if counts_author > 2:
            for j in authorlist:
                refauthor += "、"
                refauthor += j


        # type ------->>普通文章类
        if self.__bibDict["bibType"] in ["article", "misc", "manual"]:
            # 格式化文本
            self.__bibTex += (r"\bibitem[" + citeauthor + ", ")
            self.__bibTex += (self.__bibDict["year"] + r"]{")
            self.__bibTex += (self.__bibDict["citelabel"] + "}\n")
            self.__bibTex += (refauthor + r"（" +
                              self.__bibDict["year"] + "）。\n")
            self.__bibTex += (r"\newblock " + self.__bibDict["title"])
            #  判斷是否存在期刊名
            if self.__bibDict["journal"] != "":
                self.__bibTex += "。\n"
                self.__bibTex += r"\newblock \textbf{" + \
                                 self.__bibDict["journal"] + r"}"
            if self.__bibDict["number"] != "" or self.__bibDict["volume"] != "":
                self.__bibTex += "，"
                if self.__bibDict["volume"] != "":
                    self.__bibTex += (r"\textbf{" +
                                      self.__bibDict["volume"] + r"}")
                # 判斷是否存卷,卷號
                if self.__bibDict["number"] != "":
                    self.__bibTex += (r"\textbf{(" +
                                      self.__bibDict["number"] + r")}")
            # 判斷是否存在頁碼
            if self.__bibDict["pages"] != "":
                self.__bibTex += f"，{self.__bibDict['pages']}"
            self.__bibTex += "。"
            if self.__bibDict["doi"] != "":
                self.__bibTex = self.__bibTex + \
                                f" doi:{self.__bibDict['doi']}"
            self.__bibTex += "\n\n"

        # type ------->>畢業論文
        elif self.__bibDict["bibType"] in ["thesis", "phdthesis", "mastersthesis"]:
            self.__bibTex += (r"\bibitem[" + citeauthor + ", ")
            self.__bibTex += (self.__bibDict["year"] + r"]{")
            self.__bibTex += (self.__bibDict["citelabel"] + "}\n")
            self.__bibTex += (refauthor +
                              r" (" + self.__bibDict["year"] + ")。\n")
            self.__bibTex += r"\newblock \textbf{"
            self.__bibTex += self.__bibDict["title"] + "}。"
            if self.__bibDict["bibType"] == "phdthesis":
                self.__bibTex += "博士論文"
            elif self.__bibDict["bibType"] == "mastersthesis":
                self.__bibTex += "碩士論文"
            elif self.__bibDict["bibType"] == "thesis":
                self.__bibTex += "論文"
            # 判断是否存在学校信息
            if self.__bibDict["school"] != "":
                self.__bibTex += ("，" + self.__bibDict["school"])
            elif self.__bibDict["university"] != "":
                self.__bibTex += ("，" + self.__bibDict["university"])
            self.__bibTex += "。\n\n"

        # type ------->>online
        elif self.__bibDict["bibType"] in ["online"]:
            if self.__bibDict["date"] != "":
                date = self.__bibDict["date"].split("-")
                if len(date) == 3:
                    date = f"{date[0]}年{date[1]}月{date[2]}日"
                elif len(date) == 2:
                    date = f"{date[0]}年{date[1]}月"
                elif len(date) == 1:
                    date = f"{date[0]}年"
            else:
                date = "无日期"
            self.__bibTex += (r"\bibitem[" +
                              self.__bibDict["citelabel"] + ", ")
            self.__bibTex += (date + r"]{")
            self.__bibTex += (self.__bibDict["citelabel"] + "}\n")
            if self.__bibDict["author"] == "":
                self.__bibTex += (self.__bibDict["title"] + "。(")
                self.__bibTex += (date + ")。取自 ")
                self.__bibTex += self.__bibDict["url"]
            else:
                self.__bibTex += (self.__bibDict["author"] + "(")
                self.__bibTex += (date + ")【" +
                                  self.__bibDict["description"] + "】。" + self.__bibDict["title"])
                self.__bibTex += ("。取自 " + self.__bibDict["url"])
            self.__bibTex += "\n\n"

        # type ------->> 会议论文
        elif self.__bibDict["bibType"] in ["proceedings", "inproceedings", "conference"]:
            self.__bibTex += (r"\bibitem[" + citeauthor + ", ")
            self.__bibTex += (self.__bibDict["year"] + r"]{")
            self.__bibTex += (self.__bibDict["citelabel"] + "}\n")
            self.__bibTex += (refauthor +
                              r" (" + self.__bibDict["year"] + ")。\n")
            self.__bibTex += r"\newblock "
            self.__bibTex += self.__bibDict["title"]
            # 判断会议是否存在
            if self.__bibDict["organization"] != "":
                self.__bibTex += self.__bibDict["organization"]
            if self.__bibDict["pages"] != "":
                self.__bibTex += ("（頁 " + self.__bibDict["pages"] + "）")
            # 判断是否存在出版社
            if self.__bibDict["location"] != "" and self.__bibDict["publisher"] != "":
                self.__bibTex += ("。" + self.__bibDict["location"] +
                                  "：" + self.__bibDict["publisher"])
            elif self.__bibDict["location"] != "":
                self.__bibTex += ("。" + self.__bibDict["location"])
            elif self.__bibDict["publisher"] != "":
                self.__bibTex += ("。" + self.__bibDict["publisher"])
            self.__bibTex += "。\n\n"

        # type ------->>图书类
        elif self.__bibDict["bibType"] in ["book", "booklet"]:
            self.__bibTex += (r"\bibitem[" + citeauthor + ", ")
            self.__bibTex += (self.__bibDict["year"] + r"]{")
            self.__bibTex += (self.__bibDict["citelabel"] + "}\n")
            self.__bibTex += (refauthor + r"（" +
                              self.__bibDict["year"] + "）。\n")
            self.__bibTex += r"\newblock \textbf{ "
            self.__bibTex += self.__bibDict["title"] + "}"
            # 判断是否存在出版社
            if self.__bibDict["location"] != "" and self.__bibDict["publisher"] != "":
                self.__bibTex += ("。" + self.__bibDict["location"] +
                                  "：" + self.__bibDict["publisher"])
            elif self.__bibDict["location"] != "":
                self.__bibTex += ("。" + self.__bibDict["location"])
            elif self.__bibDict["publisher"] != "":
                self.__bibTex += ("。" + self.__bibDict["publisher"])
            self.__bibTex += "。\n\n"

        # type ------->>书籍类
        elif self.__bibDict["bibType"] in ["inbook"]:
            self.__bibTex += (r"\bibitem[" + citeauthor + ", ")
            self.__bibTex += (self.__bibDict["year"] + r"]{")
            self.__bibTex += (self.__bibDict["citelabel"] + "}\n")
            self.__bibTex += (refauthor + r"（" +
                              self.__bibDict["year"] + "）。\n")
            self.__bibTex += r"\newblock  "
            self.__bibTex += self.__bibDict["booktitle"]
            if self.__bibDict["editor"] != "":
                if " and " in self.__bibDict["editor"]:
                    xx = (self.__bibDict["editor"].split(
                        " and ")[0].strip() + "等人")
                elif "," in self.__bibDict["editor"]:
                    xx = (self.__bibDict["editor"].split(
                        ",")[0].strip() + "等人")
                else:
                    xx = self.__bibDict["editor"]
                self.__bibTex += ("載於" + xx + "（主編）")
            self.__bibTex += (r"，\textbf{" + self.__bibDict["title"] + r"}")
            if self.__bibDict["pages"] != "":
                self.__bibTex += ("（頁 " + self.__bibDict["pages"] + "）")
            # 判断是否存在出版社
            if self.__bibDict["location"] != "" and self.__bibDict["publisher"] != "":
                self.__bibTex += ("。" + self.__bibDict["editor"] +
                                  ": " + self.__bibDict["publisher"])
            elif self.__bibDict["location"] != "":
                self.__bibTex += ("。" + self.__bibDict["location"])
            elif self.__bibDict["publisher"] != "":
                self.__bibTex += ("。" + self.__bibDict["publisher"])
            self.__bibTex += "。\n\n"

    @staticmethod
    def allbibFileToStr(bibfilePath):
        """
        方法:将所有 bib 文件的内容进行格式化并读取出来,返回文本
        bibfilePath: 包含 bib 文件的路径.str & list
        """
        bibFileStr = ""
        # 如果 bibfilePath 參數為 str 時,則處理為 list 類型
        if type(bibfilePath) == type(""):
            bibfilePath = [bibfilePath]

        # 讀取所有 bib 文件的內容
        for refF in bibfilePath:
            with open(refF, 'r', encoding="UTF-8") as f:
                while 1:
                    # 逐行读取
                    a = f.readline()
                    # 去除空行
                    if a == '\n':
                        continue
                    # 去除两边空格
                    temp = a.strip()
                    if temp == None:
                        continue
                    # 如果該行包含 = ,就在前面加個 tab 個縮進
                    if "=" in temp:
                        temp = "\t" + temp
                    # 处理最后一条数据包含逗号的情况
                    if temp == "}":
                        if bibFileStr[-2] == ",":
                            bibFileStr = bibFileStr[:-2] + "\n"
                    bibFileStr += (temp + "\n")
                    if not a:
                        break
            # 处理@字段与新行起写的问题
            bibFileStr = bibFileStr.replace("}@", "}\n@")
        # 返回所有 bib 文件的文本內容
        return bibFileStr

    @staticmethod
    def findFile(path=r"", suffix="tex"):
        """
        path: 值='/reference' 表示搜索目录下reference文件夹
        suffix:文件后缀名
        """
        dirs = f".{path}"
        # 判断目录是否存在
        if not os.path.exists(dirs):
            print(f".{path} 文件夹不存在!!!!")
        else:
            # 读取该文件夹下的文件
            reffile = os.listdir(f'.{path}')
        # 过滤掉不是 suffix 后缀的文件
        xfile = list(filter(lambda x: suffix in x, reffile))
        rfile = ""
        for i in xfile:
            with open(i, "r", encoding="utf-8") as f:
                flinetext = f.read()
                if r"\documentclass" in flinetext:
                    rfile = i
                    break
                else:
                    continue
        return rfile
