import requests
from bs4 import BeautifulSoup

def download_documents(url):
    # Send HTTP request and get HTML response
    response = requests.get(url)
    
    # Save the entire HTML content to a file
    with open('nextra_content.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    print("Downloaded the entire content of the page.")
    
    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all links on the webpage (you may need to adjust this based on your specific needs)
    links = soup.find_all('a')
    
    # Filter out non-document links (this might require adjusting based on how your target site structures its URLs)
    document_links = [link.get('href') for link in links if link.get('href') and ('.md' in link.get('href') or '.pdf' in link.get('href'))]
    
    # Download each document found
    for i, doc_link in enumerate(document_links):
        try:
            doc_response = requests.get(doc_link)
            if doc_response.status_code == 200:
                filename = f"document_{i+1}.md" if '.md' in doc_link else f"document_{i+1}.pdf"
                with open(filename, 'wb') as file:
                    file.write(doc_response.content)
                print(f"Downloaded {filename}")
            else:
                print(f"Failed to download {doc_link}")
        except Exception as e:
            print(f"Error downloading {doc_link}: {e}")

# Replace 'your_target_url' with the URL of the page containing document links
download_documents('https://nextra.site/docs/')
print("This code is designed to download documents from a specified URL. It sends an HTTP request to the URL, retrieves the HTML content, and parses it to find links to documents. The code then downloads each document found and saves it locally.")
