# Rust EAC Information 
## Install 
```
pip install rust-eac-information
```

## How to use?
Async method
```python
from eac_info import get_eac_info


async def foo():
    return await get_eac_info(76561198256263906)
```

Sync method
```python
import asyncio

from eac_info import get_eac_info

eac = asyncio.get_event_loop().run_until_complete(get_eac_info(76561198256263906))
```

Propertys
```python
eac.steamid  # 76561198256263906
eac.is_ban  # True
eac.ban_time  # datetime.datetime(2022, 7, 22, 0, 0)
eac.days_since_ban  # 26
eac.post_link  # https://twitter.com/rusthackreport/status/1550304891448557569?ref_src=twsrc%5Etfw
eac.nexus_link  # https://www.nexusonline.co.uk/bans/profile/?id=76561198256263906
```

# About
This script works with [nexus](https://www.nexusonline.co.uk/bans/) and simply converts the information into python objects. If the site does not work, then the script will stop functioning.

The author has nothing to do with the [nexus](https://www.nexusonline.co.uk)

