import json
import argparse
import requests
from bs4 import BeautifulSoup

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-O', '--output_file', help='Output of program saved in json format', default='data.json')
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument('-U', '--url', help='URL for parsing', required=True)

    return parser.parse_args()


def save(dict_adress, filename):
    with open(filename, "w") as write_file:
        json.dump(dict_adress, write_file, indent=4)


def main():
    try:
        args = parse_arguments()
        url = args.url
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')

        set_urls = set()
        for i in soup.find_all('a', href=True):
            link = str(i.get('href'))
            if 'http' in link:
                set_urls.add(link)

        set_urls_pictures = set()
        for i in soup.find_all('img', src=True):
            link = str(i.get('src'))
            if 'http' in link:
                set_urls_pictures.add(link)

        output_dict = {"links": list(set_urls),
                       "images": list(set_urls_pictures)}
        save(output_dict, args.output_file)

    except ConnectionError:
        print("Please enter a valid URL")


if __name__ == '__main__':
    main()
