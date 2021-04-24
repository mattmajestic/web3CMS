youtubeUi <- function(id) {
  ns <- NS(id)
  tagList(
    uiOutput(ns("video"))
  )
}

youtubeServer <- function(id,rv) {
  moduleServer(
    id,
    function(input, output, session) {
      output$video <- renderUI({
        HTML('<iframe src=src="https://www.youtube.com/embed/523yxcxjtGY" width="700" height="480"></iframe>')
      })
    }
  )
}
