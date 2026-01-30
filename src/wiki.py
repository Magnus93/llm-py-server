import wikipedia
import wikipediaapi



wikipedia.set_lang("en")

results = wikipedia.search("python programming")

wiki = wikipediaapi.Wikipedia(language="en", user_agent="llm-py-server/0.1 (contact: magnus.ja.gustafsson@gmail.com)")

for result in results:
    page = wiki.page(result)
    print(f"\n======= {page.title} =======")
    print(page.summary)
    print(page.text)
    print(page.pageid)