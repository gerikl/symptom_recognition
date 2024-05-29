from xml.dom import minidom
import re
import json
import pprint
import glob


def ProcessXML(file_path):
    doc = minidom.parse(file_path)
    res_array = []
    xPathCommon = '/ClinicalDocument/component/structuredBody/'  #Общая часть xPath
    comp_index = 1
    paragraph_index = 1
    an_zabol = "-"
    os_res1 = '-'
    res1 = "-"
    fp_res1 = "-"
    nn_section = doc.getElementsByTagName("section") #получаем список узлов section
    for sect in nn_section:
        stitle = sect.getElementsByTagName("title")[0].firstChild.data.strip().lower()
        if stitle == "анамнез":
            #print(stitle)
        
            name = sect.getElementsByTagName("text")[0]
            anamnez = name.firstChild.data
            res1 = ""
            res1 = re.search(r'\w', anamnez)
            if res1 is None:
                res1 = ""
            else:
                xS = res1.start()
                txt1 = anamnez [::-1]
                res2 = re.search(r'\w|\S', txt1)
                xE = len(anamnez) - res2.start()
                res1 = anamnez[xS:xE]
            splitter = 'Анамнез заболевания'
            an_zhizn = "-"
            an_zabol = "-"
            if splitter in res1:
                x = res1.split(splitter)
                an_zhizn = x[0]
                an_zabol = x[1]
            else:
                an_zabol = res1
            thisdict = {
                "xPath": xPathCommon + "component[" + str(comp_index) + "]/section/text",
                "text": an_zabol
                }
            res_array.append(thisdict)
        elif stitle == "анамнез заболевания":
            #print(stitle)
        
            name = sect.getElementsByTagName("text")[0]
            anamnez = name.firstChild.data
            res1 = ""
            res1 = re.search(r'\w', anamnez)
            an_zabol = "-"
            if res1 is None:
                res1 = ""
            else:
                xS = res1.start()
                txt1 = anamnez [::-1]
                res2 = re.search(r'\w|\S', txt1)
                xE = len(anamnez) - res2.start()
                res1 = anamnez[xS:xE]
                an_zabol = res1
            thisdict = {
                "xPath": xPathCommon + "component[" + str(comp_index) + "]/section/text",
                "text": an_zabol
                }
            res_array.append(thisdict)
        elif stitle == "объективизированная оценка состояния больного": #Получаем Объективный статус
            #print(stitle)
        
            name = sect.getElementsByTagName("text")[0]
            sost_obs = name.firstChild.data
            sost_obs = name.firstChild.data
            os_res1 = re.search(r'\w', sost_obs)
            xS = os_res1.start()
            os_txt1 = sost_obs [::-1]
            os_res2 = re.search(r'\w|\S', os_txt1)
            xE = len(sost_obs) - os_res2.start()
            os_res1 = sost_obs[xS:xE]
            thisdict = {
                "xPath": xPathCommon + "component[" + str(comp_index) + "]/section/text",
                "text": os_res1
                }
            res_array.append(thisdict)
        elif stitle == "физикальное обследование": #ФИЗИКАЛЬНЫЕ ПАРАМЕТРЫ
            #print(stitle)
            paragraph_index = 1
        
            pars = sect.getElementsByTagName("paragraph")
            for par in pars:
                sost_obs = par.firstChild.data
                fp_res1 = re.search(r'\w', sost_obs)
                xS = fp_res1.start()
                os_txt1 = sost_obs [::-1]
                os_res2 = re.search(r'\w|\S', os_txt1)
                xE = len(sost_obs) - os_res2.start()
                fp_res1 = sost_obs[xS:xE]
                thisdict = {
                    "xPath": xPathCommon + "component[" + str(comp_index) + "]/section/text/paragraph[" + str(paragraph_index) + "]",
                    "text": fp_res1
                }
                res_array.append(thisdict)
                paragraph_index += 1
        comp_index += 1
    return res_array


class DataLoader():
    def __init__(self):
        pass
    
    def get_symptoms(self, filename):
        with open(f"data/{filename}_result.json", 'r') as file:
            return json.load(file)
    
    def get_text(self, filename, count=-1):
        """
        Return format:
        {'/ClinicalDocument/component/structuredBody/component[3]/section/text': 'В 2012 году в возрасте 34 лет перенесла правостороннюю пневмонию, во время нахождения в стационаре впервые было выявлено повышение гликемии до 11,6 ммоль/л. Гликированный гемоглобин не исследовался. Была назначена терапия метформином (Сиофор) 1000 мг/сут. На этом фоне гликемия от 6,0 до 9,0 ммоль/л в течение дня. Спустя полгода самостоятельно отменила прием препарата. Весной 2013 года отметила снижение массы тела на 20 кг за 2 месяца на фоне неизмененного питания, слабость, полидипсию, полиурию. Была проконсультирована эндокринологом по месту жительства, назначена базис-болюсная инсулинотерапия по схеме: Хумулин Р по 6 ЕД перед основными приемами пищи, Протафан 20 ЕД/сут. В январе 2014 года госпитализирована в отделение реанимации и интенсивной терапии в состоянии кетоацидоза (медицинская документация не предоставлена). В настоящее время получает Новорапид из расчета 1ХЕ:1ЕД перед завтраком, обедом и ужином, Туджео 48 ЕД в 22.00. На этом фоне гликемия от 6,0 до 23,0 ммоль/л. Гликированный гемоглобин в сентябре 2021 г. - 9%.', '/ClinicalDocument/component/structuredBody/component[4]/section/text/paragraph[1]': '1.\n       Кожные покровы обычного цвета, нормальной влажности', '/ClinicalDocument/component/structuredBody/component[4]/section/text/paragraph[2]': '2.\n       видимые слизистые физиологической окраски, чистые', '/ClinicalDocument/component/structuredBody/component[4]/section/text/paragraph[3]': '3.\n       Дыхание везикулярное, хрипов нет.', '/ClinicalDocument/component/structuredBody/component[4]/section/text/paragraph[4]': '4.\n       Тоны сердца приглушены, ритмичные', '/ClinicalDocument/component/structuredBody/component[4]/section/text/paragraph[5]': '5.\n       Живот пальпаторно мягкий, безболезненный во всех отделах. Печень не увеличена.', '/ClinicalDocument/component/structuredBody/component[4]/section/text/paragraph[6]': '6.\n       нет', '/ClinicalDocument/component/structuredBody/component[6]/section/text': 'Отсутствует'}
        """
        with open(f"data/{filename}.xml", 'r') as file:
            from_dir = f"data/{filename}.xml"
            rr = ProcessXML(from_dir)
            return {block["xPath"]: block["text"] for block in rr}

    def __call__(self, filename):
        return self.load_text(filename), self.load_symptoms(filename)

    def get_files(self, number=-1):
        xml_files = glob.glob('data/*.xml')
        if number != -1:
            return [filename.split('/')[-1].split('.')[0] for filename in xml_files[:number]]
        return [filename.split('/')[-1].split('.')[0] for filename in xml_files]
