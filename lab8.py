import asyncio
import logging
import re
import pytesseract
from PIL import Image
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
import phonenumbers
from phonenumbers import carrier, geocoder

API_TOKEN = '8625885247:AAHsPgATUOsEDTC8341JD1jhUwsDqZ89ItQ'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def identify_phone_data(phone_str):
    try:
        parsed_number = phonenumbers.parse(phone_str, "UA")
        
        if not phonenumbers.is_valid_number(parsed_number):
            return "Номер не валідний або не розпізнаний."

        country = geocoder.country_name_for_number(parsed_number, "uk")
        
        if country == "Україна":
            is_mobile = phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE
            
            if is_mobile:
                operator = carrier.name_for_number(parsed_number, "uk")
                return f"Країна: {country}\nТип: Мобільний\nОператор: {operator}"
            else:
                region = geocoder.description_for_number(parsed_number, "uk")
                return f"Країна: {country}\nТип: Стаціонарний\nМісто/Область: {region}"
        else:
            return f"Країна: {country}"
    except Exception:
        return "Не вдалося розпізнати номер."

@dp.message(F.photo)
async def handle_photo(message: Message):
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, "input.jpg")
    
    text = pytesseract.image_to_string(Image.open("input.jpg"))
    
    phone_numbers = re.findall(r'\+?\d[\d\s\-()]{7,}\d', text)
    
    if phone_numbers:
        result = identify_phone_data(phone_numbers[0])
        await message.answer(f"Розпізнано: {phone_numbers[0]}\n{result}")
    else:
        await message.answer("Номер телефону на фото не знайдено.")

@dp.message(F.text)
async def handle_text(message: Message):
    phone_numbers = re.findall(r'\+?\d[\d\s\-()]{7,}\d', message.text)
    
    if phone_numbers:
        result = identify_phone_data(phone_numbers[0])
        await message.answer(result)
    else:
        await message.answer("Надішліть номер телефону (текстом або фото).")

async def main():
    print("Бот готовий до роботи!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())