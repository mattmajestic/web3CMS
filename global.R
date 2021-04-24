library(shiny)
library(shinydashboard)
library(shinyWidgets)
library(DT)
library(leaflet)
library(rhandsontable)
library(dplyr)
library(RStripe)
library(rmarkdown)
library(shinyalert)

time_period_df <- data.frame("Time_Period" = c("Bi-Weekly","Month","Quarter"),
                             "Days" = c(15,30,90))

opps <- read.csv("data/opportunities.csv",stringsAsFactors = FALSE)
contacts <- read.csv("data/contacts.csv",stringsAsFactors = FALSE)
products <- read.csv("data/products.csv",stringsAsFactors = FALSE)

stripe_creds <- read.csv("api_keys/stripe.csv",stringsAsFactors = FALSE)

crmUi <- function(id) {
  ns <- NS(id)
  tagList(
    fluidPage(
      fluidRow(
        column(8,box(title = "Contact Information",width = 12,
                     br(),
                     h3("Below are some fields for clients of Majestic Data Solutions LLC"),
                     br(),
                     DTOutput(ns("contacts_dt")),
                     br(),
                     actionBttn(ns("upload_aws"),"Upload Your Own Contacts",icon = icon("upload"),style = "jelly",color = "primary"),
                     actionBttn(ns("add_contact"),"Add Contact",icon = icon("save"),style = "jelly",color = "primary"))),
        column(4,uiOutput(ns("selected_contact")))
      )
    )
  )
}

crmServer <- function(id,rv) {
  moduleServer(
    id,
    function(input, output, session) {
      output$contacts_dt <- renderDT({
        DT::datatable(rv$contacts,rownames = FALSE,selection = "single",editable = TRUE)
      })
      
      observeEvent(input$contacts_dt_rows_selected,{
        print(input$contacts_dt_rows_selected)
        
        ns <- NS(id)
        
        rv$selected_data <- rv$contacts %>%
          dplyr::slice(input$contacts_dt_rows_selected)
        print(rv$selected_data)
        
        tgs_lst <- list()
        
        output$selected_contact <- renderUI({
          useShinydashboard()
          
          # for(i in 1:ncol(rv$contacts))
          # {tgs_lst[[i]] <- textInput(inputId = names(rv$selected_data)[i],label = names(rv$selected_data)[i],value = rv$selected_data[,i])}
          # tgs_lst 
          # rv$tags <- tgs_lst
          box(title = "Contact Fields",solidHeader = TRUE,width = 12,status = "primary",
              # tgs_lst,
              textInput(ns("Company"),"Company",value = rv$selected_data$Company),
              textInput(ns("Street"),"Street",value = rv$selected_data$Street),
              textInput(ns("City"),"City",value = rv$selected_data$City),
              textInput(ns("State"),"State",value = rv$selected_data$State),
              textInput(ns("Zip"),"Zip",value = rv$selected_data$Zip),
              textInput(ns("Sector"),"Sector",value = rv$selected_data$Sector),
              selectInput(ns("Product"),"Product",selected = rv$selected_data$Product,choices = c("Consulting","Tutoring")),
              selectInput(ns("Status"),"Status",selected = rv$selected_data$Status,choices = c("Active","Inactive")),
              actionBttn(ns("save_contact"),"Update Contact",icon = icon("save"),style = "jelly",color = "primary"),
              actionBttn(ns("delete_contact"),"Delete Contact",icon = icon("trash"),style = "jelly",color = "danger"))
        })
      })
      
      observeEvent(input$save_contact,{
        contact_inputs <- names(rv$contacts)
        input_test <<- input
        # print(rv$tags)
        print(input$Company)
        updated_row <- data.frame()
        names(updated_row) <- names(rv$contact)
        for (col in 1:length(contact_inputs)) {
          rv$contacts[input$contacts_dt_rows_selected,col] <- input_test[[names(contacts)[col]]]
          print(input_test[[names(contacts)[col]]])
        }
        print(rv$contacts)
      })
      
      observeEvent(input$upload_aws,{
        
        showModal(modalDialog(size = "l",
                              title = "Upload a CSV file from the template Download",
                              textInput("csv_name","Company Name"),
                              fileInput("file1", "Choose CSV File",
                                        multiple = TRUE,
                                        accept = c("text/csv",
                                                   "text/comma-separated-values,text/plain",
                                                   ".csv")),
                              
                              output$upload_csv <- renderDT({
                                req(input$file1)
                                rv$upload <- read.csv(input$file1$datapath)
                                DT::datatable(rv$upload,options = list(scrollX = TRUE),rownames = FALSE)}),
                              actionButton("upload_csv","Upload CSV to S3 Bucket")
        ))
        
        Sys.sleep(2)
        shinyalert(title = "Coming Soon",text = "Use my data as V1 demo",timer = 4000,type = "error")
      })
      
      observeEvent(input$upload_csv,{
        rv_list <- reactiveValuesToList(rv)
        temp_def <- rv$upload
        showModal(modalDialog(
          title = "Successfully Uploaded",
        ))
      })
      
      observeEvent(input$add_contact,{
        rv$contacts[nrow(rv$contacts)+1,] <- "Update Field"
        write.csv(rv$contacts,"data/contacts.csv",row.names = FALSE)
      })
      
      
      observeEvent(input$delete_contact,{
        rv$contacts <- rv$contacts %>% dplyr::slice(-input$contacts_dt_rows_selected)
        write.csv(rv$contacts,"data/contacts.csv",row.names = FALSE)
      })
    }
  )
}


invoiceUi <- function(id) {
  ns <- NS(id)
  tagList(
    fluidPage(
      titlePanel('Invoice Generator'),
      sidebarLayout(
        sidebarPanel(
          fluidRow(
            textInput(ns("name"),"Your Business",placeholder = "LLC, Inc, Etc")
          ),
          fluidRow(
            textInput(ns("account"),"Your Account Number",placeholder = "Left part of check"),
            textInput(ns("routing"),"Your Routing Number",placeholder = "Right part of check")
          ),
          #dateRangeInput("dates","Date Range",start = Sys.Date() - 30,end = Sys.Date() + 30),
          numericInput(ns("rate"),"Hourly Rate",value = 50,min = 1,max = 1000),
          radioButtons(ns("time_period"),"Time Period",choices = c("Bi-Weekly")),
          downloadButton(ns("report"), "Generate invoice")
        ),
        mainPanel(
          rHandsontableOutput(ns("invoice_table")),
          br(),
          textOutput(ns("total"))
        )))
  )
}

invoiceServer <- function(id,rv) {
  moduleServer(
    id,
    function(input, output, session) {
      observeEvent(input$time_period,{
        rv$invoice_range <- time_period_df %>%
          dplyr::filter(Time_Period == input$time_period) %>%
          dplyr::select(Days) %>%
          as.numeric()
        updateDateRangeInput(session,"dates",start = Sys.Date() - rv$invoice_range,end = Sys.Date())
      })
      
      output$days <- renderText({
        paste0('Contract Length: ',  input$end_date - input$start_date + 1 - input$skip_days," days")
      })
      output$address <- renderText({
        paste('Address: ',input$address, sep = ', ')
      })
      
      rTable_content <- reactive(
        {
          time_num <- time_period_df %>%
            dplyr::filter(Time_Period == input$time_period) %>%
            dplyr::select(Days) %>%
            as.numeric()
          
          DF <- data.frame("Date" = seq.Date(from = Sys.Date() - time_num,to = Sys.Date() ,by = "days"),
                           "Hours" = 0)
          
          # Try to keep previously entered custom value for match Type's
          if (length(input$invoice_table) > 0){
            oDF <- hot_to_r(input$invoice_table)
            DF$Hours <- oDF$Hours
          }
          
          DF
        }
      )
      
      output$invoice_table <- renderRHandsontable({
        
        rhandsontable(rTable_content(),rowHeaders = FALSE)
      })
      
      output$total <- renderText({
        paste0("total: ",sum(rTable_content()$Hours) * input$rate)
      })
      
      output$report <- downloadHandler(
        # For PDF output, change this to "report.pdf"
        filename = "invoice.pdf",
        content = function(file) {
          # Copy the report file to a temporary directory before processing it, in
          # case we don't have write permissions to the current working dir (which
          # can happen when deployed).
          tempReport <- file.path(tempdir(), "invoice.Rmd")
          file.copy("invoice.Rmd", tempReport, overwrite = TRUE)
          
          # file.copy("details.csv",tdir)
          
          # Set up parameters to pass to Rmd document
          params <- list(name = input$name,
                         start_date = input$start_date,
                         end_date = input$end_date,
                         date = Sys.Date(),
                         rate = input$rate,
                         invoice_df = rTable_content(),
                         account = input$account,
                         routing = input$routing)
          
          # Knit the document, passing in the `params` list, and eval it in a
          # child of the global environment (this isolates the code in the document
          # from the code in this app).
          rmarkdown::render(tempReport, output_file = file,
                            params = params,
                            envir = new.env(parent = globalenv())
          )
        }
      )
    }
  )
}
