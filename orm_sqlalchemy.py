from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///ormHH.sqlite', echo=False)

Base = declarative_base()

data_log = Table('data_log', Base.metadata,
                 Column('id', Integer, primary_key=True,),
                 Column('vacancy', String),
                 Column('page_number', Integer),
                 Column('region_id', Integer, ForeignKey('region.id')),
                 Column('export_type', Integer, ForeignKey('export_type.id')),
                 Column('log_time', DATETIME)
                 )

class ExportType(Base):
    __tablename__ = 'export_type'
    id = Column(Integer, primary_key=True)
    name = Column(Integer, unique=True)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    name = Column(Integer, unique=True)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

def generate_session():
    # Создание таблицы
    Base.metadata.create_all(engine)

    # Заполнение таблиц
    Session = sessionmaker(bind=engine)

    # Создание сессии
    session = Session()

    return session
try:
    session = generate_session()

    # заполнение таблицы export_type
    session.add_all([ExportType('Подсчет вакансий'), ExportType('Подсчет процента'), ExportType('Подсчет упоминаний')])

    # заполнение таблицы region
    session.add_all([Region('Москва'), Region('Питер'), Region('Подольск'), Region('Уфа')])

    session.commit()
except Exception as e:
    print('данные уже внесены')


### Запросы SQL через sqlalchemy
session = generate_session()

# выборка всех регионов
all_regions = session.query(Region).all() # select * from region
print(all_regions)

# получить идентификатор города Москва
moscow = session.query(Region).filter(Region.name == 'Москва').first() # я так понимаю, это select name from Region where name = 'Москва' order by id asc limit 1
print(moscow.id)

# выборка всех типов выгрузки
all_exports = session.query(ExportType).all() # select * from export_type
print(all_exports)

# получить всю строку, где name = Подсчет вакансий
count_vacancy = session.query(ExportType).filter(ExportType.name == 'Подсчет вакансий').first()
print(f"id: {count_vacancy.id}, name: {count_vacancy.name}")