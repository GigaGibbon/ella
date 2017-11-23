Ella Ella, The Magical Monkey
=============================

Ella is a Markov chain microblogger.

Configuration JSON file:
------------------------

* `sqlite_db` : The file for the sqlite db for the blogger.
* `main_corpus_source` : Path to a directory that contains text files which
will serve as Ella's main corpus.
* `main_corpus_json` : The file to use for the stored main corpus data. This
file will be created by Ella after she runs the first time.
* `main_weight` : The weight of the main corpus
* `link_corpora_json_dir` : This is the path to a directory where the link corpora
data will be stored.
* `link_corpora` : This is a list of link copora. Each entry should have the
following:
    * `name` : The name of the link corpus (will be used to determine JSON name)
    * `source`: The path to a directory containing text files for this corpus.
    * `url` : A list of URLs to use for the links for this link corpus.
    * `weight` : The weight for this link in the results
    * `min_max` : The min/max settings for the corpus. Each must be `[min, max]`
        * `sent_per_para` : Number of sentences per paragraph.
        * `para_per_page` : Number of paragraphs per page.
        * `pages` : Number of pages
