library(knitr)
library(brocks)
library(stringr)

setwd("c:/users/ethan/ethan-cheong.github.io")

mdConverter <- function(file) {
  # Create a directory for the files
  directory.name <- str_remove_all(file, "[^A-Za-z\\-]")
  
  knitr::opts_chunk$set(
    fig.path   = sprintf('figure/%s/', directory.name),
    cache.path = sprintf('cache/%s/', directory.name),
    screenshot.force = FALSE
  )
  
  # Create directories
  source.directory = paste0('_drafts/', file, '.Rmd')
  output.directory = paste0('_posts/', file, '.md')
  
  # Convert to md
  knitr::render_markdown()
  knitr::knit(input = source.directory, 
              output = output.directory, 
              quiet = TRUE, 
              encoding = 'UTF-8', 
              envir = .GlobalEnv)
  
  # store the dependencies
  brocks::htmlwidgets_deps(source.directory)
}

build_article("2021-01-02-plotly-in-jekyll")
