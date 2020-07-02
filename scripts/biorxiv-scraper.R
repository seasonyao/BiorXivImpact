#!/usr/bin/env Rscript
#
# Usage: biorxiv-scraper.R [-o output_file] phrase
# Example ./biorxiv-scraper.R -o result.csv "gene editing"
#             

library(optparse, quietly=T, warn.conflict=F)
library(lubridate, quietly=T, warn.conflict=F)
library(tidyverse, quietly=T, warn.conflict=F)
library(httr, quietly=T, warn.conflict=F)
library(xml2, quietly=T, warn.conflict=F)

option_list<- list(
    make_option(c('-o', '--output'),
                type='character',
                default='output.tsv',
                help='Output, default %default'))
options <- parse_args(OptionParser(option_list=option_list),
                      positional_arguments=T)


options$args <- gsub("  *", "+", options$args)
numBioRxivPapers <- function(cont) {
    N <- 
        xml_text(xml_find_all(cont, 
                              "//div[@id='search-summary-wrapper']"))
    if (grepl("No Results", N)) {
        N <- 0
    } else {
        N <- gsub("[\\n\\t, ]", "", N)
        N <- gsub("Res.*", "", N)
        N <- as.numeric(N)
    }
    return(N)
}

getBioRxivPapers <- function(cont) {
    nodes <- 
        xml_find_all(cont, 
                          "//div[@class='highwire-article-citation highwire-citation-type-highwire-article']")
    bind_rows(lapply(nodes, function(node) {
        doi <- 
            xml_text(xml_find_first(node, ".//span[@class='highwire-cite-metadata-doi highwire-cite-metadata']"))
        doi <- gsub("[ \n]", "", doi)
        doi <- gsub('doi:', '', doi)
        title <- 
            xml_text(xml_find_first(node, ".//span[@class='highwire-cite-title']"))
        title <- gsub("^[ \n]*", "", title)
        title <- gsub("[ \n]*$", "", title)
        apath <- xml_attr(node, "data-apath")
        elements <- unlist(strsplit(apath, "/"))
        journal <- elements[2]
        division <- elements[3]
        submitted <- paste(elements[4], elements[5], elements[6], sep='-')
        
        tibble(link=doi,
               title=title,
               journal=journal,
               submitted=submitted)
    }))
}
query <- paste0("text_abstract_title:", 
                paste(options$args, collapse='+'),
                " ", 
                "text_abstract_title_flags:match-phrase ",
                "numresults:75 ",
                "sort:publication-date ",
                "direction:ascending ",
                "format_result:standard") %>%
    URLencode(reserved=T)

query <- paste0("https://www.biorxiv.org/search/",
                query)

response <- GET(query)
cont <- content(response, 'parsed') 
N <- numBioRxivPapers(cont)
cat("Number of papers:", N, "\n")
biomedRxivResults <-  getBioRxivPapers(cont) 

nAddPages <- ceiling(N/75) - 1

if (nAddPages>0) {
    biomedRxivResults <- 
        bind_rows(
            biomedRxivResults,
            lapply(1:nAddPages, function(i) {
                cat ("Downloading page", i+1, "of", nAddPages+1, "\n")
                query1 <- paste0(query,
                                 "?page=",
                                 i)
                result <- GET(query1)
                cont <- content(result, 'parsed')
                getBioRxivPapers(cont)
            }))
}
biomedRxivResults <- biomedRxivResults %>% mutate(title=gsub('\n', ' ', title)) %>%
    mutate(title=gsub("  *", " ", title)) %>% mutate(submitted=as.Date(submitted))

write_tsv(biomedRxivResults, options$options$output)
