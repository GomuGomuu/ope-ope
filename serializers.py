def recognizer_serializer(card_list):
    data = {"possible_cards": []}

    for card in card_list:
        print(card)
        data["possible_cards"].append(
            {
                "api_url": card["api_url"],
                "confidence": card["confidence"],
                "illustrations": card["illustrations"],
                "name": card["name"],
                "slug": card["slug"],
            }
        )

    return data
