from bs4 import BeautifulSoup as SOUP
import re
import requests as HTTP
import time


def main(emotion):
    # Define URLs for different emotions
    urls = {
        "Sad": 'http://www.imdb.com/search/title?genres=drama&title_type=feature&sort=moviemeter,asc',
        "Disgust": 'http://www.imdb.com/search/title?genres=musical&title_type=feature&sort=moviemeter,asc',
        "Anger": 'http://www.imdb.com/search/title?genres=family&title_type=feature&sort=moviemeter,asc',
        "Anticipation": 'http://www.imdb.com/search/title?genres=thriller&title_type=feature&sort=moviemeter,asc',
        "Fear": 'http://www.imdb.com/search/title?genres=sport&title_type=feature&sort=moviemeter,asc',
        "Enjoyment": 'http://www.imdb.com/search/title?genres=thriller&title_type=feature&sort=moviemeter,asc',
        "Trust": 'http://www.imdb.com/search/title?genres=western&title_type=feature&sort=moviemeter,asc',
        "Surprise": 'http://www.imdb.com/search/title?genres=film_noir&title_type=feature&sort=moviemeter,asc'
    }

    # Check if the emotion is in our predefined URLs
    if emotion not in urls:
        print(f"No URL defined for emotion '{emotion}'")
        return []

    # Fetch the URL corresponding to the emotion
    url = urls[emotion]

    try:
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # HTTP request to get the data of the whole page with headers
        response = HTTP.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Parsing the data using BeautifulSoup
        soup = SOUP(response.text, "html.parser")

        # Extract movie titles from the data using regex
        titles = soup.find_all("a", attrs={"href": re.compile(r'\/title\/tt+\d*\/')})

        return titles

    except HTTP.RequestException as e:
        print(f"HTTP request failed: {e}")
        return []

    except Exception as e:
        print(f"Error occurred: {e}")
        return []


# Driver Function
if __name__ == '__main__':
    emotion = input("Enter the emotion: ")
    movie_titles = main(emotion)

    if not movie_titles:
        print(f"No movies found for emotion '{emotion}'")
    else:
        count = 0
        for title in movie_titles:
            # Extract text inside the anchor tag
            title_text = title.get_text()
            print(title_text)

            count += 1
            if emotion in ["Disgust", "Anger", "Surprise"] and count > 13:
                break
            elif count > 11:
                break

        # Add a delay after processing to avoid triggering rate limits or bot detection
        time.sleep(2)
