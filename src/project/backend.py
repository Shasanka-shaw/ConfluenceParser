import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from project.parse import getRawHtml



def parseTable(table):
    rows = table.find_all("tr")
    if not rows:
        return {}
    headers = [
        cell.get_text(" ", strip=True)
        for cell in rows[0].find_all(["th", "td"])
    ]
    table_rows = []
    for row in rows[1:]:
        cells = [
            cell.get_text(" ", strip=True)
            for cell in row.find_all(["td", "th"])
        ]
        if not cells:
            continue
        row_data = {}
        for i, value in enumerate(cells):
            if i < len(headers):
                row_data[headers[i]] = value
        table_rows.append(row_data)
    return {
        "rows": table_rows
    }
def parseConfluence(url):

    raw_html=getRawHtml(url)
    soup = BeautifulSoup(raw_html, "html.parser")
  
    for element in soup(["script", "style", "nav", "footer"]):
        element.decompose()
    sections = {}
    current_heading = None
    current_content = []
    current_tables = []
    current_images = []
    current_svg = ""


    #for loop
    for element in soup.find_all(
        ["h1", "h2", "h3", "h4", "p", "li", "table","img","div"]
    ):
        #parsing table
        if element.name == "table":
            table_data = parseTable(element)
            if current_heading:
                current_tables.append(table_data)
            continue


        #handling macros
        if (
            element.name == "div"
            and element.get("id")
            and element.get("id").startswith("drawio-macro-content-")
        ):
            img = element.find("img")
            if img and img.get("src"):
                img_src = img.get("src")
                img_src = urljoin(url, img_src)
                current_images.append(img_src)

           
            svg = element.find("svg")

            if svg:
                current_svg=svg
            continue
        else :
            text = element.get_text(" ", strip=True)
            if not text:
                continue    
            if element.name in ["h1", "h2", "h3", "h4"]:
                if current_heading:
                    sections[current_heading] = {
                        "content": " ".join(current_content),
                        "tables": current_tables,
                        "figures":{"images":current_images,
                                "svg":current_svg
                                }
                    }

                current_heading = text
                current_content = []
                current_tables = []
                current_images=[]
                current_svg=""
            elif element.name not in ["table","div"]:
                current_content.append(text)
    if current_heading:
        sections[current_heading] = {
            "content": " ".join(current_content),
            "tables": current_tables,
            "figures":{"images":current_images,
                       "svg":current_svg
                       }
        }
    return sections