import os, sys, requests

import pandas as pd
import spacy

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# Handling of relative import
if __name__ == "__main__":
    sys.path.append(DIR_PATH)
    from secrets.keys import NEWS_API_KEY
else:
    from .secrets.keys import NEWS_API_KEY

# News module using NewsAPI

class NewsModule:

    # NewsAPI info
    top_news_url = 'https://newsapi.org/v2/top-headlines?'

    CATEGORIES = ['general', 'business', 'entertainment', 'health', 'science', 'sports', 'technology']

    api_key = NEWS_API_KEY

    # SpaCy similarity checking
    nlp_model = spacy.load("en_core_web_md")
    similarity_thresh = 0.8

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

    def _group_by_similarity(self, sentences, threshold=0.9, return_all=True):
        sentence_groups = {}

        # Build sentence : vector dictionary
        sentence_dict = {}
        for sentence in sentences:
            sentence_dict[sentence] = self.nlp_model(sentence)

        for sentence in sentences:
            # Only use sentence if it has not been removed (grouped)
            if sentence in sentence_dict.keys():
                group = []

                # Get vector representation of sentence

                vec_sent = sentence_dict[sentence]

                # Remove the current sentence from the dictionary to ensure no comparing with itself
                sentence_dict.pop(sentence)

                for compared_sent, vec_comp_sent in sentence_dict.items():
                    # Check similarity between current sentence and compared sentence
                    similarity = vec_sent.similarity(vec_comp_sent)
                    
                    # If the threshold is greater than the threshold then group them
                    if similarity >= threshold:
                        group.append(compared_sent)

                # Remove the grouped sentences
                for grouped_sent in group: sentence_dict.pop(grouped_sent)

                sentence_groups[sentence] = group

        if return_all:
            return sentence_groups
        else:
            # Only return the first of the group
            return list(sentence_groups.keys())

    def get_headline_titles(self, country=None, category='general', check_similarity=True):
        j = self.query_articles(country, category)
        output = self._extract_titles(j)
        if check_similarity:
            output = self._group_by_similarity(output, self.similarity_thresh, False)
        return output

    def get_headline_titles_by_source(self, source='bbc-news', check_similarity=True):
        j = self.query_articles_by_source(source)
        output = self._extract_titles(j)
        if check_similarity:
            output = self._group_by_similarity(output, self.similarity_thresh, False)
        return output

# Testing

if __name__ == '__main__':
    mod = NewsModule()
    # print(mod.query_headlines(country='SG'))
    # print(mod.get_headline_titles(country='uk', category='general'))
    # print(mod.get_headline_titles_by_source(source='bbc-news', check_similarity=False))
    print(mod.get_headline_titles_by_source(source='bbc-news', check_similarity=True))