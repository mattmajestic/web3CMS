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