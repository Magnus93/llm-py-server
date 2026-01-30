import wikipedia
import wikipediaapi



wikipedia.set_lang("en")

results = wikipedia.search("python programming")

wiki = wikipediaapi.Wikipedia(language="en", user_agent="llm-py-server/0.1 (contact: magnus.ja.gustafsson@gmail.com)")

page = wiki.page(results[0])
print(page.text)