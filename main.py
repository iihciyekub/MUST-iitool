import iitool
import os
import re
import string
import inlp.convert.chinese as cv  # 简体转繁体库


if __name__ == "__main__":
    # 搜索本地 bib 文件
    bibFilePath = []
    for i, j, k in os.walk("."):
        for ii in k:
            if ".bib" in os.path.join(i, ii):
                bibFilePath.append(os.path.join(i, ii))
        # 得到格式化的 bib 文件
        bibFileStr = iitool.bibPyItem.allbibFileToStr(bibFilePath)

    # 将格式化的 bib 文本内容转成繁体
    bibFileStr = cv.s2t(bibFileStr)
    # 對文本進行預處理,(處理一些特殊字符)
    bibFileStr = bibFileStr.replace(r"&", r"\&")
    bibFileStr = bibFileStr.replace(r"_", r"\_")
    bibFileStr = bibFileStr.replace(r"%", r"\%")

    # 将 bib 的文本内容按 @ 符号进行分割
    bibItemStr = [i for i in bibFileStr.split("@")[1:]]
    #　將數據進行去重
    bibItemStr = list(set(bibItemStr))
    #　解析文本，從bib 文本中讀取到的內容並實例化 bibPyItem
    bibPyItem_Obj_List = [iitool.bibPyItem(i) for i in bibItemStr]
    # 按作者姓名進行排序
    bibItemList = sorted(bibPyItem_Obj_List,
                         key=lambda x: x.bibIndex, reverse=False)
    # 設置兩個開關,用於控制是否顯示中英文參考文獻的分隔標籤
    showzh, showwn = False, False
    # tex 文档中的缺省内容
    outPutbbl_H = r"""
    \begin{thebibliography}{}

    """
    # 中文分隔標籤
    tempC = r"""\bibitem[zh, 2019]{zh2019}{\fontsize{16pt}{\baselineskip}\selectfont{\it\bfseries 中文文獻}}

    """
    # tex 結尾詞
    outPutbbl_E = r"""\end{thebibliography}
    """
    # 英文分隔標籤
    tempE = r"""\bibitem[En, 2019]{en2019}{\fontsize{16pt}{\baselineskip}\selectfont{\it\bfseries 英文文獻}}

    """

    # 中文 & 英文 bibitem 的文本内容
    ToutputE, ToutputC = "", ""

    # 輸出中文參考文獻格式
    for i in bibItemList:
        if i.bibDict["lang"] == "chinese":
            ToutputC += i.bibStyle_mustAPA
    # 輸出英文參考文獻格式
    for i in bibItemList:
        if i.bibDict["lang"] != "chinese":
            ToutputE += i.bibStyle_mustAPA
    # 判斷是否有中文參考文獻
    showzh = ("bibitem" in ToutputC)
    # 判斷是否有英文參考文獻
    showen = ("bibitem" in ToutputE)
    # 中英文參考文獻共存
    t1 = showzh * showen

    # 輸出 tex 文本
    outputbbl = outPutbbl_H + tempC*t1 + ToutputC * \
        showzh + tempE*t1 + ToutputE * showen + outPutbbl_E

    # 保存 tex 文本到本地文件夹中
    with open("format/ref.tex", "w", encoding="utf-8") as f:
        f.write(outputbbl)

    # 清除辅助文件
    delcommand = "del  *.blg *.bbl *.aux *.log *.brf *.nlo *.out *.dvi *.ps *.lof *.toc *.fls *.fdb_latexmk *.pdfsync *.synctex*.gz *.ind *.ilg *.idx *.synctex(busy) *.pdf"
    # 初始化刪除掉不必要多餘的文件
    os.system(delcommand)

    # 搜索本地目錄 找到 tex 文件
    texfile = iitool.bibPyItem.findfile(suffix='tex')

    # 初次使用 xelatex 命令进行编译
    xelatexcommand = f"xelatex {texfile}"

    # xelatex 的方式進行第一次編譯
    os.system(xelatexcommand)

    # xelatex 的方式進行第二次編譯
    os.system(xelatexcommand)

    # 清除辅助文件
    delcommand = "del  *.blg *.bbl *.aux *.log *.brf *.nlo *.out *.dvi *.ps *.lof *.toc *.fls *.fdb_latexmk *.pdfsync *.synctex*.gz *.ind *.ilg *.idx *.synctex(busy) "
    os.system(delcommand)
