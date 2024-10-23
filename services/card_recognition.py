import datetime
import json

import google.generativeai as genai
import os
from dotenv import load_dotenv
import typing_extensions as typing
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from google.generativeai import caching

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def create_cache(cache_name):
    with open("../data/merry_cards_data_dump.json") as f:
        json_data = json.load(f)

    json_string = json.dumps(json_data)
    print(f"JSON data: {json_string[:100]}...")

    print(f"Creating cache: {cache_name}")
    cache = caching.CachedContent.create(
        model="models/gemini-1.5-flash-001",
        system_instruction=(
            "You have all cards data in cache. "
            "And you are a expert comparing not formatted data with the cards data in cache."
            "And your job is to answer the user's query based on the data in cache."
        ),
        display_name=cache_name,
        contents=[json_string],
        ttl=datetime.timedelta(hours=1),
    )
    print(f"Cache created: {cache}")

    model = genai.GenerativeModel.from_cached_content(cached_content=cache)
    print(f"Model created: {model}")

    return cache.name.split("/")[1]


def extract_text_from_image(image_path):
    card_file = genai.upload_file(image_path)
    model = genai.GenerativeModel("gemini-1.5-flash")

    class ResponseFormat(typing.TypedDict):
        life: int
        attack: int
        cost: int
        counter: int
        type: str
        name: str
        tribe: str
        description: str
        trigger: str

    print(f"Extracting text from image: {image_path}")
    response = model.generate_content(
        [
            "You are a expert extracting text from images.",
            "Extract the maximum text possible from this image.",
            "Do not generate random values, just extract the text from the image.",
            "Send me JSON format",
            card_file,
        ],
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=ResponseFormat
        ),
    )

    print(f"Card extracted: {response.text}")

    return response.text


def get_card_from_ia(cache_name, data_fragment):
    print(f"Retrieving cache: {cache_name}")
    cache = caching.CachedContent.get(name=cache_name)

    print(f"Cache retrieved: {cache.name}")

    model = genai.GenerativeModel.from_cached_content(cached_content=cache)
    print(f"Model created: {model}")

    class Illustration(typing.TypedDict):
        code: str
        src: str
        external_link: str

    class Card(typing.TypedDict):
        api_url: str
        name: str
        slug: str
        illustrations: typing.List[Illustration]
        confidence: float

    class ResponseFormat(typing.TypedDict):
        possible_cards: typing.List[Card]

    print(f"Extracting card from cache: {cache_name}")
    response = model.generate_content(
        [
            "I extract these data fragments from an image, based on the cached data,"
            "which cards are closest to this data? "
            "Return a list of possible cards with their confidence, sorted by confidence.",
            "Max 5 possible cards",
            f"Data fragments: {data_fragment}",
        ],
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=ResponseFormat
        ),
    )

    print(f"Card found: {response.text}")

    return response.text


def slugify(image_path):
    return image_path.split("/")[-1].split(".")[0]


def recognize_card_from_image(image_path):
    MODEL_CACHE_NAME = "4r4rxradrhod"

    _data = extract_text_from_image(image_path)
    _result = get_card_from_ia(cache_name=MODEL_CACHE_NAME, data_fragment=_data)

    slug = slugify(image_path)
    try:
        with open(f"data/processing_output/{slug}.json", "w") as json_file:
            json_file.write(
                json.dumps(
                    {
                        "extracted_data": json.loads(_data),
                        "search_result": json.loads(_result),
                    },
                    indent=4,
                )
            )
    except Exception as e:
        print(json.loads(_result))
        print(f"Error writing file: {e}")

    return json.loads(_result)


if __name__ == "__main__":
    print("Initializing cache")
    print(f"Cache name: {create_cache("Ope-Ope-no-Mi")}")
