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

    new_dict = {}
    for e in (corpus):
        new_dict[e] = 0
    
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
    raise NotImplementedError

def iterate_pagerank(corpus, damping_factor):
    raise NotImplementedError


if __name__ == "__main__":
    main()
