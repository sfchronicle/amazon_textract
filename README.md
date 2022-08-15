# amazon_textract
to extract text!
This is the one of the repos for restrain and seclusion project. 

Here we use Amazon Textract to scrape hand-written numbers and words from over 30,000 restrain and seclusion incidents,mostly in pdf forms, in New York State. 

Each school district has their own ways to document incidents, so, we customed scripts for each district (Sounds like a lot, right? But we did it!) 

The text_config.py is to extract necessary data for the Textract outputs. Here we use keywords to identify which words or numbers we need for the story.
To extract the data, you need to check if there is any keywords you need to change in the text_config.py.

Some pdfs contain image-based tables. A small part of them could be read by Tabula which doesn't make our life easier at all. So we turn to Textact again. The table_parser.py will help you scrape data from these tables and create csv files based on the outputs.

The most important thing is that running Textract will cost money, so make sure your manager knows about it before you run any scripts.
