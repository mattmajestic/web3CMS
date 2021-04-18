ui <- dashboardPage(
  dashboardHeader(title = "shinyCRM"),
  dashboardSidebar(
    sidebarMenu(
      menuItem("Contacts",tabName = "contacts"),
      menuItem("Opportunities",tabName = "opps"),
      menuItem("Products",tabName = "products"),
      menuItem("Invoicing",tabName = "invoice"),
      menuItem("Payments",tabName = "payments"))),
  dashboardBody(
    tabItems(
      tabItem(tabName = "contacts",
              crmUi("crm_ns")),
      tabItem(tabName = "opps"),
      tabItem(tabName = "products"),
      tabItem(tabName = "invoice",
              invoiceUi("invoice_ns")),
      tabItem(tabName = "payments"))))