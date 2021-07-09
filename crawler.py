import random
import requests
import json
from bs4 import BeautifulSoup


# Retrieve the overview of the CWE collection (A list of URLs)

# url = 'https://cwe.mitre.org/data/definitions/1000.html'
# page = requests.get(url).text                            # Retrieve the weakness list page content (html)
# soup = BeautifulSoup(page, 'html.parser')                # Parse into HTML page object
# list_item = [p.text for p in soup.find_all(class_='cweid Primary')]    # Get all weakness items in a list
# set_id = set([item.strip(' - ').strip('()') for item in list_item])
# list_id = sorted([int(ids) for ids in set_id])           # Remove punctuation and get only ID number
list_id = [9, 32, 106, 168, 194, 211, 266, 284, 317, 327, 368, 406, 447, 453, 476, 537, 576, 606, 665, 669, 688, 704, 710, 779, 829, 833, 1124, 1234, 1239, 1322]
# list_url = ['https://cwe.mitre.org/data/definitions/' + str(id_item) + '.html' for id_item in list_id] 


def retrieve_entry(url, id_item):
    data = {}
    # Get a page content for each CWE entry
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")

    # Align the scrapped data to a dictionary
    data['id'] = id_item
    data['name'] = soup.find('h2').contents[0]
    data['description'] = process_desc(
        soup.find(id="oc_"+str(id_item)+"_Description"))
    data['ext_description'] = process_desc(
        soup.find(id="oc_"+str(id_item)+"_Extended_Description"))
    data['demonstrative_examples'] = process_desc(
        soup.find(id="oc_"+str(id_item)+"_Demonstrative_Examples"))

    return data


def process_desc(soup):
    if soup is not None:
        return " ".join([repr(r).strip(
            "''") for r in soup.find(class_="detail").div.stripped_strings])
    else:
        return ""


def main():

    n = [x for x in list_id if x not in [211, 284, 317, 688, 704]]

    ibm = [211, 317, 688]
    s = random.sample(n, k = 7)
    ibm.extend(s)
    ibm = sorted(ibm)

    sovrin = [211, 317, 704]
    s2 = random.sample([x for x in n if x not in s], k=7)
    sovrin.extend(s2)
    sovrin = sorted(sovrin)

    uport = [211, 284, 317]
    s3 = random.sample([x for x in n if x not in s2], k=7)
    uport.extend(random.sample(n, k=7))
    uport = sorted(uport)

    with open('./intermediate files/cwe-case.json', 'r') as file:
        data = json.load(file)
        file.close()

    t_ibm = []
    t_sov = []
    t_upo = []
    for d in data:

        if d["id"] in ibm:
            if(d["id"] in [211, 317, 688]):
                t_ibm.append(True == d["truth"])
            else:
                t_ibm.append(False == d["truth"])

        if d["id"] in sovrin:
            if(d["id"] in [211, 317, 704]):
                t_sov.append(True == d["truth"])
            else:
                t_sov.append(False == d["truth"])

        if d["id"] in uport:
            if(d["id"] in [211, 284, 317]):
                t_upo.append(True == d["truth"])
            else:
                t_upo.append(False == d["truth"])

    print("IBM:\n {} \n {}".format(ibm, t_ibm))
    print("Sovrin:\n {} \n {}".format(sovrin, t_sov))
    print("Uport:\n {} \n {}".format(uport, t_upo))

    # rand = random.sample(list_id, k=30)
    # print(sorted(rand))
    

    # with open('./intermediate files/cwe.json', 'r') as file:
    #     data = json.load(file)
    #     file.close()

    # countAll = 0
    # countCode = 0
    # for ent in data:
    #     if ent["demonstrative_examples"] != "":
    #         countCode += 1
    #     countAll += 1


    # print("Count Code: {}".format(countCode))
    # print("All Entries: {}".format(countAll))
    # list_entry = [retrieve_entry(url, list_id[index])
    #           for index, url in enumerate(list_url)]

    # jsonString = json.dumps(list_entry)
    # with open("./intermediate files/cwe-case.json", 'w') as file:
    #     file.write(jsonString)
    #     file.close()

if __name__ == '__main__':
    main()