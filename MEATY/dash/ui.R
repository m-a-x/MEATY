library(shinydashboard)

sidebar <- dashboardSidebar(
  sidebarMenu(
    id = "tabs",
    menuItem("Members", tabName = "members", icon = icon("user")), 
    menuItem("Posts", tabName = "posts", icon = icon(""))
  )
)

body <- dashboardBody(
  tabItems(
    tabItem(tabName = "members",
            h1("Members"),
            fluidRow(
              infoBoxOutput("members_day"),
              infoBoxOutput("members_week"),
              infoBoxOutput("total_members")
            ),
            fluidRow(
              box(title = "Top Posters", solidHeader = TRUE, collapsible = TRUE,
                  plotOutput("top_posters")),
              box(title = "Member Registration", solidHeader = TRUE, collapsible = TRUE,
                  dateRangeInput("date_range", "Joined Between:",
                                 start = Sys.Date() - 365,
                                 end = Sys.Date()), 
                  plotOutput("members_joined_plot")))),
    tabItem(tabName = "posts",
            h1("Posts"),
            fluidRow(
              infoBoxOutput("total_posts_day"),
              infoBoxOutput("total_posts_week"),
              infoBoxOutput("today_posts_reacts")
            ),
            fluidRow(
              box(title = "Page Activity", solidHeader = TRUE, collapsible = TRUE,
                  dateRangeInput("activity_date_range", "During Period:",
                                 start = Sys.Date() - 364,
                                 end = Sys.Date()),
                  plotOutput("page_activity"),
                  fluidRow(
                    actionButton("activity_by_day", "Day"),
                    actionButton("activity_by_week", "Week"),
                    actionButton("activity_by_month", "Month")
                  )
              )
            )
    )
  )
)

dashboardPage(
  dashboardHeader(title = "MEATY"),
  sidebar,
  body
)