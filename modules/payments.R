

paymentsUi <- function(id) {
  ns <- NS(id)
  tagList(
    box(title = "Include RStripe Package integration with something like this")
  )
}

paymentsServer <- function(id,rv) {
  moduleServer(
    id,
    function(input, output, session) {
    }
  )
}
