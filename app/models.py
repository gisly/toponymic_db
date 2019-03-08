from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship


class Languages(Model):
    language_id = Column(Integer, primary_key=True)
    language_iso = Column(String(100), unique=True, nullable=False)
    language_name_ru = Column(String(100), unique=True, nullable=False)
    language_name_en = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return self.language_iso


class SourceReferences(Model):
    source_id = Column(Integer, primary_key=True)
    source_full_description = Column(String(100), unique=False, nullable=False)

    def __repr__(self):
        return self.source_full_description


class MotivationTypes(Model):
    motivation_id = Column(Integer, primary_key=True)
    motivation_short_name_ru = Column(String(100), unique=True, nullable=False)
    motivation_short_name_en = Column(String(100), unique=True, nullable=False)
    motivation_comment_ru = Column(String(1000), unique=False, nullable=False)
    motivation_comment_en = Column(String(1000), unique=False, nullable=False)

    def __repr__(self):
        return self.motivation_short_name_ru

    def __lt__(self, other):
        return self.motivation_short_name_ru < other.motivation_short_name_ru


class GeoTypes(Model):
    geotype_id = Column(Integer, primary_key=True)
    geotype_ru = Column(String(100), unique=True, nullable=False)
    geotype_en = Column(String(100), unique=True, nullable=False)
    geotype_description_ru = Column(String(1000), unique=False, nullable=False)
    geotype_description_en = Column(String(1000), unique=False, nullable=False)

    def __repr__(self):
        return self.geotype_ru


class GeoObjects(Model):
    geoobject_id = Column(Integer, primary_key=True)
    latitude = Column(Numeric, unique=False, nullable=False)
    longitude = Column(Numeric, unique=False, nullable=False)
    osm_id = Column(Integer, primary_key=False, unique=False, nullable=False)
    area_name_ru = Column(String(1000), unique=False, nullable=True)
    area_name_en = Column(String(1000), unique=False, nullable=True)
    geotype_id = Column(Integer, ForeignKey("geo_types.geotype_id"), nullable=False)
    geo_types = relationship("GeoTypes")

    def __repr__(self):
        return '%s:%s (%s;%s)' % (self.latitude, self.longitude, self.osm_id, self.area_name_en)


class GeoNames(Model):
    geoname_id = Column(Integer, primary_key=True)
    geoname = Column(String(200), unique=False, nullable=False)
    name_translation_ru = Column(String(200), unique=False, nullable=False)
    name_translation_en = Column(String(200), unique=False, nullable=False)
    motivation_comment = Column(String(1000), unique=False, nullable=True)
    linguistic_means = Column(String(1000), unique=False, nullable=True)

    language_id = Column(Integer, ForeignKey("languages.language_id"), nullable=False)
    languages = relationship("Languages")

    geoobject_id = Column(Integer, ForeignKey("geo_objects.geoobject_id"), nullable=False)
    geo_objects = relationship("GeoObjects")

    source_references = relationship("SourceReferences")
    source_id = Column(Integer, ForeignKey("source_references.source_id"), nullable=False)

    motivation_types = relationship("MotivationTypes")
    motivation_id = Column(Integer, ForeignKey("motivation_types.motivation_id"), nullable=False)

    def __repr__(self):
        return self.geoname
