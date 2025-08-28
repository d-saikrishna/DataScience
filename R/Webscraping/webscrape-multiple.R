# load packages ----
library(tidyverse)
library(rvest)
library(polite)
library(glue)

# Check for scrape-ability ----
bow("https://www.scrapingcourse.com")

# read pages ----
page_nos <- 1:5
urls <- glue("https://www.scrapingcourse.com/ecommerce/page/{page_nos}/")

# Write function to scrape a single page ----
scrape_items <- function(url){
  
  page <- read_html(url)
  
  # scrape titles of products
  titles <- page |>
    html_elements(css = ".woocommerce-loop-product__title") |>
    html_text()
  
  # prices
  prices <- page |>
    html_elements(css = "bdi") |>
    html_text() |>
    str_remove("\\$") |>
    as.numeric()
  
  # URL
  urls <- page |>
    html_elements(css = ".woocommerce-loop-product__link") |>
    html_attr(name = "href")
  
  
  # make tibble 
  tibble(
    title = titles ,
    price = prices, 
    url = urls,
  )
}

# map function over all urls
map(urls,scrape_items) |>
  list_rbind()
