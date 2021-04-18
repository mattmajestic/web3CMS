server <- function(input,output,session){
  rv <- reactiveValues()
  
  crmServer("crm_ns",rv)
  invoiceServer("invoice_ns",rv)
  
}