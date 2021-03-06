from python_translators.translation_costs import TranslationCosts
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse
from python_translators.translators.glosbe_translator import GlosbeTranslator
from torrequest import TorRequest


class GlosbeOverTorTranslator(GlosbeTranslator):

    def __init__(self, source_language: str, target_language: str, translator_name: str = 'Glosbe', quality: int = '50',
                 service_name: str = 'Glosbe') -> None:
        super(GlosbeOverTorTranslator, self).__init__(source_language, target_language, translator_name, quality, service_name)

    def reset_identity(self):
        with TorRequest() as tr:
            tr.reset_identity()

    def _translate(self, query: TranslationQuery) -> TranslationResponse:
        """

        :param query:
        :return:
        """

        # Construct url
        api_url = GlosbeTranslator.build_url(query.query, self.source_language, self.target_language)

        # Send request

        with TorRequest() as tr:
            response = tr.get(api_url).json()['tuc']

        # Extract the translations (thanks @SAMSUNG)
        translations = []
        try:
            for translation in response[:query.max_translations]:
                translations.append(self.make_translation(translation['phrase']['text']))

        except KeyError:
            pass

        return TranslationResponse(
            translations=translations,
            costs=TranslationCosts(
                money=0  # API is free
            )
        )
