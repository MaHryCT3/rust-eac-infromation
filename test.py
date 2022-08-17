from eac_info import get_eac_info

import asyncio


a = asyncio.get_event_loop().run_until_complete(get_eac_info(76561198256263906))
print(a)
