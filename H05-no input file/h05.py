import sys
import utility
import heapq

class Webpage:
    def __init__(self, url, num_links, num_words, links, words, weight):
        self.url = url
        self.num_links = num_links
        self.num_words = num_words
        self.links = links
        self.words = words
        self.weight = weight

class SearchWord:
    def __init__(self, text, pages, num_pages):
        self.text = text
        self.pages = pages
        self.num_pages = num_pages

def printSearchResult(query):
    output = '0 pages match\n'
    if (query in wordmap):
        sw = searchwords[wordmap[query]]
        output = str(sw.num_pages) + " pages match\n\n"
        shownmatches = min(sw.num_pages, 5)
        filtered_webpages = [webpages[i] for i in sw.pages if i < len(webpages)]
        heaviest_pages = heapq.nlargest(shownmatches, filtered_webpages, key=lambda obj: obj.weight)
        for j in range(shownmatches):
            output += str(j + 1) + ". [" + str(round(heaviest_pages[j].weight, 3)) + "] " + heaviest_pages[j].url + "\n"
            index = heaviest_pages[j].words.index(query)
            if (index >= 5):
                output += heaviest_pages[j].words[index -  5] + " "
                output += heaviest_pages[j].words[index -  4] + " "
                output += heaviest_pages[j].words[index -  3] + " "
                output += heaviest_pages[j].words[index -  2] + " "
                output += heaviest_pages[j].words[index -  1] + " "
            else:
                for i in range(index):
                    output += heaviest_pages[j].words[i] + " "
                    
            output += heaviest_pages[j].words[index] + " "
            if (len(heaviest_pages[j].words) > index + 4):
                output += heaviest_pages[j].words[index + 1] + " "
                output += heaviest_pages[j].words[index + 2] + " "
                output += heaviest_pages[j].words[index + 3] + " "
                output += heaviest_pages[j].words[index + 4] + " "
            else:
                for i in range(index + 1, len(heaviest_pages[j].words)):
                    if (i == len(heaviest_pages[j].words) - 1):
                        output += heaviest_pages[j].words[i] + " "
                    else:
                        output += heaviest_pages[j].words[i] + " "
            output += "\n"
            
        # if sw.num_pages >= 2:
            # output += "2. [] " + webpages[sw.pages[1]].url + "\n\n"
        # if sw.num_pages >= 3:
            # output += "3. [] " + webpages[sw.pages[2]].url + "\n\n"
        # if sw.num_pages >= 4:
            # output += "4. [] " + webpages[sw.pages[3]].url + "\n\n"
        # if sw.num_pages >= 5:
            # output += "5. [] " + webpages[sw.pages[4]].url + "\n"
    print(output)

webpages = []
urlmap = {}
urlindex = 0
searchwords = []
wordmap = {}
wordindex = 0
totalWeight = 0

# Opens input file to read
input = open(sys.argv[1], 'r', encoding='utf-8')

print("Creating search engine...")

# Gets first line of input
line = next(input)
linenum = 0

# Using a try, can loop until the end of file, reading 3 lines at a time for each webpage
try:
    while True:
        # Gets to next entry, skipping newlines
        while (line == '\n'):
             line = next(input)
             linenum += 1

        # Checks the URL
        if line.startswith("URL: "):
             url = line[5:].strip()
        else:
             print("ERROR: Invalid input, line " + str(linenum))

        # Goes to next line, checks the content
        line = next(input)
        linenum += 1
        if line.startswith("CONTENT: "):
             content = line[9:].strip()
        else:
             print("ERROR: Invalid input, line " + str(linenum))

         # Goes to next line, checks the links
        line = next(input)
        linenum += 1
        if line.startswith("LINKS: "):
             linkstr = line[7:].strip()
        else:
             print("ERROR: Invalid input, line " + str(linenum))

        words = content.split(" ")
        words = list(filter(None, words))

        links = linkstr.split(" ")

        wp = Webpage(url, len(links), len(words), links, words, 1)
        webpages.append(wp)
        urlmap[url] = urlindex

        urlindex += 1
        totalWeight += 1

        # Adds word to the map and array of search words
        checked_words = {}
        for w in words:
            if w not in wordmap:
                wordmap[w] = wordindex
                searchwords.append(SearchWord(w, [urlmap[url]], 1))
                wordindex += 1
                checked_words[w] = 1
            elif w not in checked_words:
                searchwords[wordmap[w]].pages.append(urlmap[url])
                searchwords[wordmap[w]].num_pages += 1
                checked_words[w] = 1
        

        line = next(input)
        linenum += 1

except StopIteration:
        # End of file reached
        None

# Second run through loop - removing external URLS
for wp in webpages:
    for link in wp.links[:]:
         if link not in urlmap:
              wp.links.remove(link)
    wp.num_links = len(wp.links)


# Assigning page weight by running a loop 50 times
for k in range(50):
    new_weight = [0.1] * len(webpages)
    for i in range(len(webpages)):
        # oldWeight = i.weight
        # new_weight[i] = 0.1
        if webpages[i].num_links > 0:
            for j in webpages[i].links:
                new_weight[urlmap[j]] += 0.9 * webpages[i].weight / webpages[i].num_links
        else:
            new_weight[i] += webpages[i].weight * 0.9
        # i.weight = new_weight[i]
        # totalWeight += i.weight - oldWeight
    for i in range(len(webpages)):
        webpages[i].weight = new_weight[i]


print("Enter search word:")
utility.process_keystrokes(printSearchResult)
# word = "coffee"
# printSearchResult(word)