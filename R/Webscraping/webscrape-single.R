# load packages ----
library(tidyverse)
library(rvest)
library(polite)

# Check for scrape-ability ----
bow("https://www.scrapingcourse.com")

# read page ----
url <- "https://www.scrapingcourse.com/ecommerce/"
page <- read_html(url)

# scrape titles of products ----
titles <- page |>
  html_elements(css = ".woocommerce-loop-product__title") |>
  html_text()

# prices ----
prices <- page |>
  html_elements(css = "bdi") |>
  html_text() |>
  str_remove("\\$") |>
  as.numeric()

# URLS ----
urls <- page |>
  html_elements(css = ".woocommerce-loop-product__link") |>
  html_attr(name = "href")


# make tibble ----
items <- tibble(
  title = titles ,
  price = prices, 
  url = urls,
)

write_csv(items, file="data/items.csv")

