#!/bin/env python3

'''
Данная программа пишет главу о правильном переходе между эпохами
на основании данных с сайта https://rise-of-cultures.fandom.com.
'''

import requests
from bs4 import BeautifulSoup
import math
import pprint

epochs = {
    'BA': ['Бронзовый Век', 'Бронзового Века'],
    'ME': ['Минойская Эра', 'Минойской Эры'],
    'CG': ['Классическая Греция', 'Классической Греции'],
    'ER': ['Древний Рим', 'Древнего Рима'],
    'RE': ['Римская Империя', 'Римской Империи'],
    'BE': ['Византийская Эпоха', 'Византийской Эпохи'],
    'AF': ['Эпоха Франков', 'Эпохи Франков']
}

pages = {
    'CG': 'https://rise-of-cultures.fandom.com/wiki/Home_Cultures/Classic_Greece_(880_B.C.)',
    'ER': 'https://rise-of-cultures.fandom.com/wiki/Home_Cultures/Early_Rome_(750_B.C.)',
    'RE': 'https://rise-of-cultures.fandom.com/wiki/Home_Cultures/Roman_Empire_(50_B.C.)',
    'BE': 'https://rise-of-cultures.fandom.com/wiki/Home_Cultures/Byzantine_Era_(330_A.D.)',
    'AF': 'https://rise-of-cultures.fandom.com/wiki/Home_Cultures/Age_of_the_Franks_(550_A.D.)'
}

parents = {
    'CG': {
            'Agora': [],
            'Carpentry': ['Agora'],
            'Cultural Exchange': ['Agora'],
            'Domestic Pigs': ['Carpentry'],
            'Primary Goods': ['Carpentry'],
            'Alloys': ['Cultural Exchange'],
            'Storage': ['Cultural Exchange'],
            'Education': ['Domestic Pigs'],
            'Psiloi': ['Primary Goods'],
            'Golden Mask': ['Alloys'],
            'Ceremonial Dress': ['Storage'],
            'Philosophy': ['Education', 'Psiloi'],
            'Channel': ['Golden Mask', 'Ceremonial Dress'],
            'Crop Rotation': ['Philosophy', 'Channel'],
            'Toxotai': ['Philosophy', 'Channel'],
            'Astrology': ['Philosophy', 'Channel'],
            'Astronomy': ['Philosophy', 'Channel'],
            'Hoplites': ['Crop Rotation', 'Toxotai'],
            'Temples': ['Toxotai'],
            'Library': ['Astrology'],
            'Mummification': ['Astronomy'],
            'Cataphract': ['Hoplites'],
            'Concrete': ['Temples'],
            'Water Pump': ['Temples', 'Library', 'Mummification'],
            'Math': ['Cataphract', 'Concrete'],
            'Secondary Goods': ['Concrete'],
            'Make Up': ['Water Pump'],
            'Tertiary Goods': ['Math', 'Secondary Goods'],
            'Scaffolding': ['Make Up'],
            'Egyptian Consensus': ['Tertiary Goods', 'Scaffolding']
    },
    'ER': {
            'Municipium': [],
            'Hastati': ['Municipium'],
            'Rise of China': ['Municipium'],
            'Rear Livestock': ['Hastati', 'Rise of China'],
            'Insulae': ['Hastati', 'Rise of China'],
            'Primary Goods': ['Hastati', 'Rise of China'],
            'Ink and Brush': ['Rise of China'],
            'Marketplaces': ['Rear Livestock', 'Insulae', 'Primary Goods'],
            'Sericulture': ['Ink and Brush'],
            'Marks of History': ['Marketplaces'],
            'Velites': ['Marketplaces'],
            'Silk Manufacture': ['Sericulture'],
            'Tributum Capitis': ['Marks of History', 'Velites'],
            'Paddy Fields': ['Silk Manufacture'],
            'Rammed Earth Houses': ['Silk Manufacture'],
            'Auxilia Riders': ['Tributum Capitis', 'Paddy Fields'],
            'Calligraphy': ['Paddy Fields', 'Rammed Earth Houses'],
            'Roman Providence': ['Auxilia Riders'],
            'Baked Bricks': ['Calligraphy'],
            'Enhanced Paddy Fields': ['Calligraphy'],
            'Refined Silk': ['Calligraphy'],
            'Domus': ['Roman Providence'],
            'Triarii': ['Roman Providence'],
            'Dynastic Law': ['Baked Bricks', 'Enhanced Paddy Fields', 'Refined Silk'],
            'Watchtowers': ['Domus'],
            'Secondary Goods': ['Triarii'],
            'Silk Mastery': ['Dynastic Law'],
            'Tertiary Goods': ['Watchtowers', 'Secondary Goods', 'Silk Mastery']
    },
    'RE': {
            'Urbs Aeterna': [],
            'Fountains': ['Urbs Aeterna'],
            'Princeps': ['Urbs Aeterna'],
            'Dedicated Workforce': ['Urbs Aeterna'],
            'Swinery': ['Fountains'],
            'Primary Goods': ['Princeps'],
            'Kaolin Processing': ['Dedicated Workforce'],
            'Iron Plough': ['Dedicated Workforce'],
            'Forums': ['Swinery'],
            'Tenant Farming': ['Swinery'],
            'Sagittarii': ['Primary Goods'],
            'Porcelain Production': ['Kaolin Processing', 'Iron Plough'],
            'Ballistas': ['Forums', 'Tenant Farming', 'Sagittarii'],
            'Deep Foundations': ['Porcelain Production'],
            'Labor Duties': ['Porcelain Production'],
            'Villa Rustica': ['Ballistas', 'Deep Foundations'],
            'Terracing': ['Deep Foundations'],
            'Floor Plans': ['Labor Duties'],
            'Public Gardens': ['Villa Rustica'],
            'Villa Urbana': ['Villa Rustica'],
            'Turmae': ['Villa Rustica'],
            'Advanced Clayworks': ['Terracing', 'Floor Plans'],
            'Underfloor Heating': ['Public Gardens', 'Villa Urbana'],
            'Circus Maximus': ['Turmae'],
            'Urban Management': ['Advanced Clayworks'],
            'Dryland Farming': ['Advanced Clayworks'],
            'Secondary Goods': ['Underfloor Heating'],
            'Legionary': ['Circus Maximus'],
            'Porcelain Mastery': ['Urban Management', 'Dryland Farming'],
            'Tertiary Goods': ['Secondary Goods', 'Legionary', 'Porcelain Mastery'],
            'Chinese Consensus': ['Tertiary Goods']
    },
    'BE': {
            'Byzantium': [],
            'Bucellarii': ['Byzantium'],
            'Rise of the Maya': ['Byzantium'],
            'Primary Goods': ['Bucellarii'],
            'Ritual Sites': ['Rise of the Maya'],
            'Stone Carving': ['Rise of the Maya'],
            'Pendentive Dome': ['Primary Goods'],
            'Forquier': ['Primary Goods'],
            'Sacrificial Offerings': ['Ritual Sites', 'Stone Carving'],
            'Saracen Archers': ['Pendentive Dome'],
            'Architekton': ['Forquier'],
            'Shamanism': ['Sacrificial Offerings'],
            'Etched Landmarks': ['Sacrificial Offerings'],
            'Theodosian Walls': ['Saracen Archers', 'Architekton'],
            'Xocolatl': ['Shamanism', 'Etched Landmarks'],
            'Polyculture': ['Theodosian Walls'],
            'Crossgroined Vault': ['Theodosian Walls', 'Xocolatl'],
            'Obsidian Prospecting': ['Theodosian Walls', 'Xocolatl'],
            'Jade Prospecting': ['Theodosian Walls', 'Xocolatl'],
            'Catapult': ['Polyculture', 'Crossgroined Vault'],
            'Divining': ['Obsidian Prospecting', 'Jade Prospecting'],
            'Wheeled Plough': ['Catapult'],
            'Spiritual Ancestry': ['Divining'],
            'Precise Chronicle': ['Divining'],
            'Mortar': ['Wheeled Plough'],
            'Solar Rituals': ['Spiritual Ancestry'],
            'Chocolate Making': ['Precise Chronicle'],
            'Gregorian Calander': ['Mortar', 'Solar Rituals', 'Chocolate Making'],
            'Trapezites': ['Mortar', 'Solar Rituals', 'Chocolate Making'],
            'Nature Spirits': ['Mortar', 'Solar Rituals', 'Chocolate Making'],
            'Domical Vault': ['Gregorian Calander'],
            'Tillage': ['Trapezites'],
            'Jade Deposits': ['Nature Spirits'],
            'Obsidian Deposits': ['Nature Spirits'],
            'Jovians': ['Domical Vault', 'Tillage'],
            'Better Jade Extraction': ['Jade Deposits'],
            'Better Obsidian Extraction': ['Obsidian Deposits'],
            'Secondary Goods': ['Jovians'],
            'Water Cistern': ['Jovians'],
            'State Laws': ['Better Jade Extraction'],
            'Curative Rituals': ['Better Obsidian Extraction'],
            'Tertiary Goods': ['Secondary Goods', 'Water Cistern', 'State Laws', 'Curative Rituals']
    },
    'AF': {
            'Regnum Francorum': [],
            'Skirmishers': ['Regnum Francorum'],
            'Primary Goods': ['Regnum Francorum'],
            'Birdkeeping': ['Regnum Francorum'],
            'Villers': ['Skirmishers', 'Primary Goods'],
            'Headdress Craft': ['Birdkeeping'],
            'Astral Rituals': ['Birdkeeping'],
            'Aristocracy': ['Villers'],
            'Franc Axe Throwers': ['Villers'],
            'Ritual Daggers': ['Headdress Craft', 'Astral Rituals'],
            'Lingua Franca': ['Aristocracy', 'Franc Axe Throwers', 'Ritual Daggers'],
            'Advanced Jade Mining': ['Ritual Daggers'],
            'Advanced Obsidian Mining': ['Ritual Daggers'],
            'Spades': ['Lingua Franca'],
            'Aviculture': ['Advanced Jade Mining', 'Advanced Obsidian Mining'],
            'Perfected Headdresses': ['Advanced Jade Mining', 'Advanced Obsidian Mining'],
            'Production Boom': ['Spades'],
            'Caballarii': ['Spades'],
            'Maya Glyphs': ['Aviculture', 'Perfected Headdresses'],
            'Priest Schooling': ['Aviculture', 'Perfected Headdresses'],
            'Advanced Fodder': ['Production Boom', 'Caballarii', 'Maya Glyphs'],
            'Pottery Wheel': ['Production Boom', 'Caballarii', 'Priest Schooling'],
            'Sustainable Mining': ['Maya Glyphs', 'Priest Schooling'],
            'Improved Daggers': ['Maya Glyphs', 'Priest Schooling'],
            'Halberds': ['Advanced Fodder', 'Pottery Wheel'],
            'Sacred Shrines': ['Sustainable Mining', 'Improved Daggers'],
            'Population Growth': ['Sustainable Mining', 'Improved Daggers'],
            'Patrimony': ['Halberds'],
            'Scythes': ['Halberds'],
            'Feather Mastery': ['Sacred Shrines', 'Population Growth'],
            'Dagger Perfection': ['Sacred Shrines', 'Population Growth'],
            'Goat Herds': ['Patrimony', 'Scythes'],
            'Divine Ascension': ['Feather Mastery', 'Dagger Perfection'],
            'Ritual Mastery': ['Feather Mastery', 'Dagger Perfection'],
            'Carolingian Catapult': ['Goat Herds', 'Divine Ascension', 'Ritual Mastery'],
            'Leges Salica': ['Goat Herds', 'Divine Ascension', 'Ritual Mastery'],
            'Xocolatl Virtuoso': ['Goat Herds', 'Divine Ascension', 'Ritual Mastery'],
            'Secondary Goods': ['Carolingian Catapult', 'Leges Salica'],
            'Jade Mastery': ['Xocolatl Virtuoso'],
            'Obsidian Mastery': ['Xocolatl Virtuoso'],
            'Tertiary Goods': ['Secondary Goods'],
            'Astral Alignment': ['Jade Mastery', 'Obsidian Mastery'],
            'Mayan Consensus': ['Tertiary Goods', 'Astral Alignment']
    }
}

units = {
    'CG': ['Psiloi', 'Toxotai', 'Hoplites', 'Cataphract'],
    'ER': ['Hastati', 'Velites', 'Auxilia Riders', 'Triarii'],
    'RE': ['Princeps', 'Sagittarii', 'Ballistas', 'Turmae', 'Legionary'],
    'BE': ['Bucellarii', 'Saracen Archers', 'Catapult', 'Trapezites', 'Jovians'],
    'AF': ['Skirmishers', 'Franc Axe Throwers', 'Caballarii', 'Halberds', 'Carolingian Catapult']
}

units_ru = {
    'Psiloi': 'псилов',
    'Toxotai': 'токсотов',
    'Hoplites': 'гоплитов',
    'Cataphract': 'катафактариев',
    'Hastati': 'гастатов',
    'Velites': 'велитов',
    'Auxilia Riders': 'ауксисариев наездников',
    'Triarii': 'триариев',
    'Princeps': 'принципов',
    'Sagittarii': 'сагиттариев',
    'Ballistas': 'балист',
    'Turmae': 'турмов',
    'Legionary': 'легионеров',
    'Bucellarii': 'букеллариев',
    'Saracen Archers': 'сарацинских лучников',
    'Catapult': 'катапульт',
    'Trapezites': 'трапезитов',
    'Jovians': 'иовеанитов',
    'Skirmishers': 'бойцов',
    'Franc Axe Throwers': 'франков-метателей топоров',
    'Caballarii': 'кавалерии франков',
    'Halberds': 'алебардщиков',
    'Carolingian Catapult': 'катапульт каролингов'
}

all_technologies = dict() # Индексация парой (эпоха, технология).


def get_number(number_text: str):
    number_text = number_text.replace(',', '').replace('\n', '').upper().strip()
    if 'K' in number_text:
        number = float(number_text[: number_text.find('K')].strip())
    elif 'M' in number_text:
        number = float(number_text[: number_text.find('M')].strip())
    else:
        number = float(number_text)
    if 'K' in number_text:
        number *= 1000
    elif 'M' in number_text:
        number *= 1000000
    return int(number)


def get_word(value, words):
    if all((value % 10 == 1, value % 100 != 11)):
        return words[0]
    elif all((2 <= value % 10 <= 4,
              any((value % 100 < 10, value % 100 >= 20)))):
        return words[1]
    return words[2]


def days(value):
    words = ['день', 'дня', 'дней']
    return f'{value} {get_word(value, words)}'


def research(value):
    words = ['колба', 'колбы', 'колб']
    return f'{value} {get_word(value, words)}'


def goods(value):
    words = ['товар', 'товара', 'товаров']
    return f'{value} {get_word(value, words)}'


class Technology:
    def __init__(self, cells, epoch: str):
        self.name = cells[0].text.replace('\n', '').strip()
        self.epoch = epoch
        self.resources = [] #  Колбы, монеты, еда.
        self.goods = dict()
        self.parents = parents[self.epoch][self.name]

        for child in cells[1].children:
            if len(child.text) > 0:
                self.resources.append(get_number(child.text))
        goods_epoch = ''
        for child in cells[2].children:
            text = child.text.replace(',', '').replace('\n', '').strip()
            if len(text) > 0:
                if text.isnumeric():
                    if goods_epoch in self.goods:
                        self.goods[goods_epoch] += int(text)
                    else:
                        self.goods[goods_epoch] = int(text)
                else:
                    goods_epoch = text[-2:]

    def get_price(self):
        technologies = dict()

        def recursive_get_technologies(technology: str, epoch: str):
            tech_pair = (epoch, technology)
            if tech_pair not in technologies:
                technologies[tech_pair] = all_technologies[tech_pair]
                for parent in technologies[tech_pair].parents:
                    recursive_get_technologies(parent, epoch)

        recursive_get_technologies(self.name, self.epoch)
        price_resources = [0, 0, 0] # Колбы, монеты, еда.
        price_goods = dict()
        for tech in technologies:
            tech = all_technologies[tech]
            price_resources[0] += tech.resources[0]
            price_resources[1] += tech.resources[1]
            price_resources[2] += tech.resources[2]
            for goods_epoch, goods_value in zip (tech.goods.keys(), tech.goods.values()):
                if goods_epoch in price_goods:
                    price_goods[goods_epoch] += goods_value
                else:
                    price_goods[goods_epoch] = goods_value
        return price_resources, price_goods


class Epoch:
    def __init__(self, epoch: str):
        self.epoch = epoch
        self.technologies = dict()
        self.technologies_list = []  # Сохраняет порядок добавления.

        r = requests.get(pages[epoch])
        table = BeautifulSoup(r.content, 'html5lib').find('table', attrs={'class': 'article-table'})
        for row in table.find_all('tr')[1:]:
            tech = Technology(row.find_all('td'), epoch)
            all_technologies[(epoch, tech.name)] = tech
            self.technologies_list.append(tech.name)

    def print_technologies_list(self):
        print(f'\n{epochs[self.epoch][0]}\n')
        for tech in self.technologies_list:
            print(f"'{tech}': ['', '', ''],")

    def latex(self):
        epoch_list = ['BA', 'ME', 'CG', 'ER', 'RE', 'BE', 'AF']
        epoch_index = epoch_list.index(self.epoch)
        epoch_coefs = {epoch: 1.5 ** (epoch_list.index(epoch) - epoch_index) for epoch in epoch_list}
        CG_delta = epoch_index - epoch_list.index('CG')

        tex = f'\n\\subsection{{{epochs[self.epoch][0]}}}\n'
        for unit_name in units[self.epoch]:
            unit = all_technologies[(self.epoch, unit_name)]
            price_resources, price_goods = unit.get_price()
            goods_needed = math.ceil(sum([epoch_coefs[ep] * price_goods[ep] for ep in price_goods.keys()]))
            research_days = math.ceil(price_resources[0] / (50 * 0.185))
            goods_days = math.ceil(goods_needed / (int(15 / (1 + (CG_delta * 0.5))) * (60 + 30*CG_delta) * 2 * 3))
            tex += f'''\nДля прокачки до {units_ru[unit_name]} понадобится:

\\begin{{center}}
    \\begin{{tabular}}[h!]{{|l|l|}}
        \\hline
        Колб:   & {price_resources[0]} \\\\\\hline
        Золота: & {price_resources[1]} \\\\\\hline
        Еды:    & {price_resources[2]} \\\\\\hline
'''
            for goods_epoch, goods_value in zip(price_goods.keys(), price_goods.values()):
                tex += f'        Товаров {epochs[goods_epoch][1]}: & {goods_value} \\\\\\hline\n'
            tex += f'''    \\end{{tabular}}
\\end{{center}}

Товары дорожают от эпохи к эпохе в 1,5 раза.
Значит в эквиваленте {epochs[epoch_list[epoch_list.index(self.epoch) - 1]][1]} нужно {goods(goods_needed)}.
И при этом понадобится {research(price_resources[0])}. Если брать в день около 50 и принять коэффициент профита от вкладов
в Чудеса равным 0,185, то это {days(research_days)}.
Если считать, что три максимально культурно прокачанные мастерские эффективно работают часов 15 в день (простой от сна и затупов),
то для производства {goods(goods_needed)} нужно {days(goods_days)}.
То есть минимум {days(max(research_days, goods_days))}.\n\n'''
        return tex

print('''\section{Переход между эпохами}
\label{section:epochs} 

Везде ниже не учтены затраты на апгрейд казарм (только технологии).

''')

for epoch in pages.keys():
    print(Epoch(epoch).latex())
