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
                     h5("Select Row to Edit or Delete"),
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
          box(title = "Contact Fields",solidHeader = TRUE,width = 12,status = "primary",
              # tgs_lst,
              textInput("Company","Company",value = rv$selected_data$Company)
              actionBttn("save_contact","Update Contact",icon = icon("save"),style = "jelly",color = "primary"),
              actionBttn(ns("delete_contact"),"Delete Contact",icon = icon("trash"),style = "jelly",color = "danger"))
        })
      })
      
      observeEvent(input$save_contact,{
        contact_inputs <- names(contacts)
        input_test <<- input %>% reactiveValuesToList()
        updated_row <- data.frame()
        names(updated_row) <- names(contact)
        for (col in 1:length(contact_inputs)) {
          rv$contacts[input$contacts_dt_rows_selected,col] <- input_test[[names(contacts)[col]]]
          print(input_test[[names(contacts)[col]]])
        }
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
        
        Sys.time(2)
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