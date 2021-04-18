library(shiny)
library(shinydashboard)
library(shinyWidgets)
library(DT)
library(leaflet)
library(rhandsontable)
library(dplyr)
library(RStripe)
library(rmarkdown)

time_period_df <- data.frame("Time_Period" = c("Bi-Weekly","Month","Quarter"),
                             "Days" = c(15,30,90))

opps <- read.csv("data/opportunities.csv",stringsAsFactors = FALSE)
contacts <- read.csv("data/contacts.csv",stringsAsFactors = FALSE)
products <- read.csv("data/products.csv",stringsAsFactors = FALSE)

stripe_creds <- read.csv("api_keys/stripe.csv",stringsAsFactors = FALSE)
