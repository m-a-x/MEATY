source('requirements.R')
source('postgres.R')

renderCountBox <- function(data) {
  renderPlot({})
}

renderActivityPlot <- function(interval, input, post_data) {
  renderPlot({
    date_range <- input$activity_date_range
    if (interval == "day") interval <- "date"
    interval_col <- paste0("post_", interval)
    plot_data <- post_data[post_date >= date_range[1] & post_date <= date_range[2],
                           .(num_posts = length(id)),
                           by=c(interval_col)]
    ggplot(data = plot_data, aes_string(x = interval_col, y = "num_posts")) + 
      geom_bar(stat = "identity") +
      scale_x_date(name = paste0(capitalize(interval), " Posted"), date_breaks = "1 months", date_labels = "%b %d") +
      scale_y_continuous(name = "Number of Posts")
  })
}


server <- function(input, output, session) {

  post_data[, ':='(post_week=as.Date(cut.Date(post_date, breaks = "weeks")),
                   post_month=as.Date(cut.Date(post_date, breaks = "months")))]
  
  # Members joined histogram
  output$members_joined_plot <- renderPlot({
    date_range <- input$date_range
    plot_data <- member_data[date_added >= date_range[1] & date_added <= date_range[2]] 
    ggplot(data = plot_data, aes(x = date_added)) + 
      geom_bar(stat = "count") + xlab("Date Added") + ylab("")
  })
  
  output$top_posters <- renderPlot({
    top_posters <- post_data[, .(num_posts = length(id)), by=c("poster_name")][order(-num_posts)]
    top10_posters <- top_posters[1:10]
    top_poster_activity <- post_data[poster_name %in% top10_posters$poster_name,
                                     .(num_posts = length(id)),
                                     by=c("poster_name", "post_date")][order(poster_name, post_date)]
    top_poster_activity[, cum_posts := cumsum(num_posts), by=c("poster_name")]
    ggplot(data = top_poster_activity, aes(x = post_date, y = cum_posts, color = as.character(poster_name))) + 
      geom_line() + ylab("Cumulative Posts") + xlab("") + theme(legend.title=element_blank())
  })
  
  # Post reacts
  output$top_posts_plot <- renderPlot({
    var1 <- "post_date"
    var2 <- "id"
    date_range <- c(Sys.Date() - 365, Sys.Date())
    
    plot_data <- post_data[post_date >= date_range[1] & post_date <= date_range[2],
                           .SD, .SDcols = c(var1, var2, "num_reacts")]
    ggplot(data = plot_data, aes_string(x = var1, y = var2)) + 
      geom_point(aes(size = num_reacts))
  })
  
  observeEvent(input$activity_by_day, {
    output$page_activity <- renderActivityPlot("day", input, post_data)
  })
  
  observeEvent(input$activity_by_week, {
    output$page_activity <- renderActivityPlot("week", input, post_data)
  })
  
  observeEvent(input$activity_by_month, {
    output$page_activity <- renderActivityPlot("month", input, post_data)
  })
  
  output$page_activity <- renderActivityPlot("day", input, post_data)
  
  # Member-related info boxes
  output$members_today <- renderInfoBox({
    today_members <- member_data[date_added == Sys.Date()]
    infoBox("New Members Today", nrow(today_members), icon = icon("user"), color = "green")
  })
  
  output$members_week <- renderInfoBox({
    week_members <- member_data[date_added > Sys.Date() - 7]
    print(nrow(week_members))
    infoBox("New Members This Week", nrow(week_members), icon = icon("user"), color = "purple")
  })
  
  output$total_members <- renderInfoBox({
    infoBox("Total Members", nrow(member_data), icon = icon("user"), color = "yellow")
  })
  
  # Posts-related info boxes
  output$total_posts_today <- renderInfoBox({
    today_posts <- post_data[post_date == Sys.Date()]
    infoBox("Posts Today", nrow(today_posts), icon = icon("list"), color = "aqua")
  })
  
  output$total_posts_week <- renderInfoBox({
    week_posts <- post_data[post_date > Sys.Date() - 7]
    infoBox("Posts This Week", nrow(week_posts), icon = icon("list"), color = "green")
  })
  
  output$today_posts_reacts <- renderInfoBox({
    today_posts <- post_data[post_date == Sys.Date()]
    infoBox("Today's Post Reacts", sum(today_posts$num_reacts), icon = icon("thumbs-up"), color = "red")
  })
}