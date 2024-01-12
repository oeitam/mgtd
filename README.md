###
add:
 - ~~DONE comments (multiple) textual (comment @id | bla bla bla) stored as test with timestamp~~
 - ~~TODO context - a set of keywords ==> use tag instead~~
    ~~can this basically be the tag I already have?~~
 - ~~DONE add to tagging to test if tag exists - do not add it~~
 - ~~Done add priority to tasks, activities~~
 - ~~DOneDo not allow to create two projects with same name in one megaproject, no 2 megaprojects with same name~~
 - ~~Done make the adding from clip board work!!~~
 - search to TODO and fix
 - document all commands
 - ~~Done how to manag and control the location of the database (so it is backed up, for example, or based on parameter path)~~
 - document how to run in dev mode and production mode, direct and server modes
 - ~~Done print/html the database in hierarchy megaproject - its projects - task for each project~~
 - ~~Done add color to the html (like open vs closed, already added for hierarchical)~~
 - ~~Done document all the commands~~
 - enable bulk priority [of a list of ids] some priorioty (bulk priority change)
 - ~~Done, not exactly this way --> add that when the server is dying, it will copy the local directory to the area that is being backed up in one-drive. keep prod/dev seperatelly and override old~~
 - support bulk upload of commands from a txt file
 - add default sort and filter in the printing of DF - in regular list and in list html
 - ~~Done when listing a single item - still report in a table (unless want all fields) or list in a column (not a row)~~
 - when listing activity - for the project and task include first 2/3 words, not just the number
 - :make sure all tags start with a lower case t and the rest is upper case like tTAG, make sure all megaprojects are all capitals, projects are all lower case
 - when doing list tag - add a column for the type of the item (activity, task, etc)
 - add ability to create a shortcut that will take input - for example - instead of writing 'list project for megaproject XXX' have a shortcut like 'lpfmp XXX'
 - ~~Done fix the comment printing in html by replacing after html~~ \
 ~~generation - \n] for \<br>] , +++\n for +++\<br> , "\&lt;br\&gt;" for \<br> (need to identify for this the lines of comments and apply only on them)~~
 - find a way to load multy line things (as the terminal window supports only single line). perhaps the solution is the 'fromcb' option - from clipboard
 - ~~Done add to online - also the number of open projects, megaproject, tasks and activity (and priority)~~
 - the commend "sleep @136 1" put 1 as wakeup time. Need to check for correct syntax on wakeup time
 - add to task printing also the megaproject it belongs to. One implementation is to do that just for printing. Another implementaiton is to add a column, but then need to take care of this also when doing a move to a task
 - check how the move command works (before changes) and document
 - add list task and activity under project xxx or list project and task and activity under megaproject xxx
 - add ability to list for prioroity (like there is ability to list for state)
 - so when listing we can see things more clearly, limit the number of comment lines to a parameter (3? 4?) with ability also to see all comments (list ... allcomments ....)
 - ~~Done Note that when taking what is after the |, there is tendency (?) to take the space following the | ... need to remove it!~~
 - add ability to edit fields (some of them) like: edit @ID <column name> | new text
 - add ability to remove tag from all the database (like untagg tTODAY all)
 - ~~Done add commnds that run at startup like - list html, online~~
 - ~~not needed (happens after each command) consider running list html each time entering into the program~~
 - ~~for list html - make default to not include closed (keep dormant and on hold for now)~~. allow also an option to list all (list html all)
 - the command "task states" created a task for some reason ... not good. fix
 - list all tags
 - when tagging - notify the user if the tag is new or existing
 - add a recurring Activity ability (like - an activity that is created in a specific project once a month automatically)
 - we have state transitions date and text. print them together (ither in list @ID or specially)
 - END
      



 



# weekly

## opens/unknowns
does subtask (task @<taskid>) work?\
not implemented [swap, today, clean]

## system settings
need to have the following system variables\
"mgdt_code_path" = "C:\Users\oeitam\OneDrive - Intel Corporation\Documents\Z-Work\Projects\mgtd"
"mgdt_local_path" = "C:\mgtd.local"

## more
1. added ability to run commands before the client sends a first command in prod and in dev modes/
the list of commands is in the defs.py file
2. the files locations are parametrized in defs.py
3. when exiting (die), the program zips the local directory (parametrized, but usually c:\mgtd.local) and stores it in the code location (parametrized as well) in a directory named 'datastore'. The zipped files are created with a time tag as the name. They are not stored in github.
4. 

## Operation
this describes points how I use it (Jan 2024)
* 

## tags
- tEMAIL >> context is email. will try and put some hints in the description
- tONENOTE >> context is a OneNote page. Hints in the description


## commands and terms

### priority
priority >> set priority for a task or an activity\
default priority is medium\
priority test: High/Medium/Low
    
    priority @id High


### comment
comment >> adds a comment to an item. All items can take a comment. comments are textual only. all history kept

    comment @id | add some comment here

### create
megaproject >> a group of projects that can hold projects related to same area - like work or home

    create megaproject MP1 | some comment about the megaproject

project >> create a project that belongs to a megaproject

    create project P1 @MP1 tag some_tag | some comment about the project


list >> create a list of IDs for bukl operation

      create list @10677 @10678 @10679

shortcut .. (see below in section shortcut)

(task is created with task command)\
(activity is created with start command)

### task

### start
activity


### sleep
moves **activity** or **task** wakeup time\
-set wakeup time\
-add delta to shift wakeuptime (days)

      sleep @11540 17ww50
      sleep @11540 17ww50.Sun
      sleep @10673 plus 99

### stop
stop >> puts an item into terminal state: Activity to state Ended, Task to state Closed, Project to state Ended\
update the relevant fields.

      stop @some_id


### cont
cont >> moves an item to active state\
Activity and Project to state Started. Task to state Open.\

      cont @some_id


### halt
Halt >> put an item (Activity, Task, Ptoject) in OnHold state and update relevant fields

      halt @some_id


### delete
delete (does it delete underlying tasks of a project etc. ?)\
delete id
delete shortcut

      delete id
      delete shortcut 5
    
### list
list 
 - @id >> list full details of this item
 - megaproject >> list all megaprojects
 - project >> list all projects
 - task >> list all tasks
 - activity >> list all activities\
     `list @id`\
     `list megaproject`\
     `list project`\
     `list task`\
     `list activity`

 - html - craete an html file with all data\
    `list html`
 
 - tag >> list all items with tag 'some_tag'\
    `list tag some_tag`
 - hier >> create a hierarchical list of all the items in the database\
-Megaproject\
--Project\
---Activity\
---Task\
----Activity\

        list hier
        list hier html
        list hier megaproject XXX
        list hier project YYY


#### list qualifiers
[not sure qualifiers works for record types]\
[qualifiers can be mixed together]\
examples for qualifiers:\
-state some_state - would list items with this state\
-- 'all' is to list all state\
-states - list all states of a type\
-columns - lists columns of a type\
-ww xx - list what started on xx work week (task, activity)\
-col some_column - list filtered based on column some_column\
-range - date range\
-drange a_time a_time\
-examples of 'a_time':\
--bot - from earliest\
--top - till latest\
--YYwwXX.Day, YYwwXX\
-irange some_id other_id [or bot and top] >> list items within this ranmge
-list for >> list item thats parent is something else\
-filter qualifiers\
--is >> list all that equals the temr\
--not >> all except what is not\
--inc >> includes\
--ninc >> does not include\
-limit a_number >> limits the number of items listed\
-lastdays some_number >> list for some_number last days\
-listall >> use this to overcome system defaults that limits the number of lines printed/returned\
-wakeup >> list the tasks and activities in Dormant state which wakeup time is in teh past

      list activity state OnHold
      list megaproject state On
      list project state OnHold
      list task state OnHold
      list activity columns
      list megaproject states
      list activity col Start_Date drange bot top
      list activity ww 43
      list activity ww 43 state OnHold
      list activity state OnHold ww 43
      list activity ww 43
      list activity col Start_Date drange 17ww35.Sun 17ww39
      list task state all for project test1
      list project col Name is project_two
      list activity col PROJECT not 1498
      list activity col Description inc one
      list activity col PROJECT ninc 1498
      list megaproject col ID irange 2569 2631
      list megaproject col ID irange 2569 top
      list megaproject col ID irange bot 2631
      list megaproject col ID irange bot top
      list task lastdays 17 listall
      list wakeup

#### list parameter
list parameter >> lists all program parameters that can be set

#### list shortcut
(a shortcut is a substitution mechanism to save longish typing [?])\
list shortcut >> lists all the shortcuts defined in the system

### create shortcut
creates a shortcut and deposits it into config file for future - in next activation the \
shortcut is automatically loaded\
note - there is also a delete shortcut command


      create shortcut | ["simple_substitution", "co", "start @10758 | checking out - go home"]
      create shortcut | ["pipe_substitution", "lulu", "start @12969"]



### set
set a parameter

      set list_resp_row_limit value 5
      set max_width value 51

### online
online >> returns data on the status of the system (like database initialized, working env, wakeup items)

      online

### move
move all tasks or all activitess from one project to another project\
or move a list of items or a single item\
Note: need to keep the context correct (like move into an existing project and the likes)

      move task from test1 to test2 state OnHold
      move list to test1
      create list @10661 @10662 @10672
      move list to test2
      move @10661 to test2

### tag
tag with some no-spaces text
* does not allow for duplications per item
* can tag a project by name. Task/activity by ID
* can be used for context
* multiple tags allowed
* searchable (list tag command)
###
    tag @1234 some_tag
    untag @1234 some_tag
    tag project progect_name some_tag
    untag project progect_name some_tah

see list tag


### timedelta
The timedelta is a capadility to move the time base backword\
NOT SURE WHAT TO USE IT FOR (FORGET ... I THINK IT IS FOR UPDATING SOMETHING THAT HAPPENED IN THE PAST. FOR EXAMPLE - IF I COMPLETED A TASK YESTERDAY AND FORGOT, I CAN SHIFT THE TIME BACK, UPDATE THE TASK AND RESET IT BACK TO NOW)\
-returns the current timedelta\
-resets timedelta to 0\
-sets timedelta to some number of days

      timedelta
      timedelta off
      timedelta num_of_days
### help
help some_term\
Filters the help message (a hard coded list of commands examples) for some_term and returns the results


### fromcb (not a command, a term in a command)
Takes text from the system clipboard top. Assumed textual.\
Uses the content of the ckipboard for the transaction description\
(like what comes after the "|" )\
[does this really work ????]







