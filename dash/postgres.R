# create a connection

# loads the PostgreSQL driver
drv <- dbDriver("PostgreSQL")

# creates a connection to the postgres database
con <- dbConnect(drv, dbname = "postgres",
                 host = "35.196.103.17",
                 user = "postgres", password = "meaty")

# get table and field info
dbListTables(con)
dbListFields(con, "count_assoc_words")

# extract data from the database
post_data <- dbReadTable(con, "posts")
member_data <- dbReadTable(con, "group_members")
word_data <- dbReadTable(con, "count_assoc_words")
names(word_data) <- c('query','Brown', 'Columbia','Cornell', 'Dartmouth','Harvard','Penn','Princeton','Yale')

test <- duplicated.data.frame(post_data, by = c('caption', 'post_time', 'num_reacts', 'poster_name','title'))

post_data <- data.table(post_data)
member_data <- data.table(member_data)

for(con in dbListConnections(drv)){
  dbDisconnect(con)
}
dbUnloadDriver(drv)