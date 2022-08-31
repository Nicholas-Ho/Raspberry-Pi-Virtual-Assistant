import os, sys, requests

import pandas as pd

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# Handling of relative import
if __name__ == "__main__":
    sys.path.append(os.path.dirname(DIR_PATH))
    from secrets.keys import NEWS_API_KEY
else:
    from .secrets.keys import NEWS_API_KEY

# News module using NewsAPI

class NewsModule:

    top_news_url = 'https://newsapi.org/v2/top-headlines?'

    CATEGORIES = ['general', 'business', 'entertainment', 'health', 'science', 'sports', 'technology']

    api_key = NEWS_API_KEY

    # Query raw data. Only passing country and category
    def query_articles(self, country=None, category='general'):
        first_arg = True
        url = self.top_news_url
        if country:
            url += f'country={country}'
            first_arg = False
        if category:
            if not first_arg: url += '&'
            url += f'category={category}'
            first_arg = False
        url += f'&apiKey={self.api_key}'

        response = requests.get(url)

        return response.json()['articles']

    # Query raw data. Only pass in source as it is incompatible with the other arguments country and category
    def query_articles_by_source(self, source='bbc-news'):
        first_arg = True
        url = self.top_news_url + f'sources={source}&apiKey={self.api_key}'

        response = requests.get(url)

        return response.json()['articles']

    def _extract_titles(self, j):
        df = pd.DataFrame(j)
        titles = df['title'].values

        output = []

        for title in titles:
            if ' - ' in title: title = title.rpartition(' - ')[0]
            # Replacing these helps the TTS to be more understandable
            title = title.replace('US', 'U.S.')
            output.append(title)

        return output

    def get_headline_titles(self, country=None, category='general'):
        j = self.query_articles(country, category)
        output = self._extract_titles(j)
        return output

    def get_headline_titles_by_source(self, source='bbc-news'):
        j = self.query_articles_by_source(source)
        output = self._extract_titles(j)
        return output

# Testing

if __name__ == '__main__':
    mod = NewsModule()
    # print(mod.query_headlines(country='SG'))
    # mod.get_headline_titles(country='uk', category='general')
    print(mod.get_headline_titles_by_source(source='bbc-news'))