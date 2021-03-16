import time
import re
import requests
from bs4 import BeautifulSoup

def build():
    #List of uncrawled websites.
    frontier = ["http://example.webscraping.com/"]

    inverted_indices = {}

    #Initialize the time counter.
    temp_time = time.perf_counter()

    num_Crawled = 0
    while num_Crawled < len(frontier):
        #Calculate the gap between two request, wait at least 5s between two requests.
        temp_time2 = temp_time
        temp_time = time.perf_counter()
        if (temp_time-temp_time2<5):
            time.sleep(5)

        print("Already crawled "+str(num_Crawled)+" webs.")
        #Fetch the last website from the web list.
        website = frontier[num_Crawled]
        print("Crawling "+website+"\n")
         
        #Make request and parse the return html file.
        r = requests.get(website)

        #If request is failed, try again.
        while (r.status_code != 200):
            print("Request for "+website+" is failed. Try again.")
            r = requests.get(website)
        soup = BeautifulSoup(r.text, 'html.parser')

        #All important messages are in table, so we only consider about table
        content = soup.find('table')

        tds = content.find_all('td')
        for td in tds:
            #Handle all a elements.
            hrefs = td.find_all('a')

            if hrefs != []:
                for href in hrefs:
                    #Add href to frontier
                    if href['href'] != None and frontier.count("http://example.webscraping.com"+href['href'])<1:
                        #print("Add http://example.webscraping.com"+href['href']+" to frontier")
                        frontier.append("http://example.webscraping.com"+href['href'])

                    #Add strings to inverted_indices
                    if href.text != None:
                        strings = re.split('[ :,]',href.text)
                        for string in strings:
                            if string in inverted_indices and string != '':
                                if website in inverted_indices[string]:
                                    inverted_indices[string][website] += 1
                                else:
                                    inverted_indices[string][website] = 1
                            else:
                                if string != '':
                                    inverted_indices[string] = {website:1}
            else:
                #handle the strings of text.
                if td.text != None:
                    strings = re.split('[ :,]',td.text)
                    for string in strings:
                        if string in inverted_indices:
                            if website in inverted_indices[string]:
                                inverted_indices[string][website] += 1
                            else:
                                inverted_indices[string][website] = 1
                        else:
                            if string != '':
                                inverted_indices[string] = {website:1}

        #Finish one crawling
        num_Crawled += 1

    #Store the inverted indices to file system.
    fout = open("inverted_indices.txt","w")
    for item in inverted_indices:
        string = item+' '+str(inverted_indices[item])
        print(string,file=fout)
    fout.close()

def load(inverted_indices):
    fin = open("inverted_indices.txt","r")
    print("\nLoading the index...\n")
    for line in fin.readlines():
        line = line.strip()
        strings = line.split(' ',1)
        #print(strings[0]+" "+strings[1])
        inverted_indices[strings[0]] = eval(strings[1])
    fin.close()
    print("Loading finished.\n")

def printValue(key, inverted_indices):
    if key in inverted_indices:
        items = inverted_indices[key]
        print("\nThe inverted index for "+key+" is:")
        for item in items:
            print(item+": "+str(inverted_indices[key][item]))
    else:
        print("Have no results of your print query.")

def findValues(query, inverted_indices):
    webDist = {}
    webs = []
    #find the webs containing all words.
    if len(query) == 1 and query[0] in inverted_indices:
        for web in inverted_indices[query[0]]:
            webs.append(web)
    elif len(query) > 1:
        for i in range(len(query)):
            if query[i] in inverted_indices:
                if i == 0:
                    for web in inverted_indices[query[i]]:
                        webs.append(web)
                else:
                    webs_temp = []
                    for web in inverted_indices[query[i]]:
                        if webs.count(web)>=1:
                            webs_temp.append(web)
                    webs = webs_temp
            else:
                webs = []
                break

    if webs == []:
        print("Have no results of your search query.")
        return 0
    else:
        #Transfer the web list to web dictionary
        for web in webs:
            webDist[web] = 0

    #Calculate the ranks of each web page.
    for word in query:
        for web in inverted_indices[word]:
            if web in webDist:
                webDist[web] += inverted_indices[word][web]

    #Sort the final results
    webDist=sorted(webDist.items(),key=lambda x:x[1],reverse=True)

    print("all pages containing words are: ")
    for web in webDist:
        print(web)

#The dictionary of inverted indice.
inverted_indices = {}

command = input("Please input command: ");
#The main loop of the program.
while str != "exit":
    commands = command.split(" ")

    if commands[0] == "build":
        build()
    elif commands[0] == "load":
        load(inverted_indices)
    elif commands [0] == "print":
        printValue(commands[1],inverted_indices)
    elif commands [0] == "find":
        del commands [0]
        findValues(commands, inverted_indices)
    elif commands[0] == "exit":
        break
    else:
        print("Please input correct command.")
    command = input("Please input command: ");
