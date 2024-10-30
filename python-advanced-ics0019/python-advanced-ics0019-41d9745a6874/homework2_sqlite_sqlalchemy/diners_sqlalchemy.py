# -*- coding: utf-8 -*-
"""
Creating TalTech diners database using SqlAlchemy.

Created on Mon Mar  6 20:05:20 2023

@author: aloansberg

There are 8 diners in different buildings of TalTech that will be added to database diners.db, table canteen.
There are 4 service providers in total: Rahva Toit, Baltic Restaurants Estonia AS, TTÜ Sport and Kohvik
that will be added to database diners.db, table provider.
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import event


def pragma_foreign_keys_on(connection, connection_record):
    """Enabling foreign keys."""
    connection.execute('pragma foreign_keys=ON')


# create connection with SqlAlchemy database. Creating database diners.db
engine = create_engine('sqlite:///diners.db', echo=False)
event.listen(engine, 'connect', pragma_foreign_keys_on)
Base = declarative_base()


# creating table canteen
class Canteen(Base):
    """Initializing table canteen by adding columns."""

    __tablename__ = 'canteen'

    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey('provider.id'))
    name = Column(String)
    location = Column(String)
    time_open = Column(Integer)
    time_closed = Column(Integer)
    provider = relationship("Provider", back_populates="canteen")


# creating table provider
class Provider(Base):
    """Initializing table provider by adding columns."""

    __tablename__ = 'provider'

    id = Column(Integer, primary_key=True)
    provider_name = Column(String)


Provider.canteen = relationship("Canteen", order_by=Canteen.id)
Base.metadata.create_all(engine)


def create_records():
    """Insert data to tables canteen and provider."""

    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # inserting multiple canteens and providers to database
        session.add_all([
            Canteen(provider_id=1, name='Economics- and social science building canteen',
                    location='Akadeemia tee 3 SOC- building', time_open=830, time_closed=1830),
            Canteen(provider_id=1, name='Library canteen', location='Akadeemia tee 1/Ehitajate tee 7', time_open=830,
                    time_closed=1900),
            Canteen(provider_id=2, name='Main building Deli cafe',
                    location='Ehitajate tee 5 U01 building', time_open=900,
                    time_closed=1630),
            Canteen(provider_id=2, name='Main building Daily lunch restaurant', location='Ehitajate tee 5 U01 building',
                    time_open=900, time_closed=1600),
            Canteen(provider_id=1, name='U06 building canteen', location='U06 building canteen', time_open=900,
                    time_closed=1600),
            Canteen(provider_id=2, name='Natural Science building canteen', location='Akadeemia tee 15 SCI building',
                    time_open=900, time_closed=1600),
            Canteen(provider_id=2, name='ICT building canteen', location='Raja 15/Mäepealse 1', time_open=900,
                    time_closed=1600),
            Canteen(provider_id=4, name='Sports building canteen', location='Männiliiva 7 S01 building', time_open=1100,
                    time_closed=2000),
            Provider(provider_name='Rahva Toit'),
            Provider(provider_name='Baltic Restaurants Estonia AS'),
            Provider(provider_name='Kohvik'),
            Provider(provider_name='TTÜ Sport OÜ')
        ]
        )

        # inserting bitStop KOHVIK separately
        insert_item = Canteen(provider_id=3, name='bitStop KOHVIK', location='IT College, Raja 4c',
                              time_open=930, time_closed=1600)

        session.add(insert_item)

        session.commit()
    except:
        print("\nCould not insert items to database\n")
        session.rollback()
        raise
    finally:
        session.close()


def format_time(row: int) -> str:
    """Convert time (int) to (string) more readable form."""

    str_row = str(row)
    if row > 999:
        return str_row[0] + str_row[1] + "." + str_row[2:]
    else:
        return str_row[0] + "." + str_row[1:]


def query1():
    """Query for canteens which are open 16.15-18.00."""

    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        result = session.query(Canteen).filter(Canteen.time_open < 1615, Canteen.time_closed > 1800)
    except:
        session.rollback()
        raise
    finally:
        session.close()

    # print out the query results
    count = 0
    print("Query for canteens which are open 16.15-18.00:\n")
    for row in result:
        print("id :", str(row.id) + "\n", "provider_id :", str(row.provider_id) + "\n", "name :", row.name + "\n",
              "location :", row.location + "\n",
              "time_open :", format_time(row.time_open) + "\n", "time_closed :", format_time(row.time_closed) + "\n")
        count += 1

    if count > 0:
        print(f"Operation done successfully. Found {count} canteen(s) which are open 16.15-18.00\n")
    else:
        print("Nothing was found\n")


def query2():
    """Query for canteens which are serviced by Rahva Toit."""

    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        result = session.query(Canteen, Provider, ).filter(Canteen.provider_id == Provider.id, ) \
            .filter(Provider.provider_name == 'Rahva Toit', ).all()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    # print out the query results
    count = 0
    print("Query for canteens which are serviced by Rahva Toit:\n")
    for row in result:
        print("id :", str(row[0].id) + "\n", "provider_id :", str(row[0].provider_id) + "\n", "name :",
              row[0].name + "\n",
              "location :", row[0].location + "\n", "provider_name :", row[1].provider_name + "\n",
              "time_open :", format_time(row[0].time_open) + "\n", "time_closed :", format_time(row[0].time_closed) + "\n")
        count += 1

    if count > 0:
        print(f"Operation done successfully. Found {count} canteens which are serviced by Rahva Toit\n")
    else:
        print("Nothing was found\n")


if __name__ == '__main__':
    create_records()
    query1()
    query2()
