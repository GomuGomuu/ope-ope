import json
import os
from sentence_transformers import SentenceTransformer, util

from utils import Logger

logger = Logger()


class CardMatcher:
    def __init__(
        self,
        model_name="paraphrase-MiniLM-L6-v2",
        data_file="data/merry_cards_data_dump.json",
        cache_file="data/merry_cards_embeddings_cache.json",
    ):
        # Inicializa o modelo e carrega os dados
        self.model = SentenceTransformer(model_name)
        self.data_file = data_file
        self.cache_file = cache_file
        self.cards = self._load_cards()

    def _load_cards(self):
        with open(self.data_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _create_card_embedding(self, carta):
        logger.info(f"Creating card embedding for {carta['name']}")
        texts = [
            carta["name"],
            carta["effect"],
            " ".join([crew["name"] for crew in carta["crew"]]),
            carta["type"],
            str(carta["power"]),
            str(carta["cost"]),
        ]
        card_text = " ".join([text for text in texts if text])
        return self.model.encode(card_text)

    def cache_card_embeddings(self):
        if os.path.exists(self.cache_file):
            logger.info("Cache already exists")
            with open(self.cache_file, "r", encoding="utf-8") as f:
                cached_embeddings = json.load(f)
                return cached_embeddings
        else:
            logger.info("Creating cache")
            cached_embeddings = {}

        # Gera embeddings para as cartas que ainda não estão no cache
        for card in self.cards:
            if card["slug"] not in cached_embeddings:
                card_embedding = self._create_card_embedding(card).tolist()
                cached_embeddings[card["slug"]] = card_embedding

        # Salva os embeddings no cache
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(cached_embeddings, f)

        logger.info("Cache created")
        return cached_embeddings

    def _create_extracted_embedding(self, extracted_data):
        texts = [
            extracted_data.get("name"),
            extracted_data.get("description"),
            extracted_data.get("tribe"),
            extracted_data.get("type"),
        ]
        extracted_text = " ".join([text for text in texts if text])
        return self.model.encode(extracted_text)

    def find_closest_card(self, extracted_data, cached_embeddings=None):
        logger.info("Finding closest card")
        extracted_embedding = self._create_extracted_embedding(extracted_data)

        # Carrega o cache de embeddings se ainda não estiver em memória
        if cached_embeddings is None:
            logger.info("Loading embeddings cache")
            with open(self.cache_file, "r", encoding="utf-8") as f:
                cached_embeddings = json.load(f)

        best_match = None
        best_similarity = -1

        # Compara o embedding extraído com os embeddings das cartas
        for card in self.cards:
            card_embedding = cached_embeddings[card["slug"]]
            similarity = util.pytorch_cos_sim(
                extracted_embedding, card_embedding
            ).item()

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = card
        card = {}
        card.update(best_match)
        card.update({"confidence": best_similarity})
        logger.info("Best match found")
        return card

    def find_closest_cards(self, extracted_data, cached_embeddings=None, top_n=5):
        logger.info("Finding closest cards")
        extracted_embedding = self._create_extracted_embedding(extracted_data)

        # Carrega o cache de embeddings se ainda não estiver em memória
        if cached_embeddings is None:
            logger.info("Loading embeddings cache")
            with open(self.cache_file, "r", encoding="utf-8") as f:
                cached_embeddings = json.load(f)

        # Lista para armazenar as cartas com suas similaridades
        similarities = []

        # Compara o embedding extraído com os embeddings das cartas
        for card in self.cards:
            card_embedding = cached_embeddings[card["slug"]]
            similarity = util.pytorch_cos_sim(
                extracted_embedding, card_embedding
            ).item()

            # Adiciona a carta e sua similaridade à lista
            similarities.append({"card": card, "similarity": similarity})

        # Ordena as cartas pela similaridade em ordem decrescente
        similarities = sorted(similarities, key=lambda x: x["similarity"], reverse=True)

        # Retorna até `top_n` cartas mais similares
        top_matches = similarities[:top_n]

        # Atualiza as cartas retornadas com a confiança (similaridade)
        top_cards = [
            {**match["card"], "confidence": match["similarity"]}
            for match in top_matches
        ]

        logger.info(f"Top {top_n} matches found")
        return top_cards


# Exemplo de uso
if __name__ == "__main__":
    card_matcher = CardMatcher()

    # Cachear os embeddings das cartas
    card_matcher.cache_card_embeddings()

    # Exemplo de dados extraídos de OCR
    extracted_data = {
        "name": 'Eustass "Captain" Kid',
        "description": "On Play / When Attacking DON!! -1 (You may return the specified number of DON!! cards from your field to your DON!! deck.): Up to 1 of your Leader gains +1000 power until the start of your next turn.",
        "tribe": "Kid Pirates",
        "type": "CHARACTER",
    }

    # Encontrar a carta mais próxima
    closest_card = card_matcher.find_closest_card(extracted_data)

    logger.info(
        f"Melhor correspondência: {closest_card['name']} ({closest_card['slug']}) "
        f"com similaridade {closest_card['confidence']}"
    )
