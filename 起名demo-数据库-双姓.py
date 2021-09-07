# -*- coding: utf-8 -*-
from OwnTools.mysql import OperationMysql
import sxtwl
import bazi_postil
import random
from pypinyin import pinyin
import opencc
from collections import defaultdict
import re
from loguru import logger
import ngender
import json
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ShX = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
numCn = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
jqmc = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露",
        "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"]
ymc = ["十一", "十二", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
rmc = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九",
       "二十", "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"]
dict_wuxing = {'甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土', '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水',
               '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火', '午': '火', '未': '土', '申': '金', '酉': '金',
               '戌': '土', '亥': '水'}


class QiMing:
    def __init__(self):
        self.mysql = OperationMysql("qiming", type=2)
        self.s2t = opencc.OpenCC("s2t")  # 简体转繁体
        self.t2s = opencc.OpenCC("t2s")  # 繁体转简体
        self.lunar = sxtwl.Lunar()
        self.summarys = bazi_postil.summarys
        self.baijiaxing_sancaiwuge_dict = self.getBaijiaxingData()
        self.wuxing_luck_bad = self.get_wuxing_luck_bad()
        self.wuxing_strokes = self.chines_infos()
        self.sancai_strokes = self.get_sancai_strokes()

    def get_wuxing_luck_bad(self):
        temp = {}
        search_datas = self.mysql.select_mysql_many("sancai_luck_bad", "sancai,luck_bad,introduce,overvies",
                                                    " where 1=1")
        for sd in search_datas:
            temp[sd[0]] = {
                "luck_bad": sd[1],
                "overvies": sd[3],
                "introduce": sd[2]
            }

        return temp

    def get_sancai_strokes(self):
        search_datas = self.mysql.select_mysql_many("sancai_infos", "number,parse,other,status",
                                                    " where 1=1")
        sancai_strokes = {}
        for sd in search_datas:
            sancai_strokes[sd[0]] = {
                "parse": sd[1],
                "other": sd[2],
                "status": sd[3],
            }

        return sancai_strokes

    def chines_infos(self):
        search_datas = self.mysql.select_mysql_many("chinese_infos", "word,wuxing,strokes,common_use,introduce",
                                                    " where 1=1")
        chinese_infos = {
            "金": {0: {}},
            "木": {0: {}},
            "水": {0: {}},
            "火": {0: {}},
            "土": {0: {}},
        }
        for sd in search_datas:
            chinese_infos[sd[1]][0][sd[0]] = {
                "strokes": sd[2],
                "introduce": sd[4]
            }
            if sd[2] not in chinese_infos[sd[1]].keys():
                chinese_infos[sd[1]][sd[2]] = {"y": [], "n": []}
                if sd[3] == "y":
                    chinese_infos[sd[1]][sd[2]]["y"].append(sd[0])
                else:
                    chinese_infos[sd[1]][sd[2]]["n"].append(sd[0])
            else:
                if sd[3] == "y":
                    chinese_infos[sd[1]][sd[2]]["y"].append(sd[0])
                else:
                    chinese_infos[sd[1]][sd[2]]["n"].append(sd[0])

        return chinese_infos

    # 判断是否为汉字
    def is_chinese(self, uchar):
        if u'\u4e00' <= uchar <= u'\u9fa5':
            return True
        else:
            return False

    def get_stroke_number(self, word):
        stroke = 0
        for k in self.wuxing_strokes.keys():
            if word in self.wuxing_strokes[k][0].keys():
                stroke = self.wuxing_strokes[k][0][word]["strokes"]
        if stroke == 0:
            logger.error(f"获取【{word}】笔画数错误")
            with open("无法获取笔画的汉字.txt", "a") as f:
                f.write(f"【{word}】失败\n")
        return stroke

    # 获取对应五行
    def get_wuxing(self, count, types=1):
        count = count % 10
        wuxing = ""
        if count == 1 or count == 2:
            wuxing = "木"
        elif count == 3 or count == 4:
            wuxing = "火"
        elif count == 5 or count == 6:
            wuxing = "土"
        elif count == 7 or count == 8:
            wuxing = "金"
        elif count == 9 or count == 0:
            wuxing = "水"
        if types != 1:
            if count in [1, 3, 5, 7, 9]:
                return f"(阳){wuxing}"
            else:
                return f"(阴){wuxing}"
        else:
            return wuxing

    def getBaijiaxingData(self):
        """
        百家姓以及第二字和第三字笔画数最佳搭配
        另一个版本可以参考 http://www.360doc.com/content/18/0414/14/4153217_745576219.shtml
        """
        temp = {}
        search_datas = self.mysql.select_mysql_many("BaiJiaXing", "xing,bast_match_number",
                                                    " where 1=1 and bast_match_number is not NULL")
        for sd in search_datas:

            temp[sd[0]] = []
            for s in sd[1].split("|"):
                slist = s.split(",")
                temp[sd[0]].append((int(slist[0]), int(slist[1])))
        return temp

    def get_good_number(self, start_nub, min_nub=0, max_nub=0):
        good_nub = {
            "good": [],
            "general": []
        }
        stroke_goods = [1, 3, 5, 8, 11, 13, 15, 16, 21, 23, 24, 25, 29, 31, 32, 33, 35, 37, 38, 39, 41, 45, 47, 48, 52,
                        57, 63, 65, 67, 68, 81]
        stroke_generals = [6, 7, 17, 18, 27, 30, 40, 51, 52, 55, 61, 75]
        for sg in stroke_goods:
            deal_nub = int(sg) - start_nub
            if deal_nub > 0:
                if min_nub != 0 and max_nub != 0:
                    if min_nub <= deal_nub <= max_nub:
                        good_nub["good"].append(deal_nub)
                else:
                    good_nub["good"].append(deal_nub)
        for sg in stroke_generals:
            deal_nub = int(sg) - start_nub
            if deal_nub > 0:
                if min_nub != 0 and max_nub != 0:
                    if min_nub <= deal_nub <= max_nub:
                        good_nub["general"].append(deal_nub)
                else:
                    good_nub["general"].append(deal_nub)
            good_nub["general"].append(deal_nub)
        return good_nub

    def shengcheng_infos(self, sc_info):
        years, months, days, hours = sc_info[0], sc_info[1], sc_info[2], sc_info[3]
        # 八字信息
        day = self.lunar.getDayBySolar(years, months, days)
        bazi_year = "{}{}".format(Gan[day.Lyear2.tg], Zhi[day.Lyear2.dz])
        bazi_month = "{}{}".format(Gan[day.Lmonth2.tg], Zhi[day.Lmonth2.dz])
        bazi_day = "{}{}".format(Gan[day.Lday2.tg], Zhi[day.Lday2.dz])
        if day.Lleap:
            yinli = f"润 {bazi_year}年{ymc[day.Lmc]}月{rmc[day.Ldi]}日"
        else:
            yinli = f"{bazi_year}年{ymc[day.Lmc]}月{rmc[day.Ldi]}日"
        gz = self.lunar.getShiGz(day.Lday2.tg, hours)
        month = sxtwl.Lunar().yueLiCalc(years, months)
        bazi_hour = "{}{}".format(Gan[gz.tg], Zhi[gz.dz])

        # 五行信息
        bazi = f"{bazi_year}{bazi_month}{bazi_day}{bazi_hour}"
        wuxing = []
        for i in range(8):
            # print({bazi[i]: dict_wuxing[bazi[i]]})
            wuxing.append(dict_wuxing[bazi[i]])

        j = wuxing.count('金')
        m = wuxing.count('木')
        s = wuxing.count('水')
        h = wuxing.count('火')
        t = wuxing.count('土')
        # print('初始八字五行分布：')
        wuxing1 = {'金': j, '木': m, '水': s, '火': h, '土': t}

        # 木生火,火生土,土生金,金生水,水生木
        h_s = m
        t_s = h
        j_s = t
        s_s = j
        m_s = s
        # 金克木,木克土,土克水,水克火,火克金
        m_k = j
        t_k = m
        s_k = t
        h_k = s
        j_k = h
        # 最终
        j_z = j + j_s - j_k
        m_z = m + m_s - m_k
        s_z = s + s_s - s_k
        h_z = h + h_s - h_k
        t_z = t + t_s - t_k
        # print('结合相生相克之后五行分布：')
        wuxing2 = {'金': j_z, '木': m_z, '水': s_z, '火': h_z, '土': t_z}
        tiaozheng = ""
        if j_z <= 0:
            j = j + 1
            tiaozheng = '金'
        if m_z <= 0:
            m = m + 1
            tiaozheng = '木'
        if s_z <= 0:
            s = s + 1
            tiaozheng = '水'
        if h_z <= 0:
            h = h + 1
            tiaozheng = '火'
        if t_z <= 0:
            t = t + 1
            tiaozheng = '土'
        # print('调整之后五行分布：')
        wuxing3 = {'金': j, '木': m, '水': s, '火': h, '土': t}

        # 木生火,火生土,土生金,金生水,水生木
        h_s = m
        t_s = h
        j_s = t
        s_s = j
        m_s = s

        # 金克木,木克土,土克水,水克火,火克金
        m_k = j
        t_k = m
        s_k = t
        h_k = s
        j_k = h
        # 最终
        j_z = j + j_s - j_k
        m_z = m + m_s - m_k
        s_z = s + s_s - s_k
        h_z = h + h_s - h_k
        t_z = t + t_s - t_k

        # print('调整结合相生相克之后五行分布：')
        wuxing4 = {'金': j_z, '木': m_z, '水': s_z, '火': h_z, '土': t_z}

        # 批注
        introduce = random.choice(self.summarys[f"{Gan[day.Lday2.tg]}日{bazi_hour}"]["intorduce"])

        bazi_pizhu = "{}{}".format(f"{bazi_day}日{bazi_hour}时",
                                   self.summarys[f"{Gan[day.Lday2.tg]}日{bazi_hour}"]["info"][
                                       f"{bazi_day}日{bazi_hour}时"])

        return {
            "Calendar": f"{years}年{months}月{days}日 {hours}点",
            "Zodiac": ShX[month.ShX],
            "lunar": f"{yinli}{Zhi[gz.dz]}时",
            "Week": f"星期{numCn[day.week]}",
            "Bazi": f"{bazi_year} {bazi_month} {bazi_day} {bazi_hour}",
            "wuxing": wuxing,
            "start_wuxing": wuxing1,
            "fenbu_wuxing": wuxing2,
            "revise_wuxing": tiaozheng,
            "revise_later_wuxing": wuxing3,
            "end_wuxing": wuxing4,
            "bazi_introduce": introduce,
            "bazi_pizhu": bazi_pizhu,
        }

    def get_hz_wuxing(self, name, stroke):
        for k in self.wuxing_strokes.keys():
            if stroke in self.wuxing_strokes[k] and name in self.wuxing_strokes[k][0].keys():
                return k
        return self.get_wuxing(self.get_stroke(name))

    def get_stroke(self, c):
        # 如果返回 0, 则也是在unicode中不存在kTotalStrokes字段
        strokes = []
        with open("data/strokes.txt", 'r') as fr:
            for line in fr:
                strokes.append(int(line.strip()))
        unicode_ = ord(c)
        if 13312 <= unicode_ <= 64045:
            return strokes[unicode_ - 13312]
        elif 131072 <= unicode_ <= 194998:
            return strokes[unicode_ - 80338]
        else:
            print("c should be a CJK char, or not have stroke in unihan data.")
            # can also return 0

    def getLastNameWuge(self, first_name):
        # print(self.baijiaxing_sancaiwuge_dict)
        if first_name in self.baijiaxing_sancaiwuge_dict:
            return self.baijiaxing_sancaiwuge_dict[first_name]
        else:
            return []

    # 获取三才配置
    def get_sancai_config(self, counts):
        config = ""
        for count in counts:
            config += self.get_wuxing(count)
        return config

    def get_stroke_type(self, stroke):
        if stroke > 81:
            stroke = 81 % 10
        if stroke in self.sancai_strokes.keys():
            return self.sancai_strokes[stroke]["parse"]
        else:
            return ""

    def check_wuge_config(self, name, types=1):
        xing, xing2, ming1, ming2 = 0, 0, 0, 0

        complex_name = self.s2t.convert(name)
        xing = self.get_stroke_number(name[0])
        if len(name) == 2:
            status = 1
            ming1 = self.get_stroke_number(name[1])
        elif len(name) == 3:
            if types == 1:
                status = 2
                ming1 = self.get_stroke_number(name[1])
                ming2 = self.get_stroke_number(name[2])
            else:
                status = 3
                xing2 = self.get_stroke_number(name[1])
                ming1 = self.get_stroke_number(name[2])
        else:
            status = 4
            xing2 = self.get_stroke_number(name[1])
            ming1 = self.get_stroke_number(name[2])
            ming2 = self.get_stroke_number(name[3])

        # 五格计算
        if status == 1 or status == 2:
            tian = xing + 1
            ren = xing + ming1
            if status == 1:
                di = ming1 + 1
                zong = xing + ming1
                wai = 2
            else:
                di = ming1 + ming2
                zong = xing + di
                wai = zong - ren + 1
        else:
            tian = xing + xing2
            ren = xing2 + ming1
            if status == 3:
                di = ming1 + 1
                zong = tian + ming1
                wai = zong - ren + 1
            else:
                di = ming1 + ming2
                zong = tian + di
                wai = zong - ren

        # 三才配置
        sancai_config = self.get_sancai_config([tian, ren, di, zong, wai])
        result = {
            "name_info": {
                "name": {"s": name, "c": complex_name},
            },
            "sancai": {
                "wuxing": sancai_config[0:3],
                "sancai_type": self.wuxing_luck_bad[sancai_config[0:3]],
            },
            "wuge": {
                "tian": {"bihua": tian, "sancai_type": self.get_stroke_type(tian),
                         "wuxing": self.get_wuxing(tian, types=2)},
                "ren": {"bihua": ren, "sancai_type": self.get_stroke_type(ren),
                        "wuxing": self.get_wuxing(ren, types=2)},
                "di": {"bihua": di, "sancai_type": self.get_stroke_type(di),
                       "wuxing": self.get_wuxing(di, types=2)},
                "wai": {"bihua": wai, "sancai_type": self.get_stroke_type(wai),
                        "wuxing": self.get_wuxing(wai, types=2)},
                "zong": {"bihua": zong, "sancai_type": self.get_stroke_type(zong),
                         "wuxing": self.get_wuxing(zong, types=2)},

            },
        }
        if status == 1 or status == 2:
            result["name_info"]["xing"] = {
                "jianti": name[0],
                "fanti": complex_name[0],
                "bihua": xing,
                "pinyin": pinyin(name[0])[0][0],
                "wuxing": self.get_hz_wuxing(name[0], xing)
            }
            result["name_info"]["ming1"] = {
                "jianti": name[1],
                "fanti": complex_name[1],
                "bihua": ming1,
                "pinyin": pinyin(name[1])[0][0],
                "wuxing": self.get_hz_wuxing(name[1], ming1),
            }
            if status == 2:
                result["name_info"]["ming2"] = {
                    "jianti": name[2],
                    "fanti": complex_name[2],
                    "bihua": ming2,
                    "pinyin": pinyin(name[2])[0][0],
                    "wuxing": self.get_hz_wuxing(name[2], ming2)
                }
        else:
            result["name_info"]["xing"] = {
                "jianti": name[0],
                "fanti": complex_name[0],
                "bihua": xing,
                "pinyin": pinyin(name[0])[0][0],
                "wuxing": self.get_hz_wuxing(name[0], xing)
            }
            result["name_info"]["xing2"] = {
                "jianti": name[1],
                "fanti": complex_name[1],
                "bihua": xing2,
                "pinyin": pinyin(name[1])[0][0],
                "wuxing": self.get_hz_wuxing(name[1], xing)
            }
            result["name_info"]["ming1"] = {
                "jianti": name[2],
                "fanti": complex_name[2],
                "bihua": ming1,
                "pinyin": pinyin(name[2])[0][0],
                "wuxing": self.get_hz_wuxing(name[2], ming1),
            }
            if status == 4:
                result["name_info"]["ming2"] = {
                    "jianti": name[3],
                    "fanti": complex_name[3],
                    "bihua": ming2,
                    "pinyin": pinyin(name[3])[0][0],
                    "wuxing": self.get_hz_wuxing(name[3], ming2)
                }

        for ni in result["name_info"].keys():
            if ni == "name" or ni == "xing" or ni == "xing2":
                pass
            else:
                result["name_info"][ni]["introduce"] = self.wuxing_strokes[
                    result["name_info"][ni]['wuxing']
                ][0][
                    result["name_info"][ni]["jianti"]
                ]["introduce"]
        return result

    def get_source(self, source_list, validate, stroke_list):

        exist_name = dict()
        if validate:
            print('>>加载名字库...')
            get_name_valid('Chinese_Names', exist_name)

        names = {}
        for source in source_list:
            # 默认
            if source == 0:
                # get_name_dat('Chinese_Names', names, stroke_list)
                pass
            # 诗经
            elif source == 1:
                # print('>>加载诗经...')
                names["name1"] = self.get_name_json('诗经', 'content', stroke_list)
            # 楚辞
            elif source == 2:

                names["name2"] = self.get_name_json('楚辞', 'paragraphs', stroke_list)
                pass
            # 论语
            elif source == 3:
                # print('>>加载论语...')
                names["name3"] = self.get_name_json('论语', 'paragraphs', stroke_list)
            # 周易
            elif source == 4:
                # print('>>加载周易...')
                # get_name_txt('周易', names, stroke_list)
                pass
            # 唐诗
            elif source == 5:
                # print('>>加载唐诗...')
                # for i in range(0, 58000, 1000):
                # get_name_json('唐诗/poet.tang.' + str(i), names, 'paragraphs', stroke_list)
                pass
            # 宋诗
            elif source == 6:
                # print('>>加载宋诗...')
                # for i in range(0, 255000, 1000):
                #     get_name_json('宋诗/poet.song.' + str(i), names, 'paragraphs', stroke_list)
                pass
            # 宋词
            elif source == 7:
                # print('>>加载宋词...')
                # for i in range(0, 22000, 1000):
                #     get_name_json('宋词/ci.song.' + str(i), names, 'paragraphs', stroke_list)
                pass
            else:
                print('词库号输入错误')

            # print('>>筛选名字...')
            # 检查名字是否存在并添加性别
            if validate:
                if source != 0:
                    names = get_intersect(names, exist_name)
        temp_name = {}
        for na in names.keys():
            for n in names[na].keys():
                temp_name[n] = names[na][n]
        # print(names)
        # print(temp_name)
        return temp_name

    def get_intersect(self, names, exist_name):
        result = set()
        for i in names:
            if i.first_name in exist_name.keys():
                i.gender = exist_name[i.first_name]
                result.add(i)
        return result

    def get_name_json(self, path, column, stroke_list):
        names = {}
        with open('data/' + path + '.json', encoding='utf-8') as f:
            data = json.loads(f.read())
            size = len(data)
            for j in range(0, size):
                for string in data[j][column]:
                    # 转繁体
                    string = self.s2t.convert(string)
                    string_list = re.split('！？，。,.?! \n', string)
                    names = self.check_and_add_names(names, string_list, stroke_list, f"{path}·{data[j]['chapter']}")
        return names

    def check_and_add_names(self, names, string_list, stroke_list, path):
        for sentence in string_list:
            sentence = sentence.strip()
            # 转换笔画数
            strokes = list()
            # print(sentence)
            for ch in sentence:
                if self.is_chinese(ch):
                    # print(ch)
                    strokes.append(self.get_stroke_number(self.t2s.convert(ch)))
                else:
                    strokes.append(0)
            # 判断是否包含指定笔画数
            for stroke in stroke_list:
                if stroke[0] in strokes and stroke[1] in strokes:
                    index0 = strokes.index(stroke[0])
                    index1 = strokes.index(stroke[1])
                    if index0 < index1:
                        name0 = sentence[index0]
                        name1 = sentence[index1]
                        # sentence = sentence.replace(name0, f"「{name0}」").replace(name1, f"「{name1}」")
                        name_result = self.t2s.convert(f"{name0}{name1}")
                        sentence = self.t2s.convert(sentence)
                        names[name_result] = sentence + f"【{path}】"
        return names

    def run_bazi(self, conditions):
        sc_info = conditions["sc_info"]
        sc_infos = self.shengcheng_infos(sc_info)
        return sc_infos

    def qiming(self, conditions):
        first_name = conditions["first_name"]
        yn_use = conditions["yn_use"]
        ming_type = conditions["ming_type"]  # 2
        sex = conditions["sex"]
        name_type = conditions["name_type"]
        xing_type = conditions["xing_type"]
        fn_bihua_list = []
        for fn in first_name:
            # fn_ft = self.cc.convert(fn)
            fn_bihua = self.get_stroke_number(fn)
            fn_bihua_list.append(fn_bihua)
            # fn_wuxing = self.get_hz_wuxing(fn, fn_bihua)

            # logger.info(f'姓氏：{fn}  拼音【{pinyin(fn)[0][0]}】 笔画：{fn_bihua}  五行：{fn_wuxing}')

        sc_info = conditions["sc_info"]
        sc_infos = self.shengcheng_infos(sc_info)
        # logger.info(sc_infos)
        good_name_list = {}
        # 多名的来源
        good_name_list2 = {}
        name_list = {
            "bazi": sc_infos,
            "good": [],

        }
        if name_type == 2:
            name_list["generals"] = []
        if ming_type == 1:
            fn_bihua_sum = sum(fn_bihua_list)
            # logger.info(f"姓氏总笔画：【{fn_bihua_sum}】")
            good_nubs = self.get_good_number(fn_bihua_sum)
            # logger.info("需要补充的数字")
            # logger.info(good_nubs)
            lack_wuxing = sc_infos["revise_wuxing"]
            # logger.info(f'八字五行缺【{lack_wuxing}】')
            for k in good_nubs.keys():
                good_name_list[k] = []
                wuxing_dict = self.wuxing_strokes[lack_wuxing]

                for gk in good_nubs[k]:
                    if gk in wuxing_dict.keys():
                        for wdgk in wuxing_dict[gk]["y"]:
                            good_name_list[k].append(f"{first_name}{wdgk}")
                        if yn_use == "n":
                            for wdgk in wuxing_dict[gk]["n"]:
                                good_name_list[k].append(f"{first_name}{wdgk}")
        else:
            # 女诗经，男楚辞，文论语，武周易
            # logger.info(f"八字调整后五行【{sc_infos['end_wuxing']}】")
            good_nubs = self.getLastNameWuge(first_name)
            # logger.info(good_nubs)
            # 选择加载词库的类型 3 论语
            two_name_list1 = self.get_source([1, 2, 3], False, good_nubs)
            good_name_list2 = two_name_list1
            # print(two_name_list1)
            for tnl in two_name_list1:
                if "good" not in good_name_list.keys():
                    good_name_list["good"] = [f"{first_name}{tnl}"]
                else:
                    good_name_list["good"].append(f"{first_name}{tnl}")
            # print(two_name_list1)
        # print(self.baijiaxing_sancaiwuge_dict)
        # print(good_name_list)

        # # 先获取名字对应的三才五格，筛选名字三才五格的吉凶
        for k in good_name_list.keys():
            for gnl in good_name_list[k]:
                # print(gnl)
                name_infos = self.check_wuge_config(gnl, types=xing_type)
                ji_count = 0
                if name_infos["sancai"]["sancai_type"]["luck_bad"] == "大吉":
                    for wg in name_infos["wuge"].keys():
                        if "吉" in name_infos["wuge"][wg]["sancai_type"]:
                            ji_count += 1
                    if ji_count >= 2:
                        try:
                            result = ngender.guess(name_infos["name_info"]["name"]["s"])
                            if ming_type == 2:
                                name_infos["source"] = good_name_list2[
                                    name_infos["name_info"]["name"]["s"].replace(first_name, "")]
                            if result[0] == sex:
                                name_list["good"].append(name_infos)
                        except:
                            # logger.error(f'无法测取【{name_infos["name_info"]["name"]["s"]}】的性别')
                            pass

                elif name_infos["sancai"]["sancai_type"]["luck_bad"] == "中吉" \
                        or name_infos["sancai"]["sancai_type"]["luck_bad"] == "吉":
                    for wg in name_infos["wuge"].keys():
                        if "吉" in name_infos["wuge"][wg]["sancai_type"]:
                            ji_count += 1
                    if ji_count >= 2:
                        try:
                            result = ngender.guess(name_infos["name_info"]["name"]["s"])
                            if ming_type == 2:
                                name_infos["source"] = good_name_list2[
                                    name_infos["name_info"]["name"]["s"].replace(first_name, "")]
                            if result[0] == sex:
                                name_list["generals"].append(name_infos)
                        except:
                            # logger.error(f'无法测取【{name_infos["name_info"]["name"]["s"]}】的性别')
                            pass
        # print(name_list)
        # print(len(name_list["good"]))
        # print(len(name_list["generals"]))
        return name_list


qm = QiMing()


@app.route('/qiming', methods=['POST'])
def run1():
    response = {}
    if request.method == 'POST':
        try:

            content = json.loads(request.get_data())
            # print(request.get_data())
            # print(content)
            if "sc_info" not in content.keys() and len(content["sc_info"]) == 4:
                response["status"] = "error"
                response["msg"] = '生辰八字缺失 例子[1970,1,1] 集合里为整数元素且数量为4'
            elif "sex" not in content.keys():
                response["status"] = "error"
                response["msg"] = '性别缺失 男 male 女 female 字符串类型'
            elif "first_name" not in content.keys():
                response["status"] = "error"
                response["msg"] = '姓氏缺失 字符串类型'
            elif "yn_use" not in content.keys():
                paresponse["status"] = "error"
                response["msg"] = '选择常用字或者冷僻字 y 常用字 n 非常用字'
            elif "ming_type" not in content.keys():
                response["status"] = "error"
                response["msg"] = '名字个数未选择1或者2 int类型'
            elif "xing_type" not in content.keys():
                response["status"] = "error"
                response["msg"] = '姓个数未选择1或者2 int类型'
            else:
                data = qm.qiming(content)
                response["status"] = "success"
                response["msg"] = '生成成功'
                response["result"] = data
        except Exception as e:
            logger.error(e)
            response["status"] = "error"
            response["msg"] = "qiming，请检查   【{}】".format(e)
    else:
        response["status"] = "error"
        response["msg"] = "qiming,不是POST"

    return jsonify(response)


@app.route('/bazi', methods=['POST'])
def run2():
    response = {}
    if request.method == 'POST':
        try:

            content = json.loads(request.get_data())
            # print(content)
            if "sc_info" not in content.keys():
                response["status"] = "error"
                response["msg"] = '生辰八字缺失 例子[1970,1,1,1] 集合里为整数元素'
            else:
                data = qm.run_bazi(content)
                response["status"] = "success"
                response["msg"] = '分析成功'
                response["result"] = data
        except Exception as e:
            logger.error(e)
            response["status"] = "error"
            response["msg"] = "bazi，请检查   【{}】".format(e)
    else:
        response["status"] = "error"
        response["msg"] = "bazi,不是POST"

    return jsonify(response)


@app.route('/name_test', methods=['POST'])
def run3():
    response = {}
    if request.method == 'POST':
        try:
            content = json.loads(request.get_data())
            # print(content)
            if "name" not in content.keys():
                response["status"] = "error"
                response["msg"] = '需要测试的姓名未输入'
            else:
                data = qm.check_wuge_config(content["name"], types=content["xing_type"])
                response["status"] = "success"
                response["msg"] = '分析成功'
                response["result"] = data
        except Exception as e:
            logger.error(e)
            response["status"] = "error"
            response["msg"] = "name_test，请检查   【{}】".format(e)
    else:
        response["status"] = "error"
        response["msg"] = "name_test,不是POST"

    return jsonify(response)


if __name__ == '__main__':
    # qm = QiMing()
    # print(qm.qiming({
    #     "sc_info": [1995, 10, 5, 1],
    #     "sex": "male",  # 1 male 2 female
    #     "first_name": "慕容",
    #     "xing_type": 1,  # 1 单姓 2 双姓
    #     "yn_use": "y",  # y 常用字 n 非常用字
    #     "ming_type": 1,  # 1 单字 2 双字
    #     "name_type": 1,  # 1 只取吉名 2 吉名和中吉名都取
    #
    # }))

    # ttttttt = qm.check_wuge_config("慕容中分",types=2)
    # print(ttttttt)

    # ttt = qm.run_bazi({"sc_info": [1992, 12, 7, 1], })
    # print(ttt)
    #
    app.run(host='0.0.0.0', port=8090)
