import asyncio
import aiohttp
from random import choice, uniform
from db import connect, get_element, update_value, add_answer


async def fetch_content(query, engine, session, useragent=None, proxy=None):
    payload = "q={}".format(query[1])
    url = 'https://allo.ua/ua/catalogsearch/ajax/suggest/'
    headers = {
        'content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
    }
    if useragent:
        headers.update(useragent)

    await asyncio.sleep(uniform(2, 5))
    try:
        async with session.post(url, proxy=proxy, data=payload, headers=headers) as response:
            if response.status == 429:
                await asyncio.sleep(uniform(4, 7))
            else:

                    data = await response.json(content_type='text/html')
                    if isinstance(data, dict):
                        result = data.get('query', [])
                        for i in result:
                            await add_answer(engine, query[1], i)
                    await update_value(engine, query[0])
    except Exception as e:
        print(e)
        await asyncio.sleep(uniform(10, 20))


async def main(loop):
    engine = await connect()

    tasks = []
    check = True

    # useragents = open('./config/useragents.txt').read().split('\n')
    # proxies = open('./config/proxies.txt').read().split('\n')

    while check:
        list_query = await get_element(engine)
        if not list_query:
            break
        async with aiohttp.ClientSession() as session:
            while list_query:
                query = list_query.pop()
                # useragent = {'User-Agent': choice(useragents)}
                # proxy = 'http://' + choice(proxies)
                task = loop.create_task(fetch_content(
                    # useragent=useragent,
                    # proxy=proxy,
                    query=query,
                    engine=engine,
                    session=session))
                tasks.append(task)

            await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
