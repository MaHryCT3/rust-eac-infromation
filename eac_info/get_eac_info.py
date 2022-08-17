from datetime import datetime
from typing import Optional, TypeAlias, Mapping

import aiohttp
from bs4 import BeautifulSoup as BS

from eac_info.model import EACInfo
from eac_info.exceptions import CantGetEacInfo, SteamIsNotFound

__all__ = ["get_eac_info"]

ResponseText: TypeAlias = str

LINK = "https://www.nexusonline.co.uk/bans/profile/?id={steamid}"


async def get_eac_info(
    steamid: int, *, session: Optional[aiohttp.ClientSession] = None
) -> EACInfo:
    """Returns all infromation about the given steamid.

    Args:
        steamid: int - steamid of user
        session: Optional[aiohttp.ClientSession] - if you will be making multiple requests, recommend using your session
    """
    nexus_link = LINK.format(steamid=steamid)
    soup = await _get_eac_soup(link=nexus_link, session=session)
    return _parse_soup(soup=soup, steamid=steamid, nexus_link=nexus_link)


async def _get_eac_soup(link: str, session: aiohttp.ClientSession) -> BS:
    """Returns BeautifulSoup instance"""
    if session is None:
        async with aiohttp.ClientSession() as session:
            text = await _get_request(link, session)
    else:
        text = await _get_request(link, session)
    return BS(text, "lxml")


async def _get_request(link: str, session: aiohttp.ClientSession) -> ResponseText:
    """Makes a get request on the given link."""
    try:
        async with session.get(link) as response:
            return await response.text()
    except aiohttp.ClientError as e:
        raise CantGetEacInfo(
            "Failed to get information about eac. Check if the data is correct"
        )


def _parse_soup(soup: BS, steamid: int, nexus_link: str) -> EACInfo:
    """Parse BeautifulSoup instance"""
    if not _is_eac_banned(soup):
        return _not_banned_model(steamid)

    twitter_post = _find_twitter_post_info(soup)
    twitter_link = twitter_post["href"]
    ban_time = _get_datetime_from_string(twitter_post.text)
    days_since_ban = _get_days_since_ban(ban_time)
    return _banned_model(
        steamid=steamid,
        ban_time=ban_time,
        days_since_ban=days_since_ban,
        post_link=twitter_link,
        nexus_link=nexus_link,
    )


def _get_datetime_from_string(string: str) -> datetime:
    """Returns datetime instanse from format: month day, year"""
    timestamp = datetime.strptime(string, "%B %d, %Y")
    return timestamp


def _get_days_since_ban(ban_time: datetime) -> int:
    """Returns the number of days that have passed since the ban"""
    today = datetime.now()
    delta = today - ban_time
    return delta.days


def _find_twitter_post_info(soup: BS) -> Mapping:
    """Found a twitter post info with link to twitter and time when was banned."""
    links = soup.find("blockquote", class_="twitter-tweet").find_all("a", href=True)
    for link in links:
        if "twitter.com/rusthackreport/" in link["href"]:
            return link
    raise CantGetEacInfo("Can't find link to twitter post")


def _is_eac_banned(soup: BS) -> bool:
    """Checks have user ban or not"""
    banned_info = soup.find("span", class_="header")
    try:
        if "is currently game banned!" in banned_info.text:
            return True
        return False
    except AttributeError:
        raise SteamIsNotFound("Profile for this steamid is not found")


def _not_banned_model(steamid: int) -> EACInfo:
    return EACInfo(
        steamid=steamid,
        is_ban=False,
    )


def _banned_model(
    steamid: int,
    ban_time: datetime,
    days_since_ban: int,
    post_link: str,
    nexus_link: str,
) -> EACInfo:
    return EACInfo(
        steamid=steamid,
        is_ban=True,
        ban_time=ban_time,
        days_since_ban=days_since_ban,
        post_link=post_link,
        nexus_link=nexus_link,
    )
