# Zendesk - Coding Challenge

### Author - Manveer Singh

## Cloning the repository

Windows: Please install Git Bash (or github Desktop app), navigate to directory where you want to clone and run
        
        git clone https://github.com/msaulak/zendesk_manveer.git

Linux:  Please open a shell, navigate to directory where you want to clone and run

        git clone https://github.com/msaulak/zendesk_manveer.git

## Data
  
The search engine consumes data stored in the the folder data_files. 
Each sub folder holds the data for a type of data set.
For example, all files with data from organzation must be places under data_files/organization_data
and must match the pattern 'organization*.json'.
Please place addition data_files in respective folder.

## Test Data

Test data is placed under tests/test_data. The directory structure and the files are the same
as that of the data discussed above. These data files are for tests only and should not be updated
unless test cases require a change.    

## Language, build environments and dependencies

This solution has been coded in Python3.7 using PyCharm IDE on Windows. Tested on Ubuntu 18 as well.
To see the output in a tabular format, please ensure that module 'prettytable' is installed or you
can setup a conda environment for that.
If not, the output would be in the raw format.
See below for more information on setting up the conda environment.
    
    1. Please install miniconda if not installed.
        Windows : https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html
        Linux : https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html
    2. Once installed, open a 
        a. Shell if using Linux
        b. Anaconda prompt if using Windows
    3. Run the following and follow the prompts.
        a. conda create -n zendesk_manveer
        b. conda activate zendesk_manveer
        c. conda install -c conda-forge prettytable

## Running the CLI

1. Activate conda environment created above using 
        
        conda activate zendesk_manveer

2. Go to the git repository directory and run

        python main.py
        
## Run tests

There are 14 test cases in total. (4 for searching by Organization, 6 each for searching by Tickets and Users)
1. Activate conda environment
        
        conda activate zendesk_manveer

2. Go to the git repository directory and run

        python -m unittest
        
## Alternative solutions:

#### SQL database

Using MySql to store data and run queries to retrieve it. This solution is more scalable because
all the data will be store in an SQL store. Retrieval can be sped up by using the correct indices and joins.
I did not use this approach because it requires additional setup and would have exceeded the
scope of this exercise

#### python pandas

Using pandas to create data frames for users, tickets and organizations would made it easier to
code data storage and data retrieval. However, processing is very slow. I wrote a small
code snippet for comparing run times and pandas we clearly very slow. 

## Trade offs:

I decided to use a regular python dictionary to store links between different entities which
do not have foreign keys in themselves. For example, the user_to_ticket_submitter in class ZendeskSearchEngine
is a dictionary which has User._id as key and the list of Ticker._id which have that User._id as the 
Ticket.submitter_id. This ensure that lookup time is not linear when looking for all tickets where a User._id
is a submitter.


## Assumptions:

    1. OS specific character encoding representation not dealt with in the implementation.
    
    2. Searching by multiple tags not supported. For example: If the search criteria are
        a. Search for Organization
        b. by tags
        c. on Jordan, Roy, Frost (all together)
        
        There will be results displayed though organization_id 105 could be a potenital match.
        
        Searching by a single tag is supported.
        
    3. All user input is converted to lower case to allow easy use of CLI. When comparing string
    to look up entities, the values are converted to lower string. This ensures that user input and
    values of an entity are both in lower case and comparable.
       
         