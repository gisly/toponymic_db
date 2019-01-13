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

def import_from_file(filename):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(database="geoterms", user="app", password=">^P2c!yK*^NeH7cy", port=5433)
        cur = conn.cursor()
        with open(filename, "r", encoding="utf-8") as fin:
            for index, line in enumerate(fin):
                insert_geo(line, cur, conn, index)
    except Exception as e:
        print(e)
        if conn:
            conn.close()
        if cur:
            cur.close()

def insert_geo(line, cur, conn, osm_id):
    line_parts = line.split('\t')
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
                "latitude, longitude, osm_id, geotype_id)"
                " VALUES (%s, %s, %s, %s) RETURNING geoobject_id",
                (0, 0, osm_id, 1))

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
                 geoojbect_id, 2, motivation_id))


    conn.commit()


import_from_file("test.csv")
