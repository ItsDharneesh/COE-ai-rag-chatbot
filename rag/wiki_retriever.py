import wikipedia


def search_wikipedia(query):

    try:

        results = wikipedia.search(query)

        if len(results) == 0:
            return None

        page = wikipedia.page(results[0])

        content = page.content[:2000]

        return content

    except Exception:

        return None