crmUi <- function(id) {
  ns <- NS(id)
  tagList(
    fluidPage(
      fluidRow(
        column(8,DTOutput(ns("contacts_dt"))),
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
        DT::datatable(contacts,rownames = FALSE,selection = "single")
      })
      
      observeEvent(input$contacts_dt_rows_selected,{
        print(input$contacts_dt_rows_selected)
        
        rv$selected_data <- contacts %>%
          dplyr::slice(input$contacts_dt_rows_selected)
        print(rv$selected_data)
        
        tgs_lst <- list()
        
        output$selected_contact <- renderUI({
          useShinydashboard()
          
          for(i in 1:ncol(contacts))
          {tgs_lst[[i]] <- textInput(inputId = names(rv$selected_data)[i],label = names(rv$selected_data)[i],value = rv$selected_data[,i])}
          tgs_lst 
          box(title = "Contact Fields",solidHeader = TRUE,width = 12,status = "primary",
              tgs_lst,
              actionBttn("save_contact","Update Contact",icon = icon("save"),style = "jelly",color = "primary"))
        })
      })
      
      observeEvent(input$save_contact,{
        contact_inputs <- names(contacts)
        input_test <<- input %>% reactiveValuesToList()
        updated_row <- data.frame()
        names(updated_row) <- names(contact)
        for (col in 1:length(contact_inputs)) {
          print(input_test[[names(contacts)[col]]])
        }
      })
    }
  )
}