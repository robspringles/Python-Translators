import math


class TranslationBudget(object):
    def __init__(self, money=math.inf, time=math.inf):
        self.money = money
        self.time = time

    def subtract_time(self, time):
        self.time -= time

    def is_unconstrained(self):
        return self.money == math.inf and self.time == math.inf


class TranslationQuery(object):
    def __init__(self,
                 query: str,
                 before_context: str = '',
                 after_context: str = '',
                 max_translations: int = 1,
                 budget: TranslationBudget = None):
        self.query = query
        self.before_context = before_context
        self.after_context = after_context
        self.max_translations = max_translations
        self.budget = budget

        if self.budget is None:
            self.budget = TranslationBudget(
                time=math.inf,
                money=math.inf,
            )

    def budget_is_unconstrained(self):
        return self.budget.is_unconstrained()

    @classmethod
    def for_word_occurrence(cls, query: str, context: str, word_index_for_query: int, max_translations: int = 1):

        """
            Useful when context is given as a single paragraph, but it's known which occurrence of
            the query is interesting (in the situation where there's multiple occurrences of query
            in the context)
        """
        before_context, after_context = context.split(query, word_index_for_query)
        return cls(query, before_context=before_context, after_context=after_context, max_translations=max_translations)

    @classmethod
    def for_word_at_index(cls, query: str, context: str, char_index: int, max_translations: int = 1):

        """
            Convenient when context is given as a whole.
            The char_index insures that in case of multiple occurrences of the query in the context
             the right one is being translated.
        """
        before_context, after_context = context[:char_index], context[:char_index+len(query)]
        return cls(query, before_context=before_context, after_context=after_context, max_translations=max_translations)

    @classmethod
    def one_context_and_word_index(cls, query: str, context: str, word_index_for_query: int, max_translations: int = 1):

        """

            Useful when context is given as a single paragraph, but it's known which occurrence of
            the query is interesting (in the situation where there's multiple occurrences of query
            in the context)

        """
        before_context, after_context = context.split(query, word_index_for_query)
        return cls(query, before_context=before_context, after_context=after_context, max_translations=max_translations)

    @classmethod
    def one_context_and_char_index(cls, query: str, context: str, char_index: int, max_translations: int = 1):

        """

            Convenient when context is given as a whole.

            The char_index insures that in case of multiple occurrences of the query in the context
             the right one is being translated.

        """
        before_context, after_context = context[:char_index], context[:char_index+len(query)]
        return cls(query, before_context=before_context, after_context=after_context, max_translations=max_translations)

    def is_context_aware_request(self):
        return self.before_context or self.after_context

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
