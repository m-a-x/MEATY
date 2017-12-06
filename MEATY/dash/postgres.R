# create a connection

# loads the PostgreSQL driver
drv <- dbDriver("PostgreSQL")

# creates a connection to the postgres database
con <- dbConnect(drv, dbname = "postgres",
                 host = "35.190.137.115",
                 user = "postgres", password = "meaty")

# get table and field info
dbListTables(con)
dbListFields(con, "posts")

# extract data from the database
post_data <- dbReadTable(con, "posts")
member_data <- dbReadTable(con, "group_members")

test <- duplicated.data.frame(post_data, by = c('caption', 'post_time', 'num_reacts', 'poster_name','title'))

post_data <- data.table(post_data)
member_data <- data.table(member_data)

for(con in dbListConnections(drv)){
  dbDisconnect(con)
}
dbUnloadDriver(drv)