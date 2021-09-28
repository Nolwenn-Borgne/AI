import math
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
    # create the dictionary
    probability_distribution = {}
    for key in corpus:
        probability_distribution.update({key: 0})

    # we first check if page has no outgoing links
    if len(corpus[page]) == 0:
        for key in corpus:
            # chooses randomly among all pages with equal probability
            probability_distribution.update({key: (1 / len(corpus))})
    else:
        # with probability damping_factor, add the probability in the dictionary
        # the random surfer should randomly choose one of the links from page with equal probability
        for item in corpus[page]:
            probability_distribution.update({item: damping_factor / len(corpus[page])})
        # with probability 1-damping_factor, update the probability in the dictionary
        # the random surfer should randomly choose one of all the pages in the corpus with equal probability
        for key in corpus:
            probability_distribution.update({key: probability_distribution[key] + (1 - damping_factor) / len(corpus)})

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initiate sample
    sample = []

    # choose a random page
    page = random.choice(list(corpus))

    # add the page to the sample
    sample.append(page)

    # repeat n times
    for i in range(n):
        # generate the next page based on the previous page's transition model
        weights_values = list(transition_model(corpus, page, damping_factor).values())
        page = random.choices(list(corpus),
                              weights=weights_values,
                              k=1)[0]
        sample.append(page)

    # create the pagerank_values
    pagerank_values = {}
    for page in corpus:
        pagerank_values.update({page: sample.count(page) / n})

    # return the pageRank values
    return pagerank_values


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initiate pagerank_values
    pagerank_values = {}
    nb_pages = len(corpus)
    for page in corpus:
        pagerank_values.update({page: 1 / nb_pages})

    precision = 0

    while precision != nb_pages:
        precision = 0
        pagerank_copy = pagerank_values.copy()
        for page in corpus:
            sum_pr = 0
            for link in corpus:
                # if there are links to this page
                if page in corpus[link]:
                    sum_pr += + pagerank_copy[link] / len(corpus[link])
                # add some logic to deal with pages with no links
                # A page that has no links at all should be interpreted
                # as having one link for every page in the corpus (including itself).
                if len(corpus[link]) == 0:
                    sum_pr += pagerank_copy[link] / nb_pages
            value = (1 - damping_factor) / nb_pages + damping_factor * sum_pr
            if abs(pagerank_copy[page] - value) < 0.001:
                precision += 1
            pagerank_values.update({page: value})

    return pagerank_copy


if __name__ == "__main__":
    main()
