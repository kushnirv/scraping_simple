import string
import itertools
from aiopg.sa import create_engine
from models import data, answer
from decorator import decorator


@decorator
async def with_conn(func, *args, **kwargs):
    async with args[0].acquire() as conn:
        return await func(conn, *args[1:], **kwargs)

# async def with_conn(f):
#     async def wraps(*args, **kwargs):
#         async with args[0].acquire() as conn:
#             return await f(conn, *args[1:], **kwargs)
#     return wraps


async def connect():
    engine = await create_engine(
        user='postgres',
        database='allo',
        host='db',
        password='TESTtest'
    )
    return engine


@with_conn
async def drop_all_table(conn):
    await conn.execute('DROP TABLE IF EXISTS data')
    await conn.execute('DROP TABLE IF EXISTS answer')


@with_conn
async def create_all_table(conn):

    await conn.execute('''CREATE TABLE data (
                                id serial PRIMARY KEY,
                                request varchar(3),
                                status boolean DEFAULT False)''')
    await conn.execute('''CREATE TABLE answer (
                                    id serial PRIMARY KEY,
                                    request varchar(3),
                                    result varchar(256))''')


def combinations():
    for i in range(1, 4):
        yield from itertools.product(string.ascii_lowercase, repeat=i)


async def step(g):
    tasks_list = []
    for i in range(5000):
        try:
            query = ''.join(next(g))
            tasks_list.append({'request': query})
        except StopIteration:
            return None, tasks_list
    return True, tasks_list


@with_conn
async def insert_data(conn, list_tasks):
    await conn.execute(data.insert().values(list_tasks))


@with_conn
async def get_element(conn, limit=500):
    result = await conn.execute(
        data.select().where(
            data.c.status == False). \
            limit(limit)
    )
    return list(result)


@with_conn
async def update_value(conn, _id):
    await conn.execute(
        data.update(). \
            where(data.c.id == _id). \
            values(status=True)
    )


@with_conn
async def add_answer(conn, request, result):
    await conn.execute(
        answer.insert().values(request=request,
                               result=result)
    )
