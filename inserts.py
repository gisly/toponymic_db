#!/usr/bin/python
# -*- coding: utf-8 -*
__author__ = "gisly"
import codecs
import psycopg2

MOTIVATION_MAP = {
"физические характеристики" : "2",
"материал" : "3",
"ландшафт" : "4",
"ландшат" : "4",
"иноязычное" : "5",
"инояз" : "5",
"фауна" : "6",
"предмет" : "7",
"место" : "8",
"сакральное" : "9",
"жилище" : "10",
"жилище / постройка" : "10",
"термин родства" : "11",
"оценка" : "12",
"части тела" : "13",
"флора" : "14",
"круг кочевания" : "15",
"явление природы" : "16",
"неизвестно" : "17",
"другое" : 17,
"" : 17,
"имя" : "18",
"событие" : "19",
"положение в пространстве" : "20",
"часть туши" : "21",
"движение" : "22"
}

MOTIVATION_TYPES_TUPLES = [("2", "физические характеристики", "physical features", "физические характеристики", "physical features"),
("3", "материал", "material", "материал", "material"),
("4", "ландшафт", "landscape", "ландшафт", "landscape"),
("5", "иноязычное", "foreign language", "иноязычное", "foreign language"),
("6", "фауна", "fauna", "фауна", "fauna"),
("7", "предмет", "object", "предмет", "object"),
("8", "место", "place", "место [???]", "place"),
("9", "сакральное", "sacred", "сакральное", "sacred"),
("10", "жилище", "house", "жилище", "house"),
("11", "термин родства", "kinship term", "термин родства", "kinship term"),
("12", "оценка", "assessment", "оценка", "assessment"),
("13", "части тела", "body parts", "части тела", "body parts"),
("14", "флора", "flora", "флора", "flora"),
("15", "круг кочевания", "nomadic circle", "круг кочевания", "nomadic circle"),
("16", "явление природы", "nature phenomenon", "явление природы", "nature phenomenon"),
("17", "неизвестно", "unknown", "неизвестно", "unknown"),
("18", "имя", "name", "имя", "name"),
("19", "событие", "event", "событие", "event"),
("20", "положение в пространстве", "position", "положение в пространстве", "position"),
("21", "часть туши", "animal body part", "часть туши", "animal body part"),
("22", "движение", "motion", "движение", "motion")]

def import_from_file(filename):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(database="geoterms", user="app", password="rfrfyl.babaloos", host="gisly.net", port=5432)
        cur = conn.cursor()
        insert_geo_types(cur)
        insert_languages(cur)
        insert_sources(cur)
        insert_motivations(cur)
        with open(filename, "r", encoding="utf-8") as fin:
            for index, line in enumerate(fin):
                line_parts = line.split('\t')
                insert_geo(line_parts, cur, conn, index, None)
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.commit()
            conn.close()
        if cur:
            cur.close()

def insert_geo_types(cur):
    cur.execute("INSERT INTO geo_types("
                "geotype_id, geotype_ru, geotype_en, geotype_description_ru, geotype_description_en)"
                " VALUES (%s, %s, %s, %s, %s)",
                (1, "река", "river", "река", "river"))

def insert_languages(cur):
    cur.execute("INSERT INTO languages("
                "language_id, language_iso, language_name_ru, language_name_en)"
                " VALUES (%s, %s, %s, %s)",
                (1, "evk", "эвенкийский", "Evenki"))
    cur.execute("INSERT INTO languages("
                "language_id, language_iso, language_name_ru, language_name_en)"
                " VALUES (%s, %s, %s, %s)",
                (2, "sah", "якутский", "Yakut (Sakha)"))
    cur.execute("INSERT INTO languages("
                "language_id, language_iso, language_name_ru, language_name_en)"
                " VALUES (%s, %s, %s, %s)",
                (3, "rus", "русский", "Russian"))

def insert_sources(cur):
    cur.execute("INSERT INTO source_references("
                "source_id, source_full_description)"
                " VALUES (%s, %s)",
                (1, "unknown"))

def insert_motivations(cur):
    statement = "INSERT INTO motivation_types "\
                "(motivation_id, motivation_short_name_ru, motivation_short_name_en, motivation_comment_ru, " \
                "motivation_comment_en) "\
                "VALUES (%s, %s, %s, %s, %s)"

    for motivation_tuple in MOTIVATION_TYPES_TUPLES:
        cur.execute(statement,
                    motivation_tuple)



def insert_geo(line_parts, cur, conn, osm_id, area_name_ru):
    geoname = line_parts[0].strip()
    translation = line_parts[1].strip()
    linguistic_means = line_parts[2].strip()
    motivation_type = line_parts[3].strip()
    motivation_comment = line_parts[4].strip()
    if motivation_type not in MOTIVATION_MAP:
        print(motivation_type + ":" + geoname)
        return

    motivation_id = MOTIVATION_MAP[motivation_type]

    cur.execute("INSERT INTO geo_objects("
                "latitude, longitude, osm_id, geotype_id, area_name_ru)"
                " VALUES (%s, %s, %s, %s, %s) RETURNING geoobject_id",
                (0, 0, osm_id, 1, area_name_ru))

    geoojbect_id = cur.fetchone()[0]

    cur.execute("INSERT INTO geo_names("
                "geoname, name_translation_ru, name_translation_en, "
                "motivation_comment, linguistic_means, language_id, "
                "geoobject_id, source_id, motivation_id)"
                "VALUES (%s, %s, %s, "
                "%s, %s, %s, "
                "%s, %s, %s)",
                (geoname, translation, "NA",
                 motivation_comment, linguistic_means, 1,
                 geoojbect_id, 1, motivation_id))


    #conn.commit()



def update_river_systems(filename):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(database="geoterms", user="app", password="rfrfyl.babaloos", port=5432, host="gisly.net")
        cur = conn.cursor()
        river_systems, river_names_freq_dict, river_systems_by_name  = read_river_systems(filename)

        for river_name, river_data in river_systems_by_name.items():
            if river_names_freq_dict[river_name] > 1:
                cur.execute(
                    "SELECT o.geoobject_id FROM geo_objects o join geo_names n ON o.geoobject_id = n.geoobject_id"
                    " WHERE n.geoname = %s", (river_name,))
                geoobject_id = None
                for res in cur:
                    geoobject_id = res[0]
                    break
                if geoobject_id:
                    cur.execute("UPDATE geo_objects SET area_name_ru = %s,"
                                "area_name_en = %s where geoobject_id = %s",
                                (river_data[0][1], None, geoobject_id))
                    start_index = 1
                else:
                    start_index = 0


                for i in range(start_index, len(river_data)):
                    area_name_real = river_data[i][1]
                    if not area_name_real:
                        area_name_real = ''

                    insert_geo([river_name, '?', '', '', ''], cur, conn, i, area_name_real)
            else:
                area_name_real = river_data[0][1]
                if not area_name_real:
                    area_name_real = ''
                area_name = str(river_data[0][0]) + '-' + area_name_real

                update_area_name(cur, conn, area_name, river_name)




    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.commit()
            conn.close()
        if cur:
            cur.close()

def update_area_name(cur, conn, area_name, river_name):
    cur.execute("SELECT o.geoobject_id FROM geo_objects o join geo_names n ON o.geoobject_id = n.geoobject_id"
                " WHERE n.geoname = %s", (river_name,))
    geoobject_id = None
    for res in cur:
        geoobject_id = res[0]
        break
    if geoobject_id is None:
        insert_geo([river_name, '?', '', '', ''], cur, conn, 0, area_name)
    else:
        cur.execute("UPDATE geo_objects SET area_name_ru = %s,"
                    "area_name_en = %s where geoobject_id = %s",
                    (area_name, None, geoobject_id))


def read_river_systems(filename):
    with open(filename, "r", encoding="utf-8") as fin:
        river_systems = dict()
        river_systems_by_name = dict()
        current_rivers = []
        current_map_name = None
        current_map_number = None
        river_names_freq_dict = dict()
        for line in fin:
            line_parts = line.strip().split('\t')
            if len(line_parts) > 2:
                index_part = line_parts[0]
            else:
                index_part = ''
            river_name = line_parts[-1]

            if river_name in river_names_freq_dict:
                river_names_freq_dict[river_name] += 1
            else:
                river_names_freq_dict[river_name] = 1


            if index_part != '':
                if index_part.isnumeric():
                    if current_map_name is not None:
                        river_systems[current_map_number] = dict()
                        river_systems[current_map_number]['rivers'] = current_rivers
                        river_systems[current_map_number]['map_name'] = current_map_name
                    current_rivers = []
                    current_map_number = index_part
                    current_map_name = None

                else:
                    current_map_name = index_part
            current_rivers.append(river_name)
            if river_name in river_systems_by_name:
                river_systems_by_name[river_name].append((current_map_number, current_map_name))
            else:
                river_systems_by_name[river_name] = [(current_map_number, current_map_name)]


    if current_map_name is not None:
        river_systems[current_map_number] = dict()
        river_systems[current_map_number]['rivers'] = current_rivers
        river_systems[current_map_number]['map_name'] = current_map_name
    return river_systems, river_names_freq_dict, river_systems_by_name

#import_from_file("test.csv")

update_river_systems("D:/Projects/2018/Nadya/rivers_systems.txt")