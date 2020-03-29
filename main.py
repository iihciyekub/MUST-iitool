# coding:utf-8
# author:YJ.Li 2019-07-06
# version:0.0.2.6
##
# bib -> Dict -> bbl -> pdf | iitool.exe
import iitool
import os
import inlp.convert.chinese as cv  # 简体转繁体库

if __name__ == "__main__":

    filepath = ""
    bibFilePath = []
    bibFileStr = ""

    # 搜索所有 tex 文本,将文本内容全转为繁体
    for i, j, k in os.walk("."):
        for ii in k:
            temPath = os.path.join(i, ii)
            # 如果找到 tex 后缀的文件
            if ".tex" in temPath:
                filepath = temPath
                with open(filepath, "r+", encoding="utf-8") as f:
                    # 读取全文
                    temp = f.read()
                    # 全文转繁体
                    temp = cv.s2t(temp)
                    # 全文重写到文件中
                    f.seek(0)
                    f.truncate()
                    f.write(temp)
            # 如果找到 bib 后缀的文件        
            elif ".bib" in temPath:
                bibFilePath.append(temPath)

    # 得到格式化的 bib 文件
    bibFileStr = iitool.BIBPYITEM.allbibFileToStr(bibFilePath)

    # 将格式化的 bib 文本内容转成繁体
    bibFileStr = cv.s2t(bibFileStr)
    # 對文本進行預處理,(處理一些特殊字符)
    bibFileStr = bibFileStr.replace(r"&", r"\&")
    bibFileStr = bibFileStr.replace(r"_", r"\_")
    bibFileStr = bibFileStr.replace(r"%", r"\%")

    # 将 bib 的文本内容按 @ 符号进行分割
    bibItemStr = [i for i in bibFileStr.split("@")[1:]]
    # 將數據進行去重
    bibItemStr = list(set(bibItemStr))
    # 解析文本，從bib 文本中讀取到的內容並實例化 bibPyItem
    bibPyItem_Obj_List = [iitool.BIBPYITEM(i) for i in bibItemStr]
    # 按作者姓名進行排序
    bibItemList = sorted(bibPyItem_Obj_List,
                         key=lambda x: x.bibIndex, reverse=False)
    # 設置兩個開關,用於控制是否顯示中英文參考文獻的分隔標籤
    showZH = False
    showEN = False
    # tex 文档中的缺省内容
    outPutBBL_H = r"""
    \begin{thebibliography}{}

    """
    # 中文分隔標籤
    tempC = r"""\bibitem[zh, 2019]{zh2019}{\fontsize{16pt}{\baselineskip}\selectfont{\it\bfseries 中文文獻}}

    """
    # tex 結尾詞
    outPutBBL_E = r"""\end{thebibliography}
    """
    # 英文分隔標籤
    tempE = r"""\bibitem[En, 2019]{en2019}{\fontsize{16pt}{\baselineskip}\selectfont{\it\bfseries 英文文獻}}

    """

    # 中文 & 英文 bibitem 的文本内容
    ToutPutE, ToutPutC = "", ""

    # 輸出中文參考文獻格式
    for i in bibItemList:
        if i.bibDict["lang"] == "chinese":
            ToutPutC += i.bibStyle_mustAPA
    # 輸出英文參考文獻格式
    for i in bibItemList:
        if i.bibDict["lang"] != "chinese":
            ToutPutE += i.bibStyle_mustAPA
    # 判斷是否有中文參考文獻
    showZH = ("bibitem" in ToutPutC)
    # 判斷是否有英文參考文獻
    showEN = ("bibitem" in ToutPutE)
    # 中英文參考文獻共存
    t1 = showZH * showEN

    # 輸出 tex 文本
    outPutBBL = outPutBBL_H + tempC * t1 + ToutPutC * showZH + tempE * t1 + ToutPutE * showEN + outPutBBL_E

    # 保存 tex 文本到本地文件夹中
    dirs = "{0}/format".format(os.getcwd())
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    with open("format/ref.tex", "w", encoding="utf-8") as f:
        f.write(outPutBBL)

    # 清除辅助文件
    delCommand = "del  *.blg *.bbl *.aux *.log *.brf *.nlo *.out *.dvi *.ps *.lof *.toc *.fls *.fdb_latexmk *.pdfsync *.synctex*.gz *.ind *.ilg *.idx *.synctex(busy) *.pdf"
    # 初始化刪除掉不必要多餘的文件
    os.system(delCommand)

    # 搜索本地目錄 找到 tex 文件
    texFile = iitool.BIBPYITEM.findFile(suffix='tex')

    # 初次使用 xelatex 命令进行编译
    xelatexCommand = f"xelatex {texFile}"

    # xelatex 的方式進行第一次編譯
    os.system(xelatexCommand)

    # xelatex 的方式進行第二次編譯
    os.system(xelatexCommand)

    # 清除辅助文件
    delCommand = r"del  *.blg *.bbl *.aux *.log *.brf *.nlo *.out *.dvi *.ps *.lof *.toc *.fls *.fdb_latexmk *.pdfsync *.synctex*.gz *.ind *.ilg *.idx *.synctex(busy) "
    os.system(delCommand)
