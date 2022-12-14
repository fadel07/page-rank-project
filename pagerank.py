import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    
    #Return a dictionary where each key is a page, and values are
    #a list of all other pages in the corpus that are linked to by the page.
    
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor,num_of_decimal=5):
    
    #Return a probability distribution over which page to visit next,
    #given a current page.
    
    #creating defult dict with 0 value for each page
    new_dict = {page:0 for page in corpus}
    
    #probability that the surfer should randomly choose one of all pages
    prob_random = float((1-damping_factor)/len(corpus))
    
    #probability that the  surfer should randomly choose one of the links from "page"
    if len(corpus[page]) == 0:
        prob_dam = float(damping_factor/len(corpus))
    else:
        
        prob_dam = float(damping_factor/len(corpus[page]))

    #iterate over all the pages in the courpus, if the page existed in the linked pages of "page" then add the prob_random
    #and the prob_dam, else, add only the prob_random
    for key in new_dict:
        
        if key in corpus[page]:
            new_dict[key] += round((prob_random + prob_dam),num_of_decimal)
        else:
            new_dict[key] += round(prob_random,num_of_decimal)
    
    return new_dict


def sample_pagerank(corpus, damping_factor, n):
    
    #Return PageRank values for each page by sampling `n` pages
    #according to transition model, starting with a page at random.

    #generating random sample from a list contains all the pages
    random_sample = random.choice([ key for key,value in corpus.items()])
    
    #generating new dict with keys are the pages and values are 0
    new_dict = {page:0 for page in corpus}
    
    #calculating the occurance of the random sample
    new_dict[random_sample] += 1
    total = n
    
    #iterating n times and in each time we generate transition model using our random sample (except for the first time), 
    #and then choose from the the list of pages based on the transition model probabilities as weights, then we add it to the
    #new_dict we created, then our random sample will be the last sample we generated
    while n != 0:
        new_model = transition_model(corpus, random_sample, 0.85)
        next_random_sample = random.choices([ key for key,value in new_model.items()],
                                         [value for key,value in new_model.items()], k=1)[0]
        new_dict[next_random_sample] += 1
        random_sample = next_random_sample
        n -= 1
        
    #calcuating proportion of all the pages using the total number of samples
    for key, value in new_dict.items():
        new_dict[key] = value/total
    return new_dict

def iterate_pagerank(corpus, damping_factor):
    
    #Return PageRank values for each page by iteratively updating
    #PageRank values until convergence.
    
    #generating new dict with keys are the pages and values are 1/N where N is the number of pages
    dict_2 = {page: 1/len(corpus) for page in corpus}

    flag = True
    while flag:
        
        #creating a copy from the values to use at as old values for comparison
        prev_dict = dict_2.copy()
        
        #iterating over the N pages and for each page(p), finding which pages(i) that link to that page(p), and dividing the 
        #value with the number of links in that page(i) and summing it and then applying the formula 
        for each_page in dict_2:
            value = 0
            value = sum([dict_2[page]/len(corpus[page]) for page in corpus if each_page in corpus[page]])
            value = 0.0375 + (damping_factor*value)
            dict_2[each_page] = value
        
        result = []
        #after the iteration over the N pages, comparing it with the previous value, until no value  changes by more than 0.001
        for page in dict_2:
            if abs(prev_dict[page] - dict_2[page]) >= 0.001:
                result.append(True)
            else:
                result.append(False)
        if any(result):
            #prev_dict = dict_2
            continue
        else:
            flag = False
    return dict_2


if __name__ == "__main__":
    main()
