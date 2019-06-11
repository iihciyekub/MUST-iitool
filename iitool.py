# coding:utf-8
# author:YJ.Li 2019-06-11
# version:0.0.2.0
# bib -> Dict -> bbl -> pdf | iitool.exe
###########

import os
import re
import string
import inlp.convert.chinese as cv  # 简体转繁体库

tempDic = """一,乙,二,丁,十,七,人,入,八,九,匕,刁,了,乃,刀,力,又,三,土,士,工,才,下,寸,丈,大,上,小,口,山,巾,千,乞,川,丸,久,凡,勺,及,夕,亡,丫,之,己,已,巳,弓,子,也,女,刃,叉,王,井,天,夫,元,丐,木,五,支,不,太,犬,友,尤,歹,匹,巨,牙,屯,戈,比,互,切,瓦,止,少,日,曰,中,內,水,午,手,牛,毛,壬,升,夭,仁,什,片,仇,化,仍,斤,爪,戶,反,介,父,今,凶,分,乏,公,勻,月,氏,勿,欠,丹,勾,六,文,亢,方,火,冗,心,尺,引,孔,巴,以,允,予,幻,玉,刊,未,末,示,打,巧,正,卉,扒,功,扔,去,甘,世,艾,古,本,可,丙,左,右,石,布,夯,戊,平,卡,北,凸,占,且,旦,目,叮,甲,申,田,由,只,叭,史,央,兄,叼,叩,叫,另,叨,冉,冊,皿,凹,囚,四,生,失,矢,乍,禾,丘,付,仗,代,仙,白,仔,他,斥,瓜,乎,令,用,甩,印,句,匆,卯,犯,外,冬,包,主,市,立,玄,半,汁,穴,它,必,永,司,尼,民,弗,弘,出,奶,奴,加,召,皮,孕,台,矛,母,幼,邦,丟,式,迂,刑,戎,扛,寺,吉,扣,托,考,老,圾,地,耳,芋,共,芒,芝,朽,臣,吏,再,西,戌,在,有,百,存,而,匠,灰,列,死,成,夷,邪,至,此,尖,劣,光,早,吐,曲,同,吊,吃,因,吸,吆,屹,帆,回,肉,年,朱,先,廷,舌,竹,迄,乒,乓,休,伍,伏,臼,伐,延,仲,件,任,份,仰,仿,自,伊,血,向,似,行,舟,全,合,兆,企,肌,肋,朵,危,旨,旬,旭,匈,各,名,多,色,冰,亦,交,次,衣,亥,充,妄,羊,米,州,汗,汙,江,汛,池,汝,忙,宇,守,宅,字,安,那,迅,弛,收,防,奸,如,妃,好,她,羽,巡,弄,玖,形,戒,吞,扶,技,扼,拒,找,批,址,扯,走,抄,汞,攻,赤,折,抓,扳,扮,孝,坎,均,抑,投,坑,抗,坊,抖,志,扭,把,抒,劫,芙,芽,花,芹,芥,芬,芳,芯,克,芭,杆,杜,杠,材,村,杖,杏,杉,巫,李,求,車,甫,匣,更,束,吾,豆,酉,辰,否,夾,尬,步,肖,旱,盯,呈,貝,見,助,呆,吱,吠,呀,足,男,困,吵,串,呐,呂,吟,吩,別,吻,吹,吭,吳,吧,吼,邑,囤,吮,刪,牡,告,我,利,禿,秀,私,每,兵,估,何,佐,佑,但,伸,佃,作,伯,伶,低,你,住,位,伴,身,皂,伺,佛,囪,近,役,返,希,兌,坐,妥,含,岔,肝,肚,肛,肘,甸,免,狂,角,彤,卵,灸,刨,迎,系,言,床,庇,吝,冷,序,辛,冶,忘,判,灶,灼,弟,汪,沐,沛,汰,沙,沖,汽,沃,泛,沒,沈,沉,沁,決,忱,快,完,宋,宏,牢,究,良,初,社,祀,罕,君,即,屁,尿,尾,局,改,忌,阿,壯,妝,阻,附,妓,妙,妖,姊,妨,妒,努,忍,矣,災,奉,玩,武,青,玫,表,抹,長,卦,坷,坯,拓,拔,拋,坪,坦,坤,押,抽,拐,拖,拍,者,拆,拎,抵,拘,抱,拄,垃,拉,幸,拌,拂,拙,招,坡,披,抬,亞,拇,拗,其,取,茉,苦,昔,苛,若,茂,苗,英,苟,苑,苞,直,茁,茄,苔,茅,枉,林,枝,杯,枚,析,板,來,松,杭,述,枕,軋,東,或,臥,事,刺,兩,雨,協,矽,奈,奔,奇,妻,到,非,叔,歧,肯,些,卓,虎,尚,旺,具,味,果,昆,哎,咕,昌,門,呵,明,易,昂,迪,典,固,忠,呻,咒,咋,咐,呼,呢,咄,咖,岸,岩,帖,帕,岡,制,知,迭,氛,垂,牧,物,乖,刮,和,季,委,秉,佳,侍,供,使,例,兒,版,侄,佩,侈,依,卑,的,迫,欣,征,往,爬,彼,所,舍,金,刹,侖,命,肴,斧,爸,采,受,爭,乳,念,忿,肺,肢,朋,股,肮,肪,肥,服,周,昏,兔,狐,忽,狗,京,享,店,夜,府,底,疙,疚,卒,郊,庚,盲,放,刻,於,育,氓,券,卷,並,炬,炒,炊,炕,炎,沫,法,泄,沽,河,沾,沮,油,況,泊,沿,泡,注,泣,泌,泳,泥,沸,沼,波,治,怔,怯,怖,性,怕,怪,怡,宗,定,宜,宙,官,空,宛,郎,肩,房,衫,祈,建,帚,屆,居,刷,屈,弧,弦,承,孟,陋,狀,陌,孤,降,函,限,妹,姑,姐,姓,妮,始,姆,迢,糾,契,奏,春,玷,珍,玲,珊,玻,毒,型,拭,封,持,拷,拱,垮,挎,城,政,赴,拽,哉,挺,括,垢,拴,拾,挑,垛,指,拼,挖,按,挪,拯,某,甚,荊,茸,革,茬,巷,草,茵,茶,荒,茫,故,胡,荔,南,茲,柑,枯,柄,查,相,柵,柏,柳,柱,柿,勃,軌,要,柬,威,歪,研,頁,厘,厚,砌,砂,泵,砍,面,耐,耍,殃,皆,勁,韭,背,貞,虐,省,削,昧,盹,是,則,盼,眨,哇,哄,冒,映,星,昨,咧,昭,畏,趴,胃,界,虹,思,品,咽,咱,哈,哆,咬,咳,咪,哪,炭,骨,幽,卸,缸,拜,看,矩,怎,牲,秒,香,秋,科,重,竿,段,便,俠,修,俏,保,促,侶,俄,俐,侮,俗,俘,信,皇,泉,鬼,侵,禹,侯,帥,追,俊,盾,待,徊,衍,律,很,後,逃,卻,食,盆,胚,胞,胖,胎,負,勉,風,狡,狠,怨,急,訂,計,哀,亭,亮,度,庭,疫,疤,姿,音,帝,施,差,美,叛,送,迷,籽,前,首,逆,炸,炮,炫,剃,為,洪,柒,洞,洗,活,派,洽,染,洶,洛,洋,洲,津,恃,恒,恢,恍,恬,恤,恰,恨,宣,宦,室,突,穿,客,冠,軍,扁,祖,神,祝,祠,退,既,屍,屋,屏,屎,陡,陣,眉,陝,孩,除,院,娃,姥,姨,姻,姚,娜,怒,架,飛,盈,勇,怠,癸,蚤,柔,紅,約,級,紀,紉,耕,耘,耗,耙,泰,秦,珠,班,素,匿,匪,栽,捕,埂,捂,馬,振,挾,起,捎,捍,捏,貢,埋,捉,捆,捐,袁,捌,都,哲,逝,挫,挽,恐,捅,埃,挨,耿,耽,恥,華,恭,莽,莖,莫,莉,荷,真,莊,框,梆,桂,桔,桐,株,栓,桃,格,校,核,根,索,軒,連,哥,速,逗,栗,酌,配,翅,辱,唇,夏,砸,砰,破,原,套,逐,烈,殊,殉,致,晉,鬥,柴,桌,時,逞,畢,財,眠,哮,晃,哺,閃,晌,剔,蚌,畔,蚣,蚊,蚪,蚓,哨,員,哩,圃,哭,哦,恩,唁,哼,唧,啊,唉,唆,豈,峽,峭,峨,峰,峻,剛,缺,氧,氣,氨,特,郵,造,乘,秤,租,秧,秩,秘,透,笑,借,值,倆,倚,俺,倒,條,倘,俱,們,倡,個,候,倫,俯,倍,倦,健,臭,射,躬,息,島,烏,倔,師,徒,徑,徐,殷,般,航,途,釘,針,殺,拿,爹,舀,豺,豹,倉,翁,胰,脈,脆,脂,胸,胳,逛,狹,狽,狸,狼,卿,逢,留,討,訓,這,訊,記,凍,衰,畝,衷,高,郭,席,庫,准,座,症,病,疾,疹,疼,疲,脊,效,紊,唐,瓷,站,剖,部,旁,旅,畜,羞,羔,瓶,拳,粉,料,益,兼,烤,烘,烙,浙,浦,酒,涉,消,浩,海,浴,浮,流,涕,浪,浸,悖,悟,悄,悍,悔,悅,害,家,宵,宴,宮,窄,容,宰,案,朗,扇,袖,袍,被,祥,冥,冤,書,展,屑,弱,陸,陵,陳,孫,祟,陰,陶,陷,陪,娟,恕,娛,娥,娘,脅,通,能,務,桑,剝,純,紗,納,紛,紙,紋,紡,紐,球,責,現,理,琉,琅,規,捧,掛,堵,措,描,域,捺,掩,捷,排,焉,掉,捶,赦,堆,推,頂,埠,掀,掄,授,掙,教,掏,掐,掠,掂,培,接,執,控,探,掃,掘,基,聆,勘,聊,娶,著,菱,萊,勒,菲,萌,菌,萎,菜,萄,菊,菩,萍,菠,乾,菇,械,彬,婪,梗,梧,梢,梅,麥,梳,梯,桶,梭,紮,救,斬,軟,專,曹,副,區,堅,票,酗,戚,帶,奢,盔,爽,盛,匾,雪,頃,鹵,彪,處,雀,堂,常,眶,匙,晨,敗,販,貶,眯,眼,野,啪,啦,啞,閉,問,婁,曼,晦,晚,啄,啡,異,距,趾,啃,略,蚯,蛀,蛇,唬,累,鄂,唱,國,患,唾,唯,啤,啥,帳,崖,崎,眾,崗,崔,帷,崩,崇,崛,圈,過,氫,甜,秸,梨,犁,移,動,笨,笛,笙,符,第,敏,做,袋,偵,悠,側,偶,偎,偷,您,貨,售,進,停,偽,偏,鳥,兜,假,偉,術,徘,徙,得,從,舶,船,舵,敘,斜,釣,盒,悉,欲,彩,覓,貪,貧,脖,脯,豚,脫,魚,象,逸,猜,凰,猖,猙,猛,夠,祭,訝,許,訛,訟,設,訪,訣,毫,烹,庶,麻,庵,產,痊,痕,廊,康,庸,鹿,章,竟,商,族,旋,望,率,牽,羚,眷,粘,粗,粒,剪,焊,清,添,淩,淋,涯,淹,淒,渠,淺,淑,淌,混,渦,淮,淪,淆,淫,淨,淘,涼,淳,液,淤,淡,淚,深,涮,涵,婆,梁,情,惜,悼,惕,惟,惦,悴,惋,寇,寅,寄,寂,宿,窒,密,啟,袱,視,晝,逮,敢,尉,屠,屜,張,強,隋,將,蛋,階,陽,隅,隆,隊,婚,婉,婦,習,參,貫,鄉,組,紳,細,終,絆,紹,巢,貳,琴,琳,琢,斑,替,揍,款,堯,堪,塔,搭,堰,揀,堿,項,揩,越,趁,超,堤,提,場,揚,博,揭,喜,彭,揣,插,揪,搜,塊,煮,援,換,裁,達,搓,報,揮,壹,殼,壺,握,搔,揉,惡,斯,期,欺,黃,葉,葫,散,惹,葬,募,萬,葛,董,葡,敬,蒂,落,葷,朝,喪,辜,葦,葵,棒,棱,棋,椰,植,森,焚,棟,椅,棲,棧,椒,棵,棍,椎,棉,棚,棕,棺,榔,極,軸,惠,惑,逼,腎,粟,棗,棘,酣,酥,硬,硝,硯,硫,雁,殖,殘,裂,雄,雲,雅,悲,紫,虛,敞,棠,掌,晴,暑,最,晰,量,貼,貯,貽,鼎,喳,閏,開,閑,晶,間,悶,喇,遇,喊,遏,景,晾,跋,跌,跑,跛,貴,蛙,蛛,蜓,蜒,蛤,喝,喂,單,喘,喉,喻,喚,啼,喧,喲,嵌,幅,凱,買,帽,黑,圍,甥,無,掰,短,智,毯,氮,氯,剩,稍,稈,程,稀,稅,喬,筐,等,策,筒,筏,答,筋,筍,筆,傲,備,傅,牌,貸,順,堡,傑,集,焦,傍,皓,皖,街,循,須,艇,舒,鈣,鈍,鈔,鈉,欽,鈞,鈕,逾,番,爺,傘,禽,創,飯,飲,脹,脾,腋,勝,腔,腕,猩,猾,猴,猶,然,貿,評,詐,訴,診,詠,詞,馮,就,敦,廂,廁,斌,痘,痢,痛,童,竣,遊,棄,善,翔,普,尊,奠,道,遂,曾,焰,勞,湊,港,湖,渣,湘,渤,減,渺,測,湯,渴,滑,湃,淵,渝,渙,盜,渡,滋,渲,渾,溉,湧,慌,惰,愕,愣,惶,愧,愉,慨,惱,割,寒,富,寓,窖,窗,窘,甯,運,遍,雇,補,裡,裕,裙,禍,祿,尋,畫,犀,費,粥,疏,違,韌,隔,隙,隕,隘,媒,絮,嫂,媚,婿,賀,登,發,綁,絨,結,給,絢,絡,絞,統,絕,絲,幾,瑟,瑞,瑰,瑙,頑,魂,肆,摸,填,載,搏,馱,馴,馳,塌,損,遠,鼓,搗,搬,勢,搶,搖,搞,塘,聖,聘,斟,蒜,蓋,勤,蓮,靴,靶,墓,幕,夢,蒼,蓬,蓄,蒲,蓉,蒙,幹,蔭,蒸,椿,禁,楚,楷,楊,想,槐,榆,楓,概,較,賈,酪,酬,感,碘,碑,碎,碰,碗,碌,匯,電,雷,零,雹,頓,盞,督,歲,虜,業,當,睛,睹,睦,瞄,睞,睫,睡,賊,賄,賂,睬,睜,嗎,嗜,嘩,鄙,嗦,閘,愚,暖,盟,歇,暗,暈,暇,號,照,畸,跨,跳,跺,跪,路,跡,跤,跟,園,遣,蜈,蛾,蛻,蜂,農,嗅,嗚,嗆,嗡,嗓,署,置,罪,罩,蜀,幌,圓,矮,稚,稠,愁,筷,節,與,債,僅,傳,毀,舅,鼠,傾,催,賃,傷,傻,像,傭,躲,魁,粵,奧,衙,遞,微,鉗,鉀,鈴,鉛,鉤,愈,會,愛,亂,飾,飽,飼,頒,頌,腰,腸,腥,腮,腫,腹,腺,腳,腿,腦,猿,獅,解,遙,煞,試,詩,誇,誠,話,誕,詭,詢,該,詳,稟,廈,痹,廓,痰,廉,資,靖,新,意,義,羨,煎,塑,慈,煤,煙,煉,煩,煌,煥,溝,漠,滇,滅,源,溫,滌,塗,滔,溪,滄,溜,漓,溢,溯,溶,溺,粱,慎,塞,寞,窩,窟,褂,裸,福,肅,群,殿,辟,裝,遜,際,障,媽,媳,嫉,嫌,嫁,預,經,絹,剿,瑪,瑣,碧,璃,熬,摳,駁,趙,趕,墟,摟,嘉,摧,赫,截,誓,境,摘,摔,墊,撇,壽,摻,聚,慕,暮,摹,蔓,蔑,蔥,蔔,蔡,蔗,蔽,熙,蔚,兢,蔣,構,樺,模,槍,榴,榜,榨,榕,輔,輕,歌,遭,監,緊,酵,酷,酸,厲,碟,厭,碩,碳,磁,爾,奪,需,雌,對,嘗,裳,夥,瞅,墅,暢,閨,聞,閩,閥,閣,嗽,嘔,蜻,蝸,蜘,團,鳴,嘛,嘀,嶄,嶇,罰,圖,舞,舔,種,稱,熏,箕,算,箏,管,僥,僚,僕,僑,僧,鼻,魄,魅,銜,銬,銅,鋁,銘,銀,貌,餌,蝕,餃,餅,領,膜,膊,膀,鳳,疑,獄,孵,誡,誣,語,誤,誘,誨,說,認,誦,裹,敲,豪,膏,廣,遮,麼,腐,瘩,瘧,瘟,瘦,瘓,瘋,塵,辣,彰,竭,端,適,齊,旗,養,精,鄰,粹,鄭,歉,弊,幣,熄,榮,熒,熔,煽,漢,滿,漆,漸,漱,漂,滯,漫,漁,滾,滴,漾,演,滬,漏,漲,滲,慚,慢,慷,慘,慣,寨,寬,賓,寡,窪,察,蜜,寢,寥,實,肇,褐,複,褪,劃,盡,屢,墮,隨,墜,隧,嫩,頗,翠,熊,態,凳,鄧,緒,綽,綱,網,維,綿,綢,綜,綻,綴,綠,慧,撓,墳,撕,撒,駛,駒,駐,駝,撩,趣,趟,撲,撐,撮,賣,撫,撬,熱,播,擒,鞏,撚,墩,撞,撤,摯,增,撈,穀,撰,撥,歎,鞋,鞍,邁,蕪,蕉,蕩,蕊,蔬,樁,槽,樞,標,樓,橡,樟,樣,橄,橢,輛,暫,輪,敷,歐,毆,豎,賢,豌,遷,醋,醇,醉,碼,磕,磊,憂,磅,確,碾,遼,豬,震,霄,鴉,輩,鬧,齒,劇,膚,慮,輝,賞,暴,賦,賬,賭,賤,賜,賠,瞎,噴,嘻,嘶,嘲,閱,數,嘹,影,踐,踢,踏,踩,遺,蝶,蝴,蝠,蝟,蝌,蝗,蝙,蝦,嘿,嘮,嘰,罵,罷,幢,幟,墨,靠,稽,稻,黎,稿,稼,箱,範,箭,篇,僵,價,儉,億,儀,躺,樂,僻,質,德,徹,衛,艘,盤,鋪,銷,鋤,銳,鋒,鋅,劍,貓,餓,餘,餒,膝,膛,膠,魯,劉,皺,請,諸,諾,誹,課,誰,論,調,諒,諄,談,誼,熟,廚,廟,摩,褒,廠,瘡,瘤,慶,廢,凜,毅,敵,糊,遵,導,憋,瑩,潔,澆,澎,潮,潭,潛,潤,澗,潰,澳,潘,澈,澇,澄,潑,憤,懂,憫,憔,懊,憐,憎,寫,審,窮,窯,翩,褥,褲,憨,慰,遲,劈,履,層,彈,選,槳,獎,漿,險,嬌,駕,豫,練,緬,緝,緞,線,緩,締,編,緯,緣,靜,駱,駭,撼,擂,據,擋,操,擇,撿,擔,壇,擅,擁,薑,燕,蕾,薯,薛,薇,擎,薦,薪,薄,翰,蕭,噩,薩,樹,橫,樸,橋,橙,橘,機,輻,輯,輸,整,賴,融,頭,瓢,醒,醜,勵,磚,曆,奮,頰,霍,霎,頸,冀,頻,餐,盧,瞞,縣,曉,鴨,閻,噸,嘴,踱,蹄,踴,蹂,螞,蟆,螃,器,戰,噪,鴦,嘯,還,嶼,默,黔,積,穆,頹,勳,築,篡,篩,篷,舉,興,學,憊,儒,鴕,邀,衡,艙,錯,錨,錢,錫,鋼,鍋,錘,錐,錦,鍵,鋸,錳,錄,墾,餡,館,膩,膨,雕,鮑,獲,穎,獨,鴛,謀,諜,謊,諧,謂,諷,諮,諺,謎,諱,憑,磨,瘸,凝,親,辨,辦,龍,劑,糙,糖,糕,燒,燃,螢,營,燈,燙,濃,澡,澤,濁,激,澱,憾,懈,憶,憲,窺,窿,禪,壁,避,隱,縛,縫,環,贅,幫,駿,趨,擱,戴,擬,擴,擠,擲,擦,擰,聲,藉,聰,聯,艱,鞠,藍,藏,舊,藐,韓,隸,檬,檔,檢,檀,轄,輾,擊,臨,醞,壓,礁,磷,尷,霜,霞,戲,虧,瞭,顆,瞧,購,嬰,賺,瞬,瞳,瞪,嚇,闊,曙,蹋,蹈,螺,蟋,蟀,雖,嚎,嶺,嶽,點,矯,穗,魏,簧,簍,簇,繁,輿,優,償,儲,龜,徽,禦,聳,鍬,鍛,鍍,斂,鴿,爵,懇,朦,膿,臊,臉,膽,謄,鮮,獰,講,謝,謠,謗,謙,氈,應,療,癌,齋,糟,糞,糠,斃,燦,燥,燭,鴻,濤,濫,濕,濟,濱,濘,澀,懦,豁,賽,襖,禮,臀,臂,彌,牆,翼,績,縷,繃,總,縱,縮,瓊,攆,翹,騎,擾,擺,聶,藕,職,藝,鞭,繭,藥,藤,櫃,檻,檸,轉,覆,醫,礎,霧,豐,叢,題,瞻,闖,曠,蹦,蹤,壘,蟲,蟬,鵑,鵝,穢,簡,雙,軀,邊,歸,鎮,鏈,鎖,鎬,鎊,翻,雞,饃,餾,臍,鯉,鯽,獵,雛,謹,謬,顏,雜,離,糧,濾,鯊,瀑,濺,瀏,瀉,竄,竅,額,襟,禱,璧,醬,嬸,戳,繞,繚,織,斷,鵡,騙,騷,壞,攏,難,鵲,蘋,蘆,勸,孽,蘇,警,藹,蘑,藻,顛,蘊,攀,櫥,轎,轍,麗,礙,礦,願,贈,曝,關,疇,蹺,蹲,蹭,蹬,蠅,蠍,蟻,嚴,獸,嚨,羅,贊,穩,簸,簽,簷,簾,簿,簫,懲,鏡,鏟,辭,饅,鵬,臘,鯨,蟹,譚,識,譜,證,譏,靡,廬,癟,癡,癢,龐,瓣,壟,韻,羹,類,爆,爍,瀟,瀝,瀕,懶,懷,寵,襪,疆,繩,繹,繳,繪,繡,攔,攙,壤,馨,蘭,礬,飄,礫,齡,鹹,獻,耀,黨,懸,贍,闡,躁,蠕,嚼,嚷,巍,犧,籍,籌,籃,譽,覺,艦,鐘,釋,饒,饋,饑,朧,騰,觸,護,譴,譯,議,魔,辮,競,贏,糯,爐,灌,瀾,寶,譬,響,繽,繼,蠢,攝,驅,騾,攜,歡,權,櫻,欄,轟,覽,殲,霸,露,霹,贓,躍,蠟,囂,黯,髒,髓,鐵,鐺,鐮,鏽,鰭,癮,辯,爛,鶯,懼,顧,襯,鶴,屬,續,纏,攤,驕,聽,韁,蘿,驚,囊,鷗,鑒,贖,疊,囉,巔,邏,體,籠,鑄,讀,巒,彎,瓤,顫,癬,聾,襲,鱉,灘,灑,竊,驗,攪,曬,顯,罐,黴,鱗,變,戀,纖,鬢,攬,驟,壩,觀,矗,鹽,釀,靂,靈,蠶,囑,籬,讓,鷹,癱,贛,欖,顱,籮,鑰,鑲,饞,蠻,廳,灣,驢,矚,躪,釁,鑼,鑽,鱷,纜,豔,鑿,鸚,鬱,籲,\\,A,B,C,D,E,F,G,H,I,
J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z"""


# 用于参考文献作者排序的字典
tempDic = [i for i in tempDic.split(",")]
gDic = dict(enumerate(tempDic))


# 创建 bibPyItem 类
class bibPyItem:
    global gDic

    def __init__(self, bibitemStr):
        '''
        初始化
        '''
        self.bibitemStr = cv.s2t(bibitemStr)
        self.__bibTex = ""
        self.__bibPyIndex = -1
        self.__bibDict = {"bibType": "", "citelabel": "",
                          "author": "", "editor": "", "title": "",
                          "journal": "", "volume": "", "number": "",
                          "pages": "", "chapter": "", "institution": "",
                          "year": "", "school": "", "university": "",
                          "location": "", "publisher": "", "booktitle": "",
                          "issn": "", "doi": "", "type": "",
                          "organization": "", "url": "", "note": "",
                          "description": "", "date": ""}
        self.__to_bibDict()

    @property
    def bibPyIndex(self):
        """
        返回一个作者名的排序号
        """
        return self.__bibPyIndex

    @property
    def bibDict(self):
        self.__to_bibDict()
        return self.__bibDict

    @property
    def bibTex_APAsty(self):
        self.__to_bblTEX_APAsty()
        return self.__bibTex


    # 私有方法
    def __to_bibDict(self, P=1):
        '''
        bibitemStr:对 bib 文件读取且按@分割完成的文本内容进行解析,返回一个字典
        P:1->表示简体转繁体
        '''
        bibitemStr = self.bibitemStr
        # 简体转繁体
        if P == 1:
            bibitemStr = cv.s2t(bibitemStr)
        for i in self.__bibDict.keys():
            y = re.findall(i+".*?{(.*?)}", bibitemStr, re.I)
            self.__bibDict[i] = ("" if y == [] else y[0])

        # 提取 bibitem中的 引用标签字符串
        x = bibitemStr.split(",")[0].split("{")
        self.__bibDict["bibType"] = x[0].strip().lower()
        self.__bibDict["citelabel"] = x[1].strip()
        zhmodel = re.compile(u'[\u4e00-\u9fa5]')
        if self.__bibDict["author"] != "":

            match = zhmodel.search(self.__bibDict["author"])
            self.__bibDict["lang"] = ('chinese' if match else "")
        else:
            match = zhmodel.search(self.__bibDict["title"])
            self.__bibDict["lang"] = ('chinese' if match else "")

        # 排序的实现
        if self.__bibDict["author"] == "":
            tag = self.__bibDict["title"][0].upper()
        else:
            tag = self.__bibDict["author"][0].upper()
        if tag in tempDic:
            self.__bibPyIndex = list(gDic.keys())[
                list(gDic.values()).index(tag)]


    # 私有方法
    def __to_bblTEX_APAsty(self):
        if self.__bibDict['lang'] == 'chinese':
            self.__chParser()
        else:
            self.__enParser()


    # 解析英文类 bib
    def __enParser(self):
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

        # 出現在參考文獻中的作者信息
        refauthor = authorlist[0] if authorlist[0] != "" else "Null"
        if len(authorlist) >= 2:
            if len(authorlist) >= 8:
                for j in authorlist[1:5]:
                    refauthor += ", "
                    refauthor += j
                refauthor += ",..."
            elif len(authorlist) >= 3:
                for j in authorlist[1:-1]:
                    refauthor += ", "
                    refauthor += j
            refauthor += r", \& "
            refauthor += authorlist[-1]

        #　----------------------------------------->>
        self.__bibTex = ""
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
                    self.__bibTex += (r"{\em (" +
                                      self.__bibDict['number'] + r")}")
            # 判斷是否存在頁碼
            if self.__bibDict["pages"] != "":
                self.__bibTex += f", {self.__bibDict['pages']}"
            self.__bibTex += "."
            if self.__bibDict["doi"] != "":
                self.__bibTex = self.__bibTex + f" doi:{self.__bibDict['doi']}"
            self.__bibTex += "\n\n"

        # type II  ------->>online

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
                self.__bibTex += (self.__bibDict["title"]+",(")
                self.__bibTex += (date + "), Retrieved from ")
                self.__bibTex += self.__bibDict["url"]
            else:
                self.__bibTex += (self.__bibDict["author"]+"(")
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


    # 解析中文类 bib
    def __chParser(self):
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
        # 出現在參考文獻中的作者信息
        refauthor = authorlist[0]
        if len(authorlist) >= 2:
            if len(authorlist) >= 8:
                for j in authorlist[1:6]:
                    refauthor += "、"
                    refauthor += j
                refauthor += "、…"
            elif len(authorlist) >= 3:
                for j in authorlist[1:-1]:
                    refauthor += "、"
                    refauthor += j
            refauthor += "與"
            refauthor += authorlist[-1]

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
                    f" doi:{self.__bibDict['doi'] }"
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
        elif self.__bibDict["bibType"]in ["online"]:
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
                self.__bibTex += (self.__bibDict["title"]+"。(")
                self.__bibTex += (date + ")。取自 ")
                self.__bibTex += self.__bibDict["url"]
            else:
                self.__bibTex += (self.__bibDict["author"]+"(")
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




# 讀取 bib 文件,返回str
def allbibFileToStr(bibfilePath):
        '''
        方法:将所有 bib 文件的内容进行格式化并读取出来,返回文本
        bibfilePath: 包含 bib 文件的路径.str & list
        '''
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
                            bibFileStr = bibFileStr[:-2]+"\n"
                    bibFileStr += (temp+"\n")
                    if not a:
                        break
            # 处理@字段与新行起写的问题
            bibFileStr = bibFileStr.replace("}@", "}\n@")
        # 返回所有 bib 文件的文本內容
        return bibFileStr




# 搜索指定目录下指定后缀的文件
def findfile(path=r"", suffix="tex"):
    '''
    path: 值='/reference' 表示搜索目录下reference文件夹
    suffix:文件后缀名
    '''
    dirs = f".{path}"
    # 判断目录是否存在
    if not os.path.exists(dirs):
        print(f".{path} 文件夹不存在!!!!")
    else:
        # 读取该文件夹下的文件
        reffile = os.listdir(f'.{path}')

    # 过滤掉不是bib后缀的文件
    xfile = list(filter(lambda x: suffix in x, reffile))
    return xfile[0]



if __name__ == "__main__":
    # 搜索本地 bib 文件
    bibFilePath = []
    for i, j, k in os.walk("."):
        for ii in k:
            if ".bib" in os.path.join(i, ii):
                bibFilePath.append(os.path.join(i, ii))
        # 得到格式化的 bib 文件
        bibFileStr = allbibFileToStr(bibFilePath)

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
    bibPyItem_Obj_List = [bibPyItem(i) for i in bibItemStr]
    # 按作者姓名進行排序 
    bibItemList = sorted(bibPyItem_Obj_List,
                         key=lambda x: x.bibPyIndex, reverse=False)
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
            ToutputC += i.bibTex_APAsty
    # 輸出英文參考文獻格式
    for i in bibItemList:
        if i.bibDict["lang"] != "chinese":
            ToutputE += i.bibTex_APAsty
    #判斷是否有中文參考文獻
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
    texfile = findfile(suffix='tex')

    # 初次使用 xelatex 命令进行编译
    xelatexcommand = f"xelatex {texfile}"

    # xelatex 的方式進行第一次編譯
    os.system(xelatexcommand)

    # xelatex 的方式進行第二次編譯
    os.system(xelatexcommand)

    # 清除辅助文件
    delcommand = "del  *.blg *.bbl *.aux *.log *.brf *.nlo *.out *.dvi *.ps *.lof *.toc *.fls *.fdb_latexmk *.pdfsync *.synctex*.gz *.ind *.ilg *.idx *.synctex(busy) "
    os.system(delcommand)