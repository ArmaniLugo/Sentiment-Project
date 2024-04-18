import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import tkinter as tk

positive_threshold = 0.0


def main():
    global article_input, url_input, polarity_label

    window = tk.Tk()

    # Article text region
    tk.Label(window, text='Copy & paste passage:').grid(row=0, column=0, pady=5)
    article_input = tk.Text(window, width=60, height=20)
    article_input.grid(row=1, column=0, rowspan=2)

    # Analyze button and results from analysis
    tk.Button(window, text='Analyze Article', command=analyze_article).grid(row=1, column=1)
    polarity_label = tk.Label(window, text='')
    polarity_label.grid(row=2, column=1, padx=30)

    # Url text region and button
    tk.Label(window, text='Or insert URL to fetch:').grid(row=3, column=0, pady=5)
    url_input = tk.Text(window, width=60, height=1)
    url_input.grid(row=4, column=0)

    tk.Button(window, text='Fetch URL', command=fetch_url).grid(row=4, column=1)

    window.mainloop()


def analyze_article():
    global article_input, polarity_label

    # Get user provided article (or pulled from URL)
    user_input = article_input.get(1.0, tk.END)

    # Have TextBlob calculate polarity (positive/negative)
    blob = TextBlob(user_input)
    polarity = blob.polarity

    # Determine if article should be retweeted based on threshold
    result = 'Retweet' if polarity >= positive_threshold else "Don't retweet"

    # Update label's text
    polarity_label.configure(text=f'Polarity: {get_mood(polarity)}\nResult: {result}')


# Returns a string based on the polarity of the given float, ranging from [-1.0, 1.0]
def get_mood(polarity):
    if polarity > 0.6:
        return 'positive'
    elif polarity > 0.2:
        return 'mostly positive'
    elif polarity > -0.2:
        return 'neutral'
    elif polarity > -0.4:
        return 'mostly negative'
    else:
        return 'negative'


def fetch_url():
    global article_input, url_input

    # Get user provided url
    url = url_input.get(1.0, tk.END).strip()

    try:
        # Get HTML from given url
        response = requests.get(url)
        html = response.text

        # Convert HTML into plain, readable text
        soup = BeautifulSoup(html, features='html.parser')
        parsed_article = soup.get_text()

        # Overwrite article input text region
        article_input.delete(1.0, tk.END)
        article_input.insert(tk.INSERT, parsed_article)

    except:
        print(f'Error: unable to fetch url at "{url}"')


if __name__ == '__main__':
    main()