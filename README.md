###
add:
 - ~~DONE comments (multiple) textual (comment @id | bla bla bla) stored as test with timestamp~~
 - ~~TODO context - a set of keywords ==> use tag instead~~
    ~~can this basically be the tag I already have?~~
 - ~~DONE add to tagging to test if tag exists - do not add it~~
 - ~~Done add priority to tasks, activities~~
 - ~~DOneDo not allow to create two projects with same name in one megaproject, no 2 megaprojects with same name~~
 - ~~Done make the adding from clip board work!!~~
 - ~~Done how to manag and control the location of the database (so it is backed up, for example, or based on parameter path)~~
 - ~~Done print/html the database in hierarchy megaproject - its projects - task for each project~~
 - ~~Done add color to the html (like open vs closed, already added for hierarchical)~~
 - ~~Done document all the commands~~
 - ~~Done, not exactly this way --> add that when the server is dying, it will copy the local directory to the area that is being backed up in one-drive. keep prod/dev seperatelly and override old~~
 - ~~Done when listing a single item - still report in a table (unless want all fields) or list in a column (not a row)~~
 - ~~Done make sure all tags start with a lower case t and the rest is upper case like tTAG, make sure all megaprojects are all capitals, projects are all lower case ~~
 - ~~Done fix the comment printing in html by replacing after html~~ \
 ~~generation - \n] for \<br>] , +++\n for +++\<br> , "\&lt;br\&gt;" for \<br> (need to identify for this the lines of comments and apply only on them)~~
 - ~~Done add to online - also the number of open projects, megaproject, tasks and activity (and priority)~~
 - ~~Done Note that when taking what is after the |, there is tendency (?) to take the space following the | ... need to remove it!~~
 - ~~Done add ability to edit fields (some of them) like: edit @ID <column name> | new text~~
 - ~~Done add commnds that run at startup like - list html, online~~
 - ~~not needed (happens after each command) consider running list html each time entering into the program~~
 - ~~Done list all tags~~
 - ~~Done complete cid and lid. seems need to update cid with each call to get_id.~~
 - ~~Done (already existed) - list search - add function what just searches the database for a word and returns all items with this word~~
 - ~~ Checed - is OK - the rapid growth in ID is since every start of the app the number grows by one at init (w/o an item created) check - do we really need to get a new id for every transaction, even if not really need a new ID? seems it makes progress for each all regardless. was that intended in the past?~~
 - ~~Done add autometically that the system keeps the previous action @id (if there was one, otherwise -1). this will save tyoping in case of donig list @id, some action @id (same id)~~
 - ~~Done start @cid was not working after creating a task and the cid was that of the task. no specific issue returned~~
 - ~~Done add check that the priority setting is indeed correctly spelled and if not - return an error~~
 - ~~Done add ability to set prioroity at creation  (like start @123 tag tXXX prio Yyyy)~~
 - ~~Done enable priority in mid command (start @xxx prio High tag tSOMETAG) ~~
 - ~~ Donecheck how the move command works (before changes) and document or make useful~~
 - ~~Done and also - support move command for projects from one megaproject to another~~
 - ~~Done add a 'mark' command that will insert something to teh html file after some megaproject or after any item (id). this will help go over the file part by part. make also ability to remove the mark or report where the mark is (some exist - mark as parameter) add ability to set mark by 'name' not just by 'id' ~~
 - ~~ Done document how to run in dev mode and production mode, direct and server modes~~
 - ~~Done issue: if project name is not unique across teh dtabase, and it is still used as identifier for task or activity relations, we may have a duality in task or activity relation. So - must make project name unique across the database or need to use IDs only for relations~~
 - ~~Done add ability to create a shortcut that will take input - for example - instead of writing 'list project for megaproject XXX' have a shortcut like 'lpfmp XXX'~~
 - ~~Done add a shortcut like #<some shortcut> @ID ==> that will turn into something like tag @ID tTODAY | some text ?~~
 - \\/support bulk upload of commands from a txt file
 - \\/enable bulk priority [of a list of ids] some priorioty (bulk priority change)
 - \\/add default sort and filter in the printing of DF - in regular list and in list html
 - \\/when listing activity - for the project and task include first 2/3 words, not just the number
 - \\/when doing list tag - add a column for the type of the item (activity, task, etc)
 - \\/add to task printing also the megaproject it belongs to. One implementation is to do that just for printing. Another implementaiton is to add a column, but then need to take care of this also when doing a move to a task
 - \\/add list task and activity under project xxx or list project and task and activity under megaproject xxx
 - \\/add ability to remove tag from all the database (like untagg tTODAY all)
 - \\/add a recurring Activity ability (like - an activity that is created in a specific project once a month automatically)
 - \\/we have state transitions date and text. print them together (ither in list @ID or specially)
 - \\/~~for list html - make default to not include closed (keep dormant and on hold for now)~~. allow also an option to list all (list html all)
 - \\/ (exists in html basically) add 'list tree @id' whcih will list all the items under this id. list tree @id listall - lists also non active (closed, dormant, onhold) items
 - find a way to load multy line things (as the terminal window supports only single line). perhaps the solution is the 'fromcb' option - from clipboard
 - the commend "sleep @136 1" put 1 as wakeup time. Need to check for correct syntax on wakeup time
 - add ability to list for prioroity (like there is ability to list for state)\ 
so when listing we can see things more clearly, limit the number of comment lines to a parameter (3? 4?) with ability also to see all comments (list ... allcomments ....)
 - the command "task states" created a task for some reason ... not good. fix
 - when tagging - notify the user if the tag is new or existing
 - check - list wakeup supposed to return what has wakeup in teh past and this week. On Sunday it did not give anything ... on Monday - it showed what needs wakeup this week. So there is a shift of a day in 'what is this week'. Check.
 - when doing edit to the name of a megaproject, need to go and replace this name for projects in their records
 - add to 'online' also a check that all tasks and activities under a project is in the correct state (can do that per task and per activity)\
project that is dormant all tasks and activities cannot be open or onhold, etc. ~~also check no duplicate IDs ~~
 - - check that all items that neeed a parent have a parent
 - - check what have 'clean' for description or for parent
 - error - i cerated two projects named okr and it failed (took them!)
 - check - task @[task_id] tag tEmail | bla bla bla failed, but still created a bad task 
 - when doing sleep something - print out also the wakeup time set for the 'element'
 - remove dormant from online
 - make online wake up what is dormant and needs wake up (so I can remove dormant from my collaps and not care on them till wake up)
 - add something like 'list all state Dotmant' or 'list all prio high' to list across databases all in that state.
 - align state names across all databases. so when an item is active, it is state 'Open' for all (now some has On and Off) and also align on the name of 'OnHold'
 - remove the on hold items and the dormant items from the online report. can add online full command, to see all of the online items
 - FIX: Client say: list 00000006:list Server Said: Transaction: start activity COMPLETED. New ID is: 808 () [seems has repeated what happened before it! did not really create a new one]
 - add capability to print the 'now' activities or send them as email to me
 - error tag @852 tEMAIL 00000040:tag @852 tEMAIL Server Said: Transaction: tag something FAILED with ERROR: tag provided does not meet the formatting ctiteria tTAG
 - for Activity (and Task?) consider adding a state of 'new' before 'started' so 'started' can be something that really started to work with (vs 'new' is just entered to teh database, no action. somewhat like new and acknoledged in hsdes)
 - check/make move command updte lid and cid properly
 - check why lid and cid do not work with move command ?????
 - add a shortcut type like only replacing mv to move (rest of teh command remains the same)
 - when closing a task or a project, check that all the items under it are closed and if not - make a note and do not close.
 - why failing? "edit @578 Description | for CPSV level debug related"
 - 'add' command like 'edit' (or make it edit @id add | bla bla bla) that adds on teh description, not replacing it.
 - check why 'list activity col State is Open' does not work (but list acticity state Dormant works)
 - check why this fails: 'move @979 to @211'
 - check why 'close @979 | done .. and followup activity created' does not work, while 'close @979 | done' works
 - for something like 'start @xxx | task is ...' it tried to create a task ... check if/why
 - add to the html page where for each MEGAPROJECT the (open ?) projects are listed, list also the open tasks, in hierarchy (and make it easy to differentiate them) 
 - check - sometimes there is error in move, when it says something that the 'move to' is not task/project. Check if the list of tasks/projects might not be updated correctly [see if can attache to a running process for this ... (debug capabilit)]
 - add a beep (or two) for success with winsound
 - check: I sent only a 'list' command, and the result was a redo of the previous command ... it was not recognized as partial command and since list keeps the context of teh previous comand, it just did it!
 - the following command "list activity col Tag inc TODAY" does not work, probably since the tag is a list, and the inc here assumes a string. Make it work for list also
 - add in html listing, that if an item has a comment, there is a star added to it somewhere, THis is to see I have placed a comment for myself on thsi item
 - add to 'online' also the list of the 'now' activities
 - 
 - 
 - search to TODO and fix
 - document all commands
 - END
      



 



# weekly

## opens/unknowns

## system settings
**need to have the following system variables**\
"mgdt_code_path" = "C:\Users\oeitam\OneDrive - Intel Corporation\Documents\Z-Work\Projects\mgtd"
"mgdt_local_path" = "C:\mgtd.local"

## more
1. added ability to run commands before the client sends a first command in prod and in dev modes/
the list of commands is in the defs.py file
2. the files locations are parametrized in defs.py
3. when exiting (die), the program zips the local directory (parametrized, but usually c:\mgtd.local) and stores it in the code location (parametrized as well) in a directory named 'datastore'. The zipped files are created with a time tag as the name. They are not stored in github.
4. 

## run environment, dev and production envs
1. the system supports 3 operational modes: developement, production and demo (demo is not really used as of MAr 24)
2. each of the 3 environments has a completely seperate databases and a seperate configuration file
3. all the run data (config files, utility scripts and the databses) are in c:\mgtd.local directotry (parametrized)
### content of c:/mgtd.local [let us define ENVS as developement or demo or production]
 - developement, production, demo folders with teh databases and html files in them
 - mgtf.local.cfg file which is the config file in use when mgtd starts
 - mgtd.local.ENVS.cfg are the (3) config files for each environment. see 'GoTo' scripts
 - GoToENVS.py scripts - when mgtd is NOT running, run these python scripts to change the envoronment.
 - - the script find what envirnoment was last used, saves the mgtd.local.cfg as mgtd.local.ENVS.cfg file as appropriate and copies the GoTo env config file to mgtd.local.cfg. next time mgtd is run is in teh new environment being set. 
 - There are other files in teh directory which are obsolete or old or whatever
### test/developement mode vs production mode operation
 - the file to run is always mgtd.py as the starting script
 - two "mode"s are supported for communication 'prod' for production and 'direct' for validation (used in developement environment)
 - if mode is 'prod', the client used is the **client_script.py**' file which waits for user inputs and sends outputs to teh user process.\
 the file mgtd_wt.ps1 calls the server and then the client_script.py
 - if mode is 'direct' the server.init and server.server_process methods use the '**client_direct.py**' script to process commands in the test_defs.py file


## Operation
this describes points how I use it (Jan 2024)\
in powershell (wt) console:

        PS C:\mgtd.local> & powershell.exe '.\mgtd_wt.ps1'


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

    create project P1 @MP1 tag tTAG | some comment about the project


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

### stop, close
stop >> puts an item into terminal state: Activity to state Ended, Task to state Closed, Project to state Ended\
update the relevant fields.

      stop @some_id
Can use the term 'close' in exactly the same manner

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
 
 - tag >> list all items with tag tTAG'\
    `list tag tTAG`
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
Notes:
 - when moving, it does not update activity dfa column "Project" with the project number, but rather with project name (fix) ?
### tag
tag with no-spaces in this format tTAG
* does not allow for duplications per item
* can tag a project by name. Task/activity by ID
* can be used for context
* multiple tags allowed
* searchable (list tag command)
###
    tag @1234 tTAG
    untag @1234 tTAG
    tag project progect_name tTAG
    untag project progect_name tTAG

see list tag

### edit
Allows to edit (== replace) fields for record/
for megaproject - replace Name or Description
for the rest - replace only Description

        edit @ID Description | here enter the new description that will replace the former one
        edit @ID Name | NEW_NAME 

[Note: megaproject name is only upper case]


### import (not implemented)
import is a single word command\
it takes the file in mgdt_local_path/import_commands.txt\
and executes each line as if it was a command by the client\
remarks (only as teh first char in a line) is marked by # \
empty lines are ignored


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







