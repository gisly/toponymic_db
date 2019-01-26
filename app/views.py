from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from app import appbuilder, db
from .models import Languages, SourceReferences, MotivationTypes, GeoTypes, GeoObjects, GeoNames


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

class LanguageModelView(ModelView):
    datamodel = SQLAInterface(Languages)

    label_columns = {'language_iso':'Language ISO Code',
                     'language_name_ru' : 'Language name (Russian)',
                     'language_name_en' : 'Language name (English)'
                     }
    list_columns = ['language_iso',
                    'language_name_ru','language_name_en']

    show_fieldsets = [
                        (
                            'Summary',
                            {'fields':['language_iso','language_name_ru','language_name_en']}
                        ),

                     ]
    add_fieldsets = [
        (
            'Summary',
            {'fields': ['language_iso', 'language_name_ru', 'language_name_en']}
        ),

    ]

    edit_fieldsets = [
        (
            'Summary',
            {'fields': ['language_iso', 'language_name_ru', 'language_name_en']}
        ),

    ]

class SourceReferenceModelView(ModelView):
    datamodel = SQLAInterface(SourceReferences)

    label_columns = {'source_full_description':'Source full description'}

    show_fieldsets = [
                        (
                            'Summary',
                            {'fields':['source_full_description',]}
                        ),

                     ]
    add_fieldsets = [
                        (
                            'Summary',
                            {'fields':['source_full_description',]}
                        ),

                     ]

    edit_fieldsets = [
                        (
                            'Summary',
                            {'fields':['source_full_description',]}
                        ),

                     ]


class MotivationModelView(ModelView):
    datamodel = SQLAInterface(MotivationTypes)

    label_columns = {'motivation_short_name_ru':'Russian',
                     'motivation_short_name_en': 'English',
                     'motivation_comment_ru': 'Russian (comment)',
                     'motivation_comment_en': 'English (comment)',

                     }

    list_columns = ['motivation_short_name_ru',
                     'motivation_short_name_en',
                     'motivation_comment_ru',
                     'motivation_comment_en'
                     ]


    show_fieldsets = [
                        (
                            'Summary',
                            {'fields':['motivation_short_name_ru',
                                       'motivation_short_name_en',
                                       'motivation_comment_ru',
                                       'motivation_comment_en']}
                        ),

                     ]
    add_fieldsets = [
                        (
                            'Summary',
                            {'fields': ['motivation_short_name_ru',
                                        'motivation_short_name_en',
                                        'motivation_comment_ru',
                                        'motivation_comment_en']}
                        ),

                     ]

    edit_fieldsets = [
                        (
                            'Summary',
                            {'fields': ['motivation_short_name_ru',
                                        'motivation_short_name_en',
                                        'motivation_comment_ru',
                                        'motivation_comment_en']}
                        ),

                     ]


class GeoNamesModelView(ModelView):
    datamodel = SQLAInterface(GeoNames)
    label_columns = {
        'geoname' : 'Name',
        'name_translation_ru' : 'Translation (Russian)',
        'name_translation_en': 'Translation (English)',
        'motivation_types.motivation_short_name_ru' : 'Motivation (Russian)',
        'motivation_types.motivation_short_name_en': 'Motivation (English)',
        'motivation_comment' : 'Comment',
        'geo_objects.area_name_ru': 'Area it belongs to (Russian)',
        'geo_objects.area_name_en': 'Area it belongs to (English)',

    }
    list_columns = ['geoname',
                    'name_translation_ru',
                    'name_translation_en',
                    'motivation_types.motivation_short_name_ru',
                    'motivation_types.motivation_short_name_en',
                    'motivation_comment',
                    'geo_objects.area_name_ru',
                    'geo_objects.area_name_en'
                    ]

    show_fieldsets = [
                        (
                            'Summary',
                            {'fields' : ['geoname',
                                         'name_translation_ru',
                                         'name_translation_en',
                                         'motivation_comment',
                                         'linguistic_means',
                                       'languages',
                                       'geo_objects',
                                       'source_references',
                                    'motivation_types'
                             ]}
                        ),

                     ]
    add_fieldsets = [
        (
            'Summary',
            {'fields': ['geoname',
                        'name_translation_ru',
                        'name_translation_en',
                        'motivation_comment',
                        'linguistic_means',
                        'languages',
                        'geo_objects',
                        'source_references',
                        'motivation_types'
                        ]}
        ),

    ]

    edit_fieldsets = [
        (
            'Summary',
            {'fields': ['geoname',
                        'name_translation_ru',
                        'name_translation_en',
                        'motivation_comment',
                        'linguistic_means',
                        'languages',
                        'geo_objects',
                        'source_references',
                        'motivation_types'
                        ]}
        ),
    ]


class GeoObjectsModelView(ModelView):
    datamodel = SQLAInterface(GeoObjects)
    related_views = [GeoNamesModelView]

    label_columns = {'latitude': 'Latitude',
                     'longitude': 'Longitude',
                     'osm_id' : 'Object id in OpenStreetMap',
                     'geo_types.geotype_ru': 'Type (Russian)',
                     'geo_types.geotype_en': 'Type (English)',
                     'area_name_ru' : 'The area which it belongs to (Russian)',
                     'area_name_en' : 'The area which it belongs to (English)'
                     }
    list_columns = ['latitude', 'longitude', 'osm_id', 'geo_types.geotype_ru', 'geo_types.geotype_en',
                    'area_name_ru', 'area_name_en']
    base_order = ('latitude', 'asc')

    show_fieldsets = [
                        (
                            'Summary',
                            {'fields' : ['latitude',
                                       'longitude',
                                       'osm_id'
                                       'geo_types',
                                        'area_name_en',
                                         'area_name_ru'
                             ]}
                        ),

                     ]
    add_fieldsets = [
        (
            'Summary',
            {'fields': ['latitude',
                        'longitude',
                        'osm_id',
                        'geo_types',
                        'area_name_en',
                        'area_name_ru']}
        ),

    ]

    edit_fieldsets = [
        (
            'Summary',
            {'fields': ['latitude',
                        'longitude',
                        'osm_id',
                        'geo_types',
                        'area_name_en',
                        'area_name_ru'
                        ]}
        ),

    ]

class GeoTypesModelView(ModelView):
    datamodel = SQLAInterface(GeoTypes)
    related_views = [GeoObjectsModelView]

    label_columns = {'geotype_ru':'Geographical object type (Russian)',
                     'geotype_en': 'Geographical object type (English)',
                     'geotype_description_ru': 'Type description (Russian)',
                     'geotype_description_en': 'Type description (English)',
                     }
    list_columns = ['geotype_ru', 'geotype_en', 'geotype_description_ru', 'geotype_description_en',]


    show_fieldsets = [
                        (
                            'Summary',
                            {'fields':['geotype_ru',
                                       'geotype_en',
                                       'geotype_description_ru',
                                       'geotype_description_en']}
                        ),

                     ]
    add_fieldsets = [
                        (
                            'Summary',
                            {'fields': ['geotype_ru',
                                        'geotype_en',
                                        'geotype_description_ru',
                                        'geotype_description_en']}
                        ),

                     ]

    edit_fieldsets = [
                        (
                            'Summary',
                            {'fields': ['geotype_ru',
                                        'geotype_en',
                                        'geotype_description_ru',
                                        'geotype_description_en']}
                        ),

                     ]


from flask_appbuilder.charts.views import DirectByChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.group import aggregate_count


class GeoNamesDirectChartView(DirectByChartView):
    datamodel = SQLAInterface(GeoNames)
    chart_title = 'Geo Names'
    #chart_type = 'PieChart'

    definitions = [
        {
            'group': 'motivation_types.motivation_short_name_ru',
            'series': [(aggregate_count, 'motivation_types.motivation_short_name_ru')]
        },

    ]



db.create_all()

appbuilder.add_view(LanguageModelView,
                    "List languages",
                    icon = "fa-language",
                    category = "Directories",
                    category_icon="fa-book")

appbuilder.add_view(SourceReferenceModelView,
                    "List source references",
                    icon = "fa-book",
                    category = "Directories")

appbuilder.add_view(MotivationModelView,
                    "List motivation types",
                    icon = "fa-question",
                    category = "Directories")

appbuilder.add_view(GeoTypesModelView,
                    "List geo types",
                    icon = "fa-map",
                    category = "Directories")

appbuilder.add_view(GeoObjectsModelView,
                    "List geo objects",
                    icon = "fa-globe",
                    category = "Geo",
                    category_icon="fa-globe")


appbuilder.add_view(GeoNamesModelView,
                    "List geo names",
                    icon = "fa-globe",
                    category = "Geo",
)

appbuilder.add_view(GeoNamesDirectChartView,
                    "Geo names chart",
                    icon="fa-dashboard",
                    category="Geo")


