make_submission <- function(name, dataframe) {
    ## Parameters
    ## ----------
    ##  name:               string, your name
    ##  submission_number:  int or string
    ##  dataframe:         data.frame [5999, 2], customer ids and 
    ##                          predicted probabilties on the test set
    
    # check input data frame appropriate shape
    if(nrow(dataframe) != 5999 | ncol(dataframe) != 2) {
        stop('data frame is wrong shape. Expecting [5999, 2]')
    # check input data for correct column names
    } else if(names(dataframe)[1] != 'customer_id') {
        stop('column 1 name is wrong. Expecting customer_id')
    }
    
    filename <- paste0(name, '.csv')
    write.csv(dataframe, filename, row.names = FALSE)
    
    return(paste(filename, 'created'))
}