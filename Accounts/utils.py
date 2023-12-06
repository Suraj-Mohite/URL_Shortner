from bs4 import BeautifulSoup

def remove_html_tags(text):
    try:
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()

    except Exception as e:
        print(e)
        return None