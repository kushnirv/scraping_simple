from sqlalchemy import (
    MetaData, Table, ForeignKey,
    Integer, String, Boolean, Column
)

metadata = MetaData()

data = Table('data', metadata,

             Column('id', Integer, primary_key=True),
             Column('request', String(3)),
             Column('status', Boolean, nullable=False, default=False),
             )

answer = Table('answer', metadata,
               Column('id', Integer, primary_key=True),
               Column('request', String(3)),
               Column('result', String(256)),
               )
