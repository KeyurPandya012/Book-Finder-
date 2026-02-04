import requests
import json

def test_isbn(isbn):
    print(f"Testing ISBN: {isbn}")
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=details&format=json"
    resp = requests.get(url)
    data = resp.json()
    key = f"ISBN:{isbn}"
    if key in data:
        details = data[key]
        print("Found details.")
        if 'description' in details:
            print(f"Description found: {str(details['description'])[:100]}...")
        else:
            print("NO DESCRIPTION in Edition.")
            if 'works' in details:
                print(f"Found works: {details['works']}")
                work_key = details['works'][0]['key']
                print(f"Fetching Work: {work_key}")
                work_url = f"https://openlibrary.org{work_key}.json"
                w_resp = requests.get(work_url)
                w_data = w_resp.json()
                if 'description' in w_data:
                     print(f"WORK Description found: {str(w_data['description'])[:100]}...")
                else:
                    print("No description in Work either.")
            else:
                print("No 'works' key found.")
    else:
        print("ISBN not found in OpenLibrary.")

# Example ISBNs from known datasets or common books
test_isbn("9780132350884") # Clean Code
test_isbn("0849334047") # Network design (failed in previous log)
