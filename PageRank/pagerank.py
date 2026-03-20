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
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
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


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution={}
    N=len(corpus)
    if len(corpus[page])==0:
        for p in corpus:
            distribution[p]=1/N
        return distribution
    for p in corpus:
        distribution[p]=(1-damping_factor)/N
    
    numlinks=len(corpus[page])
    for linkedPage in (corpus[page]):
        distribution[linkedPage]+=damping_factor/numlinks
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    count={}
    for page in corpus:
        count[page]=0
    current=random.choice(list(corpus.keys()))
    count[current]+=1

    for _ in range(n-1):
        model=transition_model(corpus,current,damping_factor)
        pages=list(model.keys())
        prob=list(model.values())

        current=random.choices(pages,weights=prob,k=1)[0]
        count[current]+=1

    pagerank={}
    for page in count:
        pagerank[page]=count[page]/n
    return pagerank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank={}
    for page in corpus:
        pagerank[page]=1/len(corpus)
    
    while True:
        new_pagerank={}
        for page in corpus:
            total=0
            for other_page in corpus:
                if len(corpus[other_page])==0:
                    total+= pagerank[other_page]/len(corpus)
                elif page in corpus[other_page]:
                    total+=pagerank[other_page]/len(corpus[other_page])
            new_pagerank[page]= (1-damping_factor)/len(corpus)+damping_factor*total

        diff=0
        for page in pagerank:
                diff=max(diff,abs(new_pagerank[page]-pagerank[page]))

        pagerank=new_pagerank

        if diff<.001:
                
             break
    return pagerank


    


if __name__ == "__main__":
    main()
