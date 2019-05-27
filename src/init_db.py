import asyncio
from db import connect, create_all_table, drop_all_table, combinations, step, insert_data
from time import time


async def main(loop):
    engine = await connect()
    tasks = []
    await drop_all_table(engine)
    await create_all_table(engine)

    g = combinations()
    check = True

    while check:
        check, list_tasks = await step(g)
        task = loop.create_task(insert_data(engine, list_tasks))
        tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == '__main__':
    start = time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
    print(time() - start)
