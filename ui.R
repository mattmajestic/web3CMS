ui <- dashboardPage(
  dashboardHeader(title = "shinyCRM"),
  dashboardSidebar(
    sidebarMenu(
      menuItem("Home",tabName = "home",icon = icon("home")),
      menuItem("Contacts",tabName = "contacts",icon = icon("address-book")),
      menuItem("Invoicing",tabName = "invoice",icon = icon("file-invoice"))
      )),
  dashboardBody(
    tabItems(
      tabItem(tabName = "home",uiOutput("home_ui")),
      tabItem(tabName = "contacts",crmUi("crm_ns")),
      tabItem(tabName = "invoice",invoiceUi("invoice_ns"))
      )))