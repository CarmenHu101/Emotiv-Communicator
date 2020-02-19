import asyncio
from lib.cortex import Cortex
import json
import pandas as pd
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)


# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


async def do_stuff(cortex):
    # await cortex.inspectApi()
    print("** USER LOGIN **")
    await cortex.get_user_login()
    print("** GET CORTEX INFO **")
    await cortex.get_cortex_info()
    print("** HAS ACCESS RIGHT **")
    await cortex.has_access_right()
    print("** REQUEST ACCESS **")
    await cortex.request_access()
    print("** AUTHORIZE **")
    await cortex.authorize()
    print("** GET LICENSE INFO **")
    await cortex.get_license_info()
    print("** QUERY HEADSETS **")
    await cortex.query_headsets()
    if len(cortex.headsets) > 0:
        print("** CREATE SESSION **")
        await cortex.create_session(activate=True,
                                    headset_id=cortex.headsets[0])
        print("** CREATE RECORD **")
        await cortex.create_record(title="test record 1")
        # print("** SUBSCRIBE POW & MET **")
        print("** SUBSCRIBE POW **")
        # await cortex.subscribe(['eeg', 'pow'])
        # "eeg", "mot", "dev", "pow", "met", "com",  "fac", "sys" https://emotiv.gitbook.io/cortex-api/data-subscription
        subscription_data = await cortex.subscribe(['met'])
        # pp.pprint(subscription_data)
        cols = subscription_data['result']['success'][0]['cols'] #=14

        data = []

        while cortex.packet_count < 25: #set the number of data

            new_data = await cortex.get_data()
            new_data = json.loads(new_data)
            # new_data = [i for i in new_data if isinstance(i, bool)]
            # filtered_data = []
            # for i in new_data:
            #     if type(i) == bool:
            #         filtered_data.append(i)
            data.append(new_data['met'])

        data = pd.DataFrame(data, columns=cols)
        print(data)
        data.to_csv('h.csv', index=True)
        # ghjgyh
            # await print(cortex.get_data)

        await cortex.inject_marker(label='halfway', value=1,
                                   time=cortex.to_epoch())
        while cortex.packet_count < 20:
            await cortex.get_data()
        await cortex.close_session()


def test():
    cortex = Cortex('./cortex_creds.txt')
    asyncio.run(do_stuff(cortex))
    cortex.close()


if __name__ == '__main__':
    test()
