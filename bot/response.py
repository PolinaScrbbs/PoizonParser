import aiohttp
import xml.etree.ElementTree as ET
from .config import CURRENCY_API_URL


async def get_yuan_rate():
    async with aiohttp.ClientSession() as session:
        async with session.get(CURRENCY_API_URL) as response:
            if response.status == 200:
                xml_data = await response.text()
                root = ET.fromstring(xml_data)
                for item in root.findall(".//Valute"):
                    if item.find("CharCode").text == "CNY":
                        return float(item.find("Value").text.replace(",", "."))
            else:
                return "Не удалось получить данные о курсе"
