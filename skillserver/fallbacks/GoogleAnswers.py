from fallbacks.Scraper import scrape


class Result:
    def __init__(self, query, scraper_results):
        self.query = query
        self.results = scraper_results

        if len(self.results) > 0:
            self.string = '\n'
            self.string += '{0}'.format(self.results[0]).replace('  ', ' ')
        else:
            self.string = "Error"

    def __str__(self):
        return self.string


def ask(query, lang = "en"):
    url = convert_query(query, lang)
    result = Result(query, scrape(url))
    return result


def convert_query(query, lang):
    result = query
    result = result.replace(' ', '+')
    result = result.replace('?', '')
    result = "http://www.google.com/search?q=" + result + "&lr=lang_" + lang + "&hl=" + lang
    return result
