
import os.path
#import numpy as np
import os
import pandas as pd
import numpy as np
import logging
import re
import win32clipboard

import io
from datetime import datetime
from tabulate import tabulate

from src import defs
#from test import test_defs
#from shutil import move,copyfile
from terminaltables import AsciiTable
from textwrap import wrap

from datetime import datetime, date, timedelta #, time
from ast import literal_eval
import math

one_week = timedelta(days=7)

pd.options.display.max_colwidth = 100 # 50 by defaul
#pd.set_option('colheader_justify', 'left')

# this is an addition from home on local
# and this is from work local

def myconv(x):
    #if x is not '':
    if x != '':
        return str(int(float(x)))

def date_conv(ds):
    ds1,ds2,ds3 = ds.partition('.')
    st1 = defs.days_of_week.get(ds3, None)
    if not st1: # meaning - None
        raise ValueError
    r = datetime.strptime(ds1 + st1, "%yww%W-%w")
    if ds3 == 'Sun':
        r = r - one_week
    return(r)


def date_conv_max_date(ds):
    if isinstance(ds, str) :
        ds1,ds2,ds3 = ds.partition('.')
        st1 = defs.days_of_week.get(ds3, None)
        if not st1: # meaning - None
            raise ValueError
        r = datetime.strptime(ds1 + st1, "%yww%W-%w")
        if ds3 == 'Sun':
            r = r - one_week
        return(r.date())
    else:
        return defs.future


def mycnv2(x,other_df,str_to_cmp):
    if type(x) == str and x != '':
        return other_df.loc[int(x)]['Name'] == str_to_cmp
    else:
        return False

def print_a_list(val):
    return "test 1-\n-test 2"
    return val.replace('\n', '<br>')

    # output = io.StringIO()
    # for i in l:
    #     print(i.replace("\n","\<br\>"),file=output)
    #     #print(i)
    # return output.getvalue()


def search_in_df(x,list_to_fill,pat):
    for i in x:
        if pat in str(i):
            list_to_fill.append(int(x.name))
            return True
    return False

def if_list_find_item(item, tag):
    if type(item) == list:
        if tag in item:
            return True
    return False

def if_list_and_not_empty(item):
    if type(item) == list:
        if len(item) > 0:
            return True
    return False


logger = logging.getLogger(__name__)

conv = lambda x: str(int(x)) if not math.isnan(x) else 'N/A'

class Db(object):
    def __init__(self):
        # set up or load the databases. Those will be in the form of pandas DataFrame
        # databases table
        self.dfm = None
        self.dfp = None
        self.dft = None
        self.dfa = None

        # start fresh
        self.clean_context(sec0=True)

        # timedelta
        self.tdelta = timedelta(days=0)

        self.db_table = {'dfm': self.dfm,
                         'dfp': self.dfp,
                         'dft': self.dft,
                         'dfa': self.dfa,
                         }

        self.load_dbs()
        self.get_new_ID(1) # the 1 means this is the a setup - that is - check the file is here etc
        # create the operations_bucket
        self.operation_bucket = { "create project"     : self.create_project,
                                  "create megaproject" : self.create_megaproject,
                                  "create task"        : self.create_task,
                                  'start activity'     : self.start_activity,
                                  'stop something'     : self.stop_something,
                                  'cont something'     : self.cont_something,
                                  'halt something'     : self.halt_something,
                                  'sleep something'    : self.sleep_something,
                                  'list id'            : self.list_id,
                                  'list megaproject'   : self.list_glob,
                                  'list project'       : self.list_glob,
                                  'list task'          : self.list_glob,
                                  'list activity'      : self.list_glob,
                                  'list for'           : self.list_glob,
                                  'list html'          : self.list_html,
                                  'list search'        : self.list_search,
                                  'list wakeup'        : self.list_wakeup,
                                  'help'               : self.help_message,
                                  'delete id'          : self.delete_id,
                                  'online'             : self.online_check,
                                  'create list'        : self.create_list,
                                  'move list'          : self.move_items,
                                  'move task'          : self.move_items,
                                  'move activity'      : self.move_items,
                                  'move item'          : self.move_items,
                                  'set param'          : self.set_param,
                                  'list parameter'     : self.list_parameter,
                                  'list shortcut'      : self.list_shortcut,
                                  'create shortcut'    : self.create_shortcut,
                                  'delete shortcut'    : self.delete_shortcut,
                                  'tag something'      : self.tagging,
                                  'untag something'    : self.tagging,
                                  'tag project'        : self.tagging_project,
                                  'untag project'      : self.tagging_project,
                                  'list tag'           : self.list_tag,
                                  'tag list'           : self.tag_list,
                                  'list list'          : self.list_list,
                                  'timedelta'          : self.tdelta_func,
                                  'swap'               : self.swap,
                                  'add comment'        : self.add_comment,
                                  'set priority'       : self.set_priority,
                                  'edit id'            : self.edit_item_field,
                                  'import file'        : self.import_file,    
                                  #'list project'       : self.list_project,
                                  #'list task'          : self.list_task,
                                  #'list activity'      : self.list_activity,
                                  }


        logger.debug("class Db initialized")

    ###################################
    # returns to caller the ID it
    # reads from the file, and sets into the file
    # the next ID (+1)
    ###################################
    def get_new_ID(self, mode = 0):
        path_to_ID_file = defs.data_loc + '\\ID'
        if not os.path.isfile(path_to_ID_file):
            fb = open(path_to_ID_file,'w')
            fb.write('100')
            fb.close()
        #print(path_to_ID_file)
        fh = open(path_to_ID_file, 'r+')
        cID = int(fh.read())
        fh.seek(0)
        fh.write(str(cID+1)) # increase by 1 for next time
        if mode == 1:
            logger.debug('Starting with ID {}'.format(cID))
        logger.debug('ID is: {}'.format(cID))
        fh.close()
        if mode == 1:
            return -1
        else:
            self.pID = cID
            return cID

        ###################################
        # returns to caller the ID it
        # reads from the file,
        # does not advance the ID !!
        ###################################
    def get_current_ID(self):
        path_to_ID_file = defs.data_loc + '\\ID'
        if not os.path.isfile(path_to_ID_file):
            fb = open(path_to_ID_file,'w')
            fb.write('100')
            fb.close()
        fh = open(path_to_ID_file, 'r')
        cID = int(fh.read())
        logger.debug('current ID is: {}'.format(cID))
        fh.close()
        return cID

    # expecting date (like date.today())
    def get_time_str(self, d = None, timedel = None):
        #d = date.today()
        if d is None:
            d = date.today()
        if timedel :
            d = d + timedel
        d = d - self.tdelta # if timedelta exists, use it
        tt = d.timetuple()
        #y = str(tt[0])[2:4]
        if tt[6] == 6:  # if a sunday, need to advance ww by one
        #    ww = str(d.isocalendar()[1] + 1).zfill(2)
            ww = (d + timedelta(days=1)).strftime("%V")
            y  = (d + timedelta(days=1)).strftime("%y")
        else:
        #    ww = str(d.isocalendar()[1]).zfill(2)
            ww = d.strftime("%V")
            y  = d.strftime("%y")

        wd = d.strftime('%a')
        a = y + "ww" + ww + "." + wd
        return a







    ####################################
    # setting up 4 databases
    # metaprojects: dbm
    # projects    : dbp
    # tasks       : dbt
    # activities  : dba
    ####################################
    def load_dbs(self):
        logger.debug('setting up databases')
        # check if the file for the database exists
        # load only if exists
        # otherwise - set to None
        #metaproj
        if os.path.isfile(defs.data_loc + '/dfm.csv'):
            self.dfm = pd.read_csv(defs.data_loc + '/dfm.csv',\
                           converters={'PROJECTs_List': literal_eval,\
                                       'Comments'     : literal_eval,
                                       })
            self.dfm.set_index('ID', inplace=True)
            self.db_table['dfm'] = self.dfm
        else:
            self.dfm = None
        # proj
        if os.path.isfile(defs.data_loc + '/dfp.csv'):
            self.dfp = pd.read_csv(defs.data_loc + '/dfp.csv',\
                           converters={'Tag'        : literal_eval,\
                                       'State_Time' : literal_eval,\
                                       'State_Text' : literal_eval,\
                                       'Comments'   : literal_eval,
                                       })
            self.dfp.set_index('ID', inplace=True)
            self.db_table['dfp'] = self.dfp
        else:
            self.dfp = None
        # task
        if os.path.isfile(defs.data_loc + '/dft.csv'):
            self.dft = pd.read_csv(defs.data_loc + '/dft.csv',\
                           converters={'ACTIVITYs'  : literal_eval,\
                                       'Sub_TASKs'  : literal_eval,\
                                       'Tag'        : literal_eval,\
                                       'State_Time' : literal_eval,\
                                       'State_Text' : literal_eval,\
                                       'Comments'    : literal_eval,
                                       })
            self.dft.set_index('ID', inplace=True)
            self.db_table['dft'] = self.dft
        else:
            self.dft = None
        # activity
        if os.path.isfile(defs.data_loc + '/dfa.csv'):
            self.dfa = pd.read_csv(defs.data_loc + '/dfa.csv',\
                           converters={'TASK'       : myconv,\
                                       'PROJECT'    : myconv,\
                                       'Tag'        : literal_eval,\
                                       'State_Time' : literal_eval,\
                                       'State_Text' : literal_eval,\
                                       'Comments'    : literal_eval,
                                       })
            self.dfa.set_index('ID', inplace=True)
            self.db_table['dfa'] = self.dfa
        else:
            self.dfa = None

    # the purpose of this function is to clean all the
    # relevant 'self' variables to avoid information
    # form one transaction affecting the other transaction
    def clean_context(self, sec1=True, sec2=True, sec0 = False):
        if sec0: #put here things that need to be initialized just once at the beginning
            self.substitution_happened = 'clean'
        if sec1:
            self.pID                    = -1
            self.use_this_ID_for_ref    = -1
            self.second_ref_ID          = -1
            self.project_name           = 'clean'
            self.megaproject_name       = 'clean'
            #self.megaproject_name       = 'clean'
            self.transaction_type       = 'clean'
            self.list_resp              = 'clean'
            self.error_details          = 'clean'
            self.trans_description      = 'clean'
            self.return_message         = 'clean'
            self.return_message_ext1    = 'clean'
            self.keep_context           = False
            self.list_col_name          = 'clean'
            self.list_col_value         = 'clean'
            self.list_col_rel           = 'clean'
            self.list_col_bot           = 'clean'
            self.list_col_top           = 'clean'
            self.list_what_for          = 'clean'
            self.list_for_what          = 'clean'
            self.list_for_val           = 'clean'
            self.list_attr              = 'clean'
            self.list_ww                = 'clean'
            self.state_to_list          = 'clean'
            self.wakeup_time            = 'clean'
            self.help_search            = 'clean'
            self.move_from              = 'clean'
            self.move_to                = 'clean'
            self.param_to_set           = 'clean'
            self.value_to_set           = 'clean'
            self.shortcut_to_delete     = 'clean'
            self.tag                    = 'clean'
            self.item_to_tag_or_untag   = 'clean'
            self.tdelta_param           = 'clean'
            self.list_all               = 'clean'
            self.lastdays               = 'clean'
            self.fromcb                 = 'clean'
            self.edit_column_name       = 'clean'
            #self.trans_description      = 'clean'
            self.comment_to_add         = 'clean'
            self.priority_to_set        = 'clean'
            self.success_response       = 'clean'
            if self.substitution_happened[:4] != 'Simp': #handlinlg only simple substitutions for now. TODO
                self.substitution_happened  = 'clean'
            if hasattr(defs,'list_resp_row_limit'):
                self.list_resp_row_limit = defs.list_resp_row_limit
            else:
                self.list_resp_row_limit    = 15
            self.list_resp_rows         = -1
        if sec2:
            self.items_list             = ['clean']

    def store_context(self):
        if hasattr(defs, 'list_resp_row_limit'):
            self.list_resp_row_limit = defs.list_resp_row_limit
        else:
            self.list_resp_row_limit = 15
        self.last_list_resp_rows = -1

    # add a dataframe to a db
    # if the db does not exist yet, create it
    def add_to_db(self, which_db, df_to_add):
        db_to_add_to = self.db_table[which_db]
        # here I assume that the df_to_add matches the db_to_add_to
        # so I do not do any checking
        if db_to_add_to is None:
            # need to create the data base
            db_to_add_to = pd.DataFrame(df_to_add)
            db_to_add_to.index.name = 'ID'
            if which_db == 'dfm':
                self.dfm = db_to_add_to
                self.db_table[which_db] = self.dfm
            elif which_db == 'dfp':
                self.dfp = db_to_add_to
                self.db_table[which_db] = self.dfp
            elif which_db == 'dft':
                self.dft = db_to_add_to
                self.db_table[which_db] = self.dft
            else:
                self.dfa = db_to_add_to
                self.db_table[which_db] = self.dfa
        else: # here we assume that the databaser alrad has an index 'ID'
            if which_db == 'dfm':
                self.dfm = pd.concat([self.dfm, df_to_add])
                self.db_table[which_db] = self.dfm
            if which_db == 'dfp':
                self.dfp = pd.concat([self.dfp, df_to_add])
                self.db_table[which_db] = self.dfp
            if which_db == 'dft':
                self.dft = pd.concat([self.dft, df_to_add])
                self.db_table[which_db] = self.dft
            if which_db == 'dfa':
                self.dfa = pd.concat([self.dfa, df_to_add])
                self.db_table[which_db] = self.dfa

        # this return checks for nothing ... just returnning true
        return True

    def find_in_which_db(self,id):
        # search the id in all databases, and returns the one that has this id:
        # 'dfm', 'dfp', 'dft', 'dfa', 'nowhere'
        if id in list(self.dfm.index.values):
            return 'dfm'
        elif id in list(self.dfp.index.values):
            return 'dfp'
        elif id in list(self.dft.index.values):
            return 'dft'
        elif id in list(self.dfa.index.values):
            return 'dfa'
        else:
            return 'nowhere'


    # save the databases
    def save_databases(self):
        try:
            if self.dfm is not None:
                self.dfm.to_csv(defs.data_loc + '\dfm.csv')
            if self.dfp is not None:
                self.dfp.to_csv(defs.data_loc + '\dfp.csv')
            if self.dft is not None:
                self.dft.to_csv(defs.data_loc + '\dft.csv')
            if self.dfa is not None:
                self.dfa.to_csv(defs.data_loc + '\dfa.csv')
        except:
            #print("Could not save one of the dfx files.\n"+\
            #      "Suggest to make sure no file is open in another app.\n"+\
            #      "Exit now please (die)")
            self.had_error('Could not save databases properly. Please exit (die) and check data integrity!')
            return False

        return True

    # set the project name for the next transaction
    def set_project_name(self, project_name):
        if project_name.isdigit():
            # look for the project 'verbal' name
            if self.dfp is not None:
                if int(project_name) in self.dfp.index:
                    self.project_name = self.dfp.loc[int(project_name)].Name
                else:
                    self.had_error('Cannot find project {}\n'.format(project_name))
            else:
                self.had_error('Project database does not exist.\n')
        else:
            self.project_name = project_name

    # set the project name for the next transaction
    def set_megaproject_name(self, megaproject_name):
        self.megaproject_name = megaproject_name

    # set the description section of the next transaction
    def set_trans_description(self, trans_description):
        self.trans_description = trans_description

    # set the transaction (create project, create task etc)
    def transaction_is(self,transaction_type):
        self.transaction_type = transaction_type

    # this function tells the db to perform the transaction it was programmed to do
    # it returns the success + information about the transaction
    def do_transaction(self):
        res = self.operation_bucket.get(self.transaction_type, self.had_error)()
        if res:
            self.list_html() #after each command operation - update the html files
        if res:
            res2 = self.save_databases()
            if res2:
                self.create_return_message(True)
            else:
                if self.error_details == 'clean':
                    self.had_error()
                self.create_return_message(False)
        else:
            if self.error_details == 'clean':
                self.had_error('Variable error_details was not set')
            self.create_return_message(False)
        return True

    def had_error(self,err_text=''):
        logger.debug("in had_error. Houston - we have a problem!")
        if err_text == '' : #nothing was sent
            self.error_details = 'had_error function was called w/o error text. Could be - command name not find in bucket\n'
        else:
            self.error_details = err_text
        logger.debug(self.error_details)
        return False

    def create_return_message(self, success):
        m = ''
        if 'list ' in self.transaction_type[0:8]:
            if success:
                if self.substitution_happened != 'clean':
                    m = self.substitution_happened
                m += self.list_resp
            else:
                m = "Transaction: {} FAILED with ERROR:\n {}".format(self.transaction_type, self.error_details)
        elif ( 'stop some' in self.transaction_type
            or 'cont some' in self.transaction_type
            or 'sleep some' in self.transaction_type
            or 'halt some' in self.transaction_type) :
            if success:
                if self.substitution_happened != 'clean':
                    m = self.substitution_happened
                m += "Transaction: {} COMPLETED. Referenced ID is: {}".format(self.transaction_type, self.use_this_ID_for_ref)
            else:
                m = "Transaction: {} FAILED with ERROR:\n {}".format(self.transaction_type, self.error_details)
        elif (self.transaction_type == 'help'):
            if self.help_search != 'clean':
                l1 = defs.help_message.split('\n')
                l2 = [k for k in l1 if self.help_search in k]
                if len(l2) == 0 :
                    m = "no help message with specified string"
                else:
                    m = "\n".join(l2)
            else:
                m = defs.help_message
        else:
            if success: #
                if self.success_response == 'clean': # meaning - not set by command
                    self.success_response = '' #must be empty to be used below
                m = "Transaction: {} COMPLETED. New ID is: {} ({})".format(self.transaction_type, self.pID, self.success_response)
                if self.return_message_ext1 != 'clean' or self.substitution_happened != 'clean':
                    if self.substitution_happened != 'clean':
                        m += self.substitution_happened
                    if self.return_message_ext1 != 'clean':    
                        m += self.return_message_ext1
            else:
                m = "Transaction: {} FAILED with ERROR:\n {}".format(self.transaction_type, self.error_details)
        self.substitution_happened = 'clean' # need to wipe it here so it can 'pick up' the substitution value (and it does not retain this value next time ...)
        self.return_message = m

    # transactions functions
    ########################
    def create_project(self):
        # check project name is all lower
        b1 = not self.project_name.islower() # true if not all lower case
        if b1:
            return self.had_error('Project name supplied must be all lower case and no spaces (format project_name)\n')
        # check if project exists
        if self.dfp is not None:
            if (self.project_name) in self.dfp[self.dfp['MEGAPROJECT'] == self.megaproject_name]['Name'].values: # search if the project name exists in the same megaproject
                logger.debug("Request to create an already existing project in the Megaproject {} {}".format(self.project_name, self.dfp['Name'].values))
                self.error_details = "Request to create an already existing project in the Megaproject {} {}".format(self.project_name, self.dfp['Name'].values)
                return False
        # check if the mega project exsists
        if self.dfm is not None:
            if self.megaproject_name not in self.dfm['Name'].values:
                self.error_details = "Request to create a project in a non existing megaproject {}".format(self.megaproject_name)
                logger.debug(self.error_details)
                return False

        pID = self.get_new_ID()

        if self.tag != 'clean': # we have a tag
            tag = [self.tag]
        else:
            tag = []
        # if fromcb was used, then need to compy clipbard into transaction description
        if self.fromcb == 'Yes':
            try:
                win32clipboard.OpenClipboard()
                self.trans_description = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
            except TypeError as e:
                print("win32clipboard error: " + e)
                win32clipboard.CloseClipboard()
        today_str = datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
        today_adjusted_str = (datetime.now()-self.tdelta).strftime("%I:%M:%S%p on %B %d, %Y")
        l = [self.project_name, 'Started', self.megaproject_name, self.trans_description,tag,today_adjusted_str,[],[],[]]
        ldf = pd.DataFrame(data=[l], index=[pID], columns=defs.dfp_columns)
        ldf.index.name = 'ID'
        logger.debug(ldf.to_string())
        res = self.add_to_db(which_db='dfp', df_to_add=ldf)
        # add the new project name to the list of projects in the mega project
        if res:
            t1 = self.dfm['Name'][self.dfm['Name'] == self.megaproject_name].index
            self.dfm['PROJECTs_List'][t1[0]].append(self.project_name)
        if res:
            return True
        else:
            self.error_details = "Failed to add a new project {} to the database([])".format(self.project_name, self.pID)
            logger.debug(self.error_details)
            return False

    def create_megaproject(self):
        # check megaproject name is all upper
        b1 = not self.megaproject_name.isupper() # true if not all lower case
        if b1:
            return self.had_error('Megaproject name supplied must be all upper case and no spaces (format MEGAPROJECT_MORE)\n')
        # check if project exists
        if self.dfm is not None:
            if (self.megaproject_name) in self.dfm['Name'].values:
                ret = "Request to create an already existing megaproject {}".format(self.megaproject_name)
                logger.debug(ret)
                #self.error_details = ret
                #temp return False TODO
        # regardless if the this is the first megaproject or not ...
        pID = self.get_new_ID()
        # if fromcb was used, then need to compy clipbard into transaction description
        if self.fromcb == 'Yes':
            try:
                win32clipboard.OpenClipboard()
                self.trans_description = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
            except TypeError as e:
                print("win32clipboard error: " + e)
                win32clipboard.CloseClipboard()
        l = [self.megaproject_name, 'On', [], self.trans_description, []]
        ldf = pd.DataFrame(data=[l], index=[pID], columns=defs.dfm_columns)
        ldf.index.name = 'ID'
        logger.debug(ldf.to_string())
        self.add_to_db(which_db='dfm',df_to_add=ldf)
        return True

    # create a task
    # for now - no support for optional
    def create_task(self):
        pID = self.get_new_ID()

        if self.tag != 'clean': # we have a tag
            tag = [self.tag]
        else:
            tag = []
        # if fromcb was used, then need to compy clipbard into transaction description
        if self.fromcb == 'Yes':
            try:
                win32clipboard.OpenClipboard()
                self.trans_description = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
            except TypeError as e:
                print("win32clipboard error: " + e)
                win32clipboard.CloseClipboard()
        today_str = datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
        today_adjusted_str = (datetime.now()-self.tdelta).strftime("(a) %I:%M:%S%p on %B %d, %Y")
        l = ['Open', self.trans_description, self.get_time_str(date.today()),
             self.project_name,tag,'',
             '','','','','',
             [],[],'',today_adjusted_str,[],[],[]]
        ldf = pd.DataFrame(data=[l], index=[pID], columns=defs.dft_columns)
        ldf.index.name = 'ID'
        logger.debug(ldf.to_string())
        self.add_to_db(which_db='dft', df_to_add=ldf)
        return True

    # craete an ACTIVITY
    def start_activity(self):
        pID = self.get_new_ID()
        found_in = 'did not look yet ...'
        # search for the related task or project
        # if the use_this_ID_for_ref was actually given as a project name
        if not self.use_this_ID_for_ref.isdigit() : # it is not just digits
            num = int(self.dfp.index[self.dfp['Name'] == self.use_this_ID_for_ref].tolist()[0])
            if num is not None:
                self.use_this_ID_for_ref = num
                couple = ['', str(int(self.use_this_ID_for_ref))]
                found_in = 'projects'
            else:
                return False
        elif ((self.dfp is not None) and (int(self.use_this_ID_for_ref) in list(self.dfp.index.values))):
            couple = ['', str(int(self.use_this_ID_for_ref))]
            found_in = 'projects'
        elif ((self.dft is not None) and (int(self.use_this_ID_for_ref) in list(self.dft.index.values))) :
            couple = [str(int(self.use_this_ID_for_ref)), ""]
            found_in = 'tasks'
        elif self.use_this_ID_for_ref == 0: # indicating - ci or co (or non related activity)
            couple = ['','']
            found_in = 'not found'
        else: #found none
            self.error_details = 'ID {} from {} was not found'.format(self.use_this_ID_for_ref, found_in)
            logger.debug(self.error_details)
            return False

        if self.tag != 'clean': # we have a tag
            tag = [self.tag]
        else:
            tag = []
        # if fromcb was used, then need to compy clipbard into transaction description
        if self.fromcb == 'Yes':
            try:
                win32clipboard.OpenClipboard()
                self.trans_description = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
            except TypeError as e:
                print("win32clipboard error: " + e)
                win32clipboard.CloseClipboard()
        today_str = datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
        today_adjusted_str = (datetime.now()-self.tdelta).strftime("%I:%M:%S%p on %B %d, %Y")
        l = ['Started', self.get_time_str(date.today()), self.trans_description,tag, '',
             '', ''] + couple + [today_adjusted_str,[],[],[]]
        ldf = pd.DataFrame(data=[l], index=[pID], columns=defs.dfa_columns)
        ldf.index.name = 'ID'
        logger.debug(ldf.to_string())
        self.add_to_db(which_db='dfa', df_to_add=ldf)
        # FOR LATER TODO
        # add this activity to the projets or tasks list
        # for cross reference
        return True

    def cont_something(self):
        # handle activity, and then task and then project
        state = 'idle' # helps understand status
        today_str = datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
        # activity
        if self.dfa is not None:
            state = 'found db'
            if self.use_this_ID_for_ref in self.dfa.index.values:
                state = 'id in db'
                # process
                self.dfa.loc[self.use_this_ID_for_ref, 'State'] = 'Started'
                self.dfa.loc[self.use_this_ID_for_ref, 'End_Time'] = ''
                self.dfa.loc[self.use_this_ID_for_ref, 'Wakeup_Date'] = ''
                self.dfa.loc[self.use_this_ID_for_ref, 'State_Time'].append(today_str)
                if self.trans_description == 'clean':
                    self.dfa.loc[self.use_this_ID_for_ref, 'State_Text'].append('Started > ' + 'NA')
                else:
                    self.dfa.loc[self.use_this_ID_for_ref, 'State_Text'].append('Started > ' + self.trans_description)

        # task
        if (self.dft is not None) and (state != 'id in db'):
            state = 'found db'
            if self.use_this_ID_for_ref in self.dft.index.values:
                state = 'id in db'
                # process
                self.dft.loc[self.use_this_ID_for_ref, 'State'] = 'Open'
                self.dft.loc[self.use_this_ID_for_ref, 'Wakeup_Date'] = ''
                self.dft.loc[self.use_this_ID_for_ref, 'State_Time'].append(today_str)
                if self.trans_description == 'clean':
                    self.dft.loc[self.use_this_ID_for_ref, 'State_Text'].append('Open > ' + 'NA')
                else:
                    self.dft.loc[self.use_this_ID_for_ref, 'State_Text'].append('Open > ' + self.trans_description)
        # project
        if (self.dfp is not None) and (state != 'id in db'):
            state = 'found db'
            if self.use_this_ID_for_ref in self.dfp.index.values:
                state = 'id in db'
                # process
                self.dfp.loc[self.use_this_ID_for_ref, 'State'] = 'Started'
                self.dfp.loc[self.use_this_ID_for_ref, 'State_Time'].append(today_str)
                if self.trans_description == 'clean':
                    self.dfp.loc[self.use_this_ID_for_ref, 'State_Text'].append('Started > ' + 'NA')
                else:
                    self.dfp.loc[self.use_this_ID_for_ref, 'State_Text'].append('Started > ' + self.trans_description)

        if state != 'id in db':
            self.error_details = 'Requested to continue ACTIVITY or TASK or PROJECT {} failed (probably incorrect ID)'\
                .format(self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False
        return True

    def halt_something(self):
        # handle activity, and then task and then project
        state = 'idle' # helps understand status
        today_str = datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
        # activity
        if self.dfa is not None:
            state = 'found db'
            if self.use_this_ID_for_ref in self.dfa.index.values:
                state = 'id in db'
                # process
                self.dfa.loc[self.use_this_ID_for_ref, 'State'] = 'OnHold'
                self.dfa.loc[self.use_this_ID_for_ref, 'Wakeup_Date'] = ''
                self.dfa.loc[self.use_this_ID_for_ref, 'State_Time'].append(today_str)
                if self.trans_description == 'clean':
                    self.dfa.loc[self.use_this_ID_for_ref, 'State_Text'].append('OnHold > ' + 'NA')
                else:
                    self.dfa.loc[self.use_this_ID_for_ref, 'State_Text'].append('OnHold > ' + self.trans_description)
        # task
        if (self.dft is not None) and (state != 'id in db'):
            state = 'found db'
            if self.use_this_ID_for_ref in self.dft.index.values:
                state = 'id in db'
                # process
                self.dft.loc[self.use_this_ID_for_ref, 'State'] = 'OnHold'
                self.dft.loc[self.use_this_ID_for_ref, 'Wakeup_Date'] = ''
                self.dft.loc[self.use_this_ID_for_ref, 'State_Time'].append(today_str)
                if self.trans_description == 'clean':
                    self.dft.loc[self.use_this_ID_for_ref, 'State_Text'].append('OnHold > ' + 'NA')
                else:
                    self.dft.loc[self.use_this_ID_for_ref, 'State_Text'].append('OnHold > ' + self.trans_description)
        # project
        if (self.dfp is not None) and (state != 'id in db'):
            state = 'found db'
            if self.use_this_ID_for_ref in self.dfp.index.values:
                state = 'id in db'
                # process
                self.dfp.loc[self.use_this_ID_for_ref, 'State'] = 'OnHold'
                self.dfp.loc[self.use_this_ID_for_ref, 'State_Time'].append(today_str)
                if self.trans_description == 'clean':
                    self.dfp.loc[self.use_this_ID_for_ref, 'State_Text'].append('OnHold > ' + 'NA')
                else:
                    self.dfp.loc[self.use_this_ID_for_ref, 'State_Text'].append('OnHold > ' + self.trans_description)

        if state != 'id in db':
            self.error_details = 'Request to halt ACTIVITY or TASK or PROJECT {} failed (probably incorrect ID)'\
                .format(self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False
        return True

    def sleep_something(self):
        # find the wakeup time
        if self.wakeup_time != 'clean':
            m0 = re.match('(\d\d)ww(\d\d)$', self.wakeup_time)
            if m0 :
                self.wakeup_time += ".Sun"
            m1 = re.match('(\d\d)ww(\d\d)\.[a-zA-Z]{3}', self.wakeup_time)
            if not m1 : # if no match, need to convert to work week
                m2 = re.match('\d{8}',self.wakeup_time)
                if m2 : # this is a YYYYMMDD date
                    y = int(self.wakeup_time[0:4])
                    m = int(self.wakeup_time[4:6])
                    d = int(self.wakeup_time[6:8])
                    dt = date(y,m,d)
                    self.wakeup_time = self.get_time_str(dt)
                else: # so this is a "plus XX" type of
                    m3 = re.match('plus (\d+)',self.wakeup_time)
                    if m3 :
                        timedel = timedelta(days=int(m3.groups(1)[0]))
                        self.wakeup_time = self.get_time_str(timedel=timedel)
        else: # no wake up time set - error
            self.error_details = 'Request to sleep ACTIVITY or TASK {} failed because no wakeup time provided'\
                .format(self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False

        # handle activity, and then task
        state = 'idle' # helps understand status
        today_str = datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")

        # activity
        if self.dfa is not None:
            state = 'found db'
            if self.use_this_ID_for_ref in self.dfa.index.values:
                state = 'id in db'
                # process
                self.dfa.loc[self.use_this_ID_for_ref, 'State'] = 'Dormant'
                if self.wakeup_time != 'clean':
                    self.dfa.loc[self.use_this_ID_for_ref, 'Wakeup_Date'] = self.wakeup_time
                self.dfa.loc[self.use_this_ID_for_ref, 'State_Time'].append(today_str)
                if self.trans_description == 'clean':
                    self.dfa.loc[self.use_this_ID_for_ref, 'State_Text'].append('Dormant > ' + 'NA')
                else:
                    self.dfa.loc[self.use_this_ID_for_ref, 'State_Text'].append('Dormant > ' + self.trans_description)

        # task
        if (self.dft is not None) and (state != 'id in db'):
            state = 'found db'
            if self.use_this_ID_for_ref in self.dft.index.values:
                state = 'id in db'
                # process
                self.dft.loc[self.use_this_ID_for_ref, 'State'] = 'Dormant'
                if self.wakeup_time != 'clean':
                    self.dft.loc[self.use_this_ID_for_ref, 'Wakeup_Date'] = self.wakeup_time
                self.dft.loc[self.use_this_ID_for_ref, 'State_Time'].append(today_str)
                if self.trans_description == 'clean':
                    self.dft.loc[self.use_this_ID_for_ref, 'State_Text'].append('Dormant > ' + 'NA')
                else:
                    self.dft.loc[self.use_this_ID_for_ref, 'State_Text'].append('Dormant > ' + self.trans_description)

        if state != 'id in db':
            self.error_details = 'Request to sleep ACTIVITY or TASK {} failed (probably incorrect ID)'\
                .format(self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False
        return True




    def stop_something(self):
        # handle activity, and then task and then project
        state = 'idle' # helps understand status
        today_str = datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
        # activity
        if self.dfa is not None:
            state = 'found db'
            if self.use_this_ID_for_ref in self.dfa.index.values:
                state = 'id in db'
                # process
                self.dfa.loc[self.use_this_ID_for_ref, 'State'] = 'Ended'
                self.dfa.loc[self.use_this_ID_for_ref, 'Wakeup_Date'] = ''
                self.dfa.loc[self.use_this_ID_for_ref, 'State_Time'].append(today_str)
                if self.trans_description == 'clean':
                    self.dfa.loc[self.use_this_ID_for_ref, 'State_Text'].append('Ended > ' + 'NA')
                else:
                    self.dfa.loc[self.use_this_ID_for_ref, 'State_Text'].append('Ended > ' + self.trans_description)

        # task
        if (self.dft is not None) and (state != 'id in db'):
            state = 'found db'
            if self.use_this_ID_for_ref in self.dft.index.values:
                state = 'id in db'
                # process
                self.dft.loc[self.use_this_ID_for_ref, 'State'] = 'Closed'
                self.dft.loc[self.use_this_ID_for_ref, 'Wakeup_Date'] = ''
                self.dft.loc[self.use_this_ID_for_ref, 'State_Time'].append(today_str)
                if self.trans_description == 'clean':
                    self.dft.loc[self.use_this_ID_for_ref, 'State_Text'].append('Closed > ' + 'NA')
                else:
                    self.dft.loc[self.use_this_ID_for_ref, 'State_Text'].append('Closed > ' + self.trans_description)
        # project
        if (self.dfp is not None) and (state != 'id in db'):
            state = 'found db'
            if self.use_this_ID_for_ref in self.dfp.index.values:
                state = 'id in db'
                # process
                self.dfp.loc[self.use_this_ID_for_ref, 'State'] = 'Ended'
                self.dfp.loc[self.use_this_ID_for_ref, 'State_Time'].append(today_str)
                if self.trans_description == 'clean':
                    self.dfp.loc[self.use_this_ID_for_ref, 'State_Text'].append('Ended > ' + 'NA')
                else:
                    self.dfp.loc[self.use_this_ID_for_ref, 'State_Text'].append('Ended > ' + self.trans_description)

        if state != 'id in db':
            self.error_details = 'Request to stop ACTIVITY or TASK or PROJECT {} failed (probably incorrect ID)'\
                .format(self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False
        return True


    def list_id(self):
        # find the ID
        if self.use_this_ID_for_ref in self.dfm.index.values:
            this = "Megaproject"
            temp = pd.DataFrame([self.dfm.loc[self.use_this_ID_for_ref]])
            self.list_resp = 'listing a megaproject: \n'
            self.list_resp += tabulate(temp.T, headers=[this, temp.index.values[0]], tablefmt='psql') # temp.to_string(na_rep='N/A', float_format=conv, index_names=True, justify='left')
        elif self.use_this_ID_for_ref in self.dfp.index.values:
            this = "Project"
            temp = pd.DataFrame([self.dfp.loc[self.use_this_ID_for_ref]])
            self.list_resp = 'listing a project: \n'
            self.list_resp += tabulate(temp.T, headers=[this, temp.index.values[0]], tablefmt='psql') # temp.to_string(na_rep='N/A', float_format=conv, index_names=True, justify='left')
        elif self.use_this_ID_for_ref in self.dft.index.values:
            this = "Task"
            temp = pd.DataFrame([self.dft.loc[self.use_this_ID_for_ref]])
            self.list_resp = 'listing a task: \n'
            self.list_resp += tabulate(temp.T, headers=[this, temp.index.values[0]], tablefmt='psql') # temp.to_string(na_rep='N/A', float_format=conv, index_names=True, justify='left')
        elif self.use_this_ID_for_ref in self.dfa.index.values:
            this = "Activity"
            temp = pd.DataFrame([self.dfa.loc[self.use_this_ID_for_ref]])
            self.list_resp = 'listing an activity: \n'
            self.list_resp += tabulate(temp.T, headers=[this, temp.index.values[0]], tablefmt='psql') # temp.to_string(na_rep='N/A', float_format=conv, index_names=True, justify='left')
        else: # did not find it
            self.error_details = 'Requested ID {} to list was not found'.format(self.use_this_ID_for_ref)
            logger.debug(self.error_details)
            return False
        return True

    def list_glob(self):
        # check if listing attributes
        if self.list_attr != 'clean':
            self.list_attributes()
            return True
        # set the right database
        if self.transaction_type == 'list megaproject':
            which_db = 'dfm'
        elif self.transaction_type == 'list project':
            which_db = 'dfp'
        elif self.transaction_type == 'list task':
            which_db = 'dft'
        elif self.transaction_type == 'list activity':
            which_db = 'dfa'
        elif self.transaction_type == 'list html':
            which_db = 'all'
        elif self.transaction_type == 'list for' :
            if self.list_what_for == 'megaproject':
                which_db = 'dfm'
            elif self.list_what_for == 'project':
                which_db = 'dfp'
            elif self.list_what_for == 'task':
                which_db = 'dft'
            elif self.list_what_for == 'activity':
                which_db = 'dfa'
            else:
                which_db = 'dfm'  # stam
        else:
            which_db = 'dfm' # stam
        
        # handle list html which may be strait forward and then go back to the support for rest
        if self.transaction_type == 'list html':
            self.list_html()
        else: # all teh rest
            df = self.db_table[which_db]

            # apply the state, if exists, we are listing for
            df = self.apply_state_to_df(df, which_db)

            # apply the tag, if exists, we are listing for
            df = self.apply_tag_to_df(df)

            # if lastdays is set - manipulating the needed parameters to generate that listing
            if self.lastdays != 'clean':
                # list task col Start_Date drange 18ww13 top
                self.list_col_name = 'Start_Date'
                self.list_col_rel = 'drange'
                self.list_col_bot = self.get_time_str(timedel=timedelta(days=-self.lastdays))
                self.list_col_top = 'top' # meaning - up to today



            if df is not None:
                if self.list_col_name != 'clean':
                    if self.list_col_rel == 'is':
                        df = df[df[self.list_col_name] == self.list_col_value]
                    elif self.list_col_rel == 'inc':
                        df = df[df[self.list_col_name].str.contains(self.list_col_value)]
                    if self.list_col_rel == 'not':
                            df = df[df[self.list_col_name] != self.list_col_value]
                    elif self.list_col_rel == 'ninc':
                        df = df[df[self.list_col_name].str.contains(self.list_col_value)==False]
                    elif self.list_col_rel == 'irange':
                        if self.list_col_name == 'ID': # handling ID values
                            if self.list_col_bot.isdigit() and self.list_col_top.isdigit():    #val -> val
                                df = df.loc[int(self.list_col_bot):int(self.list_col_top)]
                            elif self.list_col_bot.isdigit() and self.list_col_top == 'top':   #val -> top
                                df = df.loc[int(self.list_col_bot):]
                            elif self.list_col_bot == 'bot' and self.list_col_top.isdigit():   #bot -> val
                                df = df.loc[:int(self.list_col_top)]
                            elif self.list_col_bot == 'bot' and self.list_col_top == 'top':   #bot -> top
                                pass # actually - it is simply all
                    elif self.list_col_rel == 'drange': #handling of range of dates
                        if self.list_col_bot != 'bot' and self.list_col_top != 'top':  # val -> val
                            df1 = df[df[self.list_col_name].apply(date_conv) >= date_conv(self.list_col_bot)].copy()
                            df2 = df[df[self.list_col_name].apply(date_conv) <= date_conv(self.list_col_top)].copy()
                            #df = pd.merge(df1, df2, how='inner',
                            #              left_on=defs.columns_to_print_table[which_db],
                            #              right_on=defs.columns_to_print_table[which_db],
                            #              left_index=True, right_index=True)
                            #df = df1.merge(df2,left_index=True,right_index=True)#.sort_index()
                            df  = pd.merge(df1,df2,on=defs.columns_to_print_table[which_db],left_index=True,right_index=True)
                        elif self.list_col_bot != 'bot' and self.list_col_top == 'top':  # val -> top
                            df = df[df[self.list_col_name].apply(date_conv) >= date_conv(self.list_col_bot)]
                        elif self.list_col_bot == 'bot' and self.list_col_top != 'top':  # bot -> val
                            df = df[df[self.list_col_name].apply(date_conv) <= date_conv(self.list_col_top)]
                        elif self.list_col_bot != 'bot' and self.list_col_top == 'top':  # bot -> top
                            pass
                    else:
                        self.had_error()
                elif self.transaction_type == 'list for':
                    df = self.list_for()
                    if df is not None:
                        df = self.apply_state_to_df(df, which_db)
                        # apply the tag, if exists, we are listing for
                        df = self.apply_tag_to_df(df)
                elif self.list_ww != 'clean':
                    df = df[df['Start_Date'].str.contains(self.list_ww)]
                    if df is not None:
                        df = self.apply_state_to_df(df, which_db)
                        # apply the tag, if exists, we are listing for
                        df = self.apply_tag_to_df(df)

                if self.list_resp_rows == -1 : # means this is the first time we handle the specific lsit
                    self.list_resp_rows = len(df)
                if self.list_resp_rows == 0 : # meaning-  we finished showing all
                    self.list_resp = "No more data to show"
                    return True
                t1 = self.list_resp_rows
                # handle the case of list all
                if self.list_all == 'Yes':
                    t2 = 0
                else:
                    t2 = max(self.list_resp_rows - self.list_resp_row_limit ,0)
                resp_title  = self.transaction_type + ": " + "Showing items {} to {}:".format(t2+1,max(t1,0))
                resp_cont_1 = self.df_to_list_resp(df[t2:t1], which_db, resp_title)
                if defs.use_tables == 'no':
                    self.list_resp = resp_title + '\n'+ resp_cont_1
                else:
                    self.list_resp = resp_cont_1

                self.list_resp_rows = t2
            else:  # did not find it
                self.error_details = 'No SOMETHING to list'
                logger.debug(self.error_details)
                return False
            return True

    def apply_state_to_df(self, df, which_db):
        # apply the state, if exists, we are listing for
        if self.state_to_list != 'all':
            if self.state_to_list == 'clean':
                self.state_to_list = defs.state_open[which_db]
            df = df[df['State'] == self.state_to_list]
        return df

    def apply_tag_to_df(self, df):
        if self.tag == 'clean':
            return df
        if self.tag == 'any-tag-at-all':
            return df
        df = df[df['Tag'].\
                apply(if_list_find_item, args=(self.tag,)) == True]
        return df




    def df_to_list_resp(self, df, which_db, title):
        if defs.use_tables == 'no':
            s = df.to_string(
                columns=defs.columns_to_print_table[which_db],
                na_rep='N/A', float_format=conv, index_names=True, justify='left')
            s = s + '\n'
            return s
        elif defs.use_tables == 'ascii':
            csv_str = df.to_csv(sep='|',
                columns=defs.columns_to_print_table[which_db],
                na_rep='N/A')#, float_format=conv, index_names=True, justify='left')
            l = []
            q = defs.columns_to_print_table[which_db][:]
            q.insert(0, 'ID')
            l.append(q)
            c = 0
            for line in csv_str.splitlines():
                if c == 0:
                    c = c + 1
                    continue
                sl = line.split('|')
                for i in range(0,len(sl)):
                    if len(sl[i]) > defs.max_width:
                        sl[i] = '\n'.join(wrap(sl[i], defs.max_width))
                l.append(sl)
            table_instance = AsciiTable(l,title)
            #table_instance.justify_columns[3] = 'right'
            #table_instance.justify_columns[2] = 'right'

            #print("=====================================")
            #self.myprint(df,which_db,title)
            #print("=====================================")

            return table_instance.table
        else:
            return False

    # process for the list for command, and return a df that corresponds to the search
    def list_for(self):
        df = None
        if self.list_what_for == 'megaproject' and self.list_for_what == 'project':
            df = self.dfm[self.dfm['PROJECTs_List'].apply(lambda x: self.list_for_val in x)]
        elif self.list_what_for == 'project' and self.list_for_what == 'megaproject':
            df = self.dfp[self.dfp['MEGAPROJECT'] == self.list_for_val]
        elif self.list_what_for == 'task' and self.list_for_what == 'project':
            df = self.dft[self.dft['PROJECT'] == self.list_for_val]
        elif self.list_what_for == 'activity' and self.list_for_what == 'project':
            df = self.dfa[self.dfa['PROJECT'].apply(mycnv2,args=(self.dfp,self.list_for_val))]
        elif self.list_what_for == 'activity' and self.list_for_what == 'task':
            if not self.list_for_val.isdigit():
                self.had_error()
            df = self.dfa[self.dfa['TASK'] == self.list_for_val]
        if df is None:
            self.error_details = 'List for unsuccessful'
            self.had_error()
            logger.debug(self.error_details)
        return df

    # print attributes
    def list_attributes(self):
        if self.list_attr == 'columns':
            s1,s2,wtp = self.transaction_type.partition(' ')
            ltp = defs.all_col[wtp]
            self.list_resp = "Showing columns for {}s:\n".format(wtp)
            for i in ltp:
                self.list_resp += i + '\n'
            #
        elif self.list_attr == 'states':
            s1, s2, wtp = self.transaction_type.partition(' ')
            dtp = defs.all_stat[wtp]
            self.list_resp = "Showing states for {}s:\n".format(wtp)
            for i in dtp.keys():
                self.list_resp += ("{:9}".format(i) + " : " + dtp[i] + '\n')


    # global search
    # the search for value is in self.transaction_description
    def list_search(self):
        self.list_resp = 'Searching for {}:\n'.format(self.trans_description)
        for df_name in ['dfm', 'dfp', 'dft', 'dfa']:
            self.list_resp += "\nResults from {}\n".format(defs.db_names[df_name])
            df = self.db_table[df_name]
            l = []
            df.apply(search_in_df, axis=1, args = (l,self.trans_description.lstrip()))
            if len(l) == 0: # nothing found
                self.list_resp += 'well ... nothing found here\n'
            else:
                df = df.loc[l]
                self.list_resp += self.df_to_list_resp(df, df_name,'list search results')
        return True

    # print out wakeup tasks and activities
    def list_wakeup(self):
        self.list_resp = 'Searching for TASK and ACTIVITY in Dormant state what Wakeup time is this week or past{}:\n\n'
        for df_name in ['dft', 'dfa']:
            #self.list_resp += "\nResults from {}\n".format(defs.db_names[df_name])
            title = "Results from {}".format(defs.db_names[df_name])
            df = self.db_table[df_name]
            df1 = df[df['State'] == 'Dormant']
            if len(df1) == 0: # nothing found
                self.list_resp += 'well ... nothing found here at {}.\n'.\
                    format(defs.db_names[df_name])
            else:
                # calculate end of this week for comparison
                d = date.today()
                ws = d-timedelta(days=d.weekday())
                we = ws + timedelta(days=6)
                we = we + defs.debug_delta
                df2 = df1[df1['Wakeup_Date'].apply(date_conv_max_date).array <= we].copy()
                if len(df2) == 0: # nothing found
                    self.list_resp += 'well ... nothing found here at {}.\n'.\
                        format(defs.db_names[df_name])
                else:
                    # in order to sort, need to convert the Wakeup_Date to numbers
                    # and then sort by these numbers
                    df2['Wakeup_Date2'] = df2['Wakeup_Date'].apply(date_conv)
                    df2.sort_values(by=['Wakeup_Date2'], axis=0, inplace=True)
                    self.list_resp += self.df_to_list_resp(df2, df_name,title)
                    self.list_resp += '\n\n'
        return True

    def list_halted(self):
        if self.list_resp == 'clean':
            self.list_resp = 'Searching for PROJECT, TASK and ACTIVITY in OnHold state:\n\n'
        else:
            self.list_resp += '==========================\n'
            self.list_resp += '\nSearching for PROJECT, TASK and ACTIVITY in OnHold state:\n\n'
        for df_name in ['dfp', 'dft', 'dfa']:
            #self.list_resp += "\nResults from {}\n".format(defs.db_names[df_name])
            title = "Results from {}".format(defs.db_names[df_name])
            df = self.db_table[df_name]
            df1 = df[df['State'] == 'OnHold']
            if len(df1) == 0: # nothing found
                self.list_resp += 'well ... nothing found here at {}.\n'.\
                    format(defs.db_names[df_name])
            else:
                self.list_resp += self.df_to_list_resp(df1, df_name,title)
                self.list_resp += '\n\n'
        return True
   
    def delete_id(self):
        found = 0
        for df_name in ['dft', 'dfa']:
            df = self.db_table[df_name]
            if self.use_this_ID_for_ref in df.index :
                found = 1
                logger.debug("found the ID in index of {}".format(df_name))
                df.drop(self.use_this_ID_for_ref, inplace = True)
                return True
        if found == 0 : #meaning - we did not find the id to delete
            self.had_error('Did not find the ID to delete ({}) in Task or Activity database. Note that project and megaproject cannot be deleted!\n'\
                           .format(self.use_this_ID_for_ref))

        return False

    def help_message(self):
        pass
        return True


    def online_check(self):
        # example
        # '{:15} {:5} {:5} {:10}\n'.format('Megaproject','db', 'is', 'online')
        self.return_message_ext1 = '\nOnline Status:\n'
        self.return_message_ext1 += '==============\n'
        if self.dfm is not None:
            self.return_message_ext1 += '{:12} {:4} {:4} {:8} has {:4} records {}\n'.format('Megaproject', 'db', 'is', 'online', len(self.dfm), \
                {y: len(self.dfm[self.dfm['State'] == y]) for y in list(defs.megaproject_states.keys())}) # dctionary with number of each state in the database
        else:
            self.return_message_ext1 += '{:12} {:4} {:4} {:8}\n'.format('Megaproject', 'db', 'is', 'None')
        if self.dfp is not None:
            self.return_message_ext1 += '{:12} {:4} {:4} {:8} has {:4} records {}\n'.format('Project', 'db', 'is', 'online', len(self.dfp), \
                {y: len(self.dfp[self.dfp['State'] == y]) for y in list(defs.project_states.keys())}) # dctionary with number of each state in the database
        else:
            self.return_message_ext1 += '{:12} {:4} {:4} {:8}\n'.format('Project', 'db', 'is', 'None')
        if self.dft is not None:
            self.return_message_ext1 += '{:12} {:4} {:4} {:8} has {:4} records {}\n'.format('Task', 'db', 'is', 'online', len(self.dft), \
                {y: len(self.dft[self.dft['State'] == y]) for y in list(defs.task_states.keys())}) # dctionary with number of each state in the database
        else:
            self.return_message_ext1 += '{:12} {:4} {:4} {:8}\n'.format('Task', 'db', 'is', 'None')
        if self.dfa is not None:
            self.return_message_ext1 += '{:12} {:4} {:4} {:8} has {:4} records {}\n'.format('Activity', 'db', 'is', 'online', len(self.dfa), \
                {y: len(self.dfa[self.dfa['State'] == y]) for y in list(defs.activity_states.keys())}) # dctionary with number of each state in the database
        else:
            self.return_message_ext1 += '{:12} {:4} {:4} {:8}\n'.format('Activity', 'db', 'is', 'None')
        self.return_message_ext1 += 'Total number of items is {}\n'.format(len(self.dfm)+len(self.dfp)+len(self.dft)+len(self.dfa))
        cid = self.get_current_ID()
        lstr = "The ID in file is: {}\n".format(cid)
        self.return_message_ext1     += lstr
        self.return_message_ext1 += '==========================\n'
        # add if developement or production
        self.return_message_ext1 += 'Working environment is {}\n'\
                .format(defs.config['MAIN']['dev_or_prod'])
        # list of wake ups, and add into the return message
        self.return_message_ext1 += '==========================\n'
        self.list_wakeup()
        self.list_halted()
        self.return_message_ext1 += self.list_resp
        self.return_message_ext1 += '==========================\n'
        # timedelta status
        self.return_message_ext1 += 'Timedelta set to {} day(s) (back).\n'. \
            format(self.tdelta)
        self.return_message_ext1 += '==========================\n'
        return True

    def move_items(self):
        if self.transaction_type == 'move list':
            if len(self.items_list) > 0:
                for item in self.items_list:
                    if item in self.dfa.index:
                        self.dfa.loc[item, 'PROJECT'] = self.move_to
                    elif item in self.dft.index:
                        self.dft.loc[item, 'PROJECT'] = self.move_to
        elif self.transaction_type == 'move item':
            item = self.use_this_ID_for_ref
            if item in self.dfa.index:
                self.dfa.loc[item, 'PROJECT'] = self.move_to
            elif item in self.dft.index:
                self.dft.loc[item, 'PROJECT'] = self.move_to
        elif self.transaction_type == 'move task':
            if self.state_to_list == 'clean':
                self.dft.loc[self.dft['PROJECT'] == self.move_from,'PROJECT']\
                    = self.move_to
            else: # there is a specific state to move
                self.dft.loc[(self.dft['PROJECT'] == self.move_from) \
                             & (self.dft['State'] == self.state_to_list) \
                    , 'PROJECT'] = self.move_to
        elif self.transaction_type == 'move activity':
            # move_to_id = 1 
            self.dfa.loc[self.dfa['PROJECT'] == self.move_from,'PROJECT'] = self.move_to
            if self.state_to_list == 'clean':
                self.dfa.loc[self.dft['PROJECT'] == self.move_from, 'PROJECT'] \
                    = self.move_to
            else:  # there is a specific state to move
                self.dfa.loc[(self.dfa['PROJECT'] == self.move_from) \
                             & (self.dfa['State'] == self.state_to_list) \
                    , 'PROJECT'] = self.move_to
        return True

    def myprint(self, df,which_db,title):
        str1 = df.to_json()
        df1 = pd.read_json(str1)

        csv_str = df1.to_csv(sep='|',
                            columns=defs.columns_to_print_table[which_db],
                            na_rep='N/A')
                            # , float_format=conv, index_names=True, justify='left')
        l = []
        q = defs.columns_to_print_table[which_db][:]
        q.insert(0, 'ID')
        l.append(q)
        c = 0
        for line in csv_str.splitlines():
            if c == 0:
                c = c + 1
                continue
            sl = line.split('|')
            for i in range(0, len(sl)):
                if len(sl[i]) > defs.max_width:
                    sl[i] = '\n'.join(wrap(sl[i], defs.max_width))
            l.append(sl)
        table_instance = AsciiTable(l, title)
        table_instance.justify_columns[2] = 'right'
        print(table_instance.table)

    def create_list(self):
        # the list is already created during parsing, so
        # no need to do anything
        return True

    def set_param(self):
        if hasattr(defs, self.param_to_set):
            if (self.value_to_set.isdigit()):
                self.value_to_set = int(self.value_to_set)
            setattr(defs,self.param_to_set, self.value_to_set)
            # check if the param to set is the columns to print, and change teh defs
            if self.param_to_set == 'columns_print_style':
                defs.columns_to_print_table = defs.which_columns_to_print[self.value_to_set]
        else:
            return False
        return True

    def list_parameter(self):
        self.list_resp = "Program Parameters that can be set:\n"
        for par in defs.params_list:
            self.list_resp += "paramter: {} = {}\n"\
                .format(par, eval("defs." + par))
        return True

    def list_shortcut(self):
        defs.config.read(r'C:\mgtd.local\mgtd.local.cfg')
        self.list_resp = ''
        for sect in defs.config.sections():
            if 'replace_' in sect:
                (a1,a2,a3) = sect.partition("_")
                self.list_resp += "replacement shortcut number {}\n".format(a3)
                self.list_resp += "===================================\n"
                self.list_resp += "substitution type: {}\n".\
                    format(defs.config[sect]['replacement_type'])
                self.list_resp += "substitute this:   {}\n".\
                    format(defs.config[sect]['replace_what'])
                self.list_resp += "with this:         {}\n".\
                    format(defs.config[sect]['replace_with'])
                self.list_resp += "===================================\n\n"
        return True

    def create_shortcut(self):
        # find the number of the next repalcement
        max_replacement_num = 0
        for sect in defs.config.sections():
            if 'replace_' in sect:
                (a1,a2,a3) = sect.partition("_")
                if int(a3) >= max_replacement_num:
                    max_replacement_num = int(a3) +1
        # write to config file, assuming replacement is always 3 long !
        l = eval(self.trans_description)
        f = open(r'C:\mgtd.local\mgtd.local.cfg', 'a')
        f.write('\n')
        f.write('[replace_{}]\n'.format(max_replacement_num))
        f.write('replacement_type = {}\n'.format(l[0]))
        f.write('replace_what = {}\n'.format(l[1]))
        f.write('replace_with  = {}\n\n'.format(l[2]))
        f.close()
        # reread the config
        defs.config.read(r'C:\mgtd.local\mgtd.local.cfg')
        return True

    def delete_shortcut(self):
        section = 'replace_'+self.shortcut_to_delete
        res = defs.config.remove_section(section)
        if not res:
            self.had_error('Could not find the requested shortcut - number {}\n'\
                           .format(self.shortcut_to_delete))
            return False
        else:
            f = open(r'C:\mgtd.local\mgtd.local.cfg', 'w')
            defs.config.write(f)
            f.close()
        return True

    def tagging(self):
        # check tag is correctly formatted - "tTAG", otherwise return false
        b1 = self.tag[0].islower() # first (t) is lower case
        b2 = self.tag[0] == 't' # first letter is t
        b3 = self.tag[1:].isupper() # the rest is upper case
        if (b1 or b2 or b3): #this is true when tag is incorrectly formatted in at least one of th eissues
            return self.had_error('tag provided does not meet the formatting ctiteria tTAG\n')
        if self.transaction_type == 'tag something':
            # look for the item and set the tag
            found_in = 'nowhere'
            duplicate_tag = False
            ref_id = int(self.use_this_ID_for_ref)
            if ((self.dfp is not None) and\
                        (ref_id in list(self.dfp.index.values))):
                found_in = 'project'
                if self.tag not in self.dfp.loc[ref_id,'Tag']:
                    self.dfp.loc[ref_id,'Tag'].append(self.tag)
                else:
                    duplicate_tag = True
                item = self.dfp.loc[ref_id,'Name']
            elif ((self.dft is not None) and (ref_id in list(self.dft.index.values))):
                found_in = 'task'
                if self.tag not in self.dft.loc[ref_id,'Tag']:
                    self.dft.loc[ref_id,'Tag'].append(self.tag)
                else:
                    duplicate_tag = True
                item = ref_id
            elif ((self.dfa is not None) and (ref_id in list(self.dfa.index.values))):
                found_in = 'activity'
                if self.tag not in self.dfa.loc[ref_id,'Tag']:
                    self.dfa.loc[ref_id,'Tag'].append(self.tag)
                else:
                    duplicate_tag = True
                item = ref_id
            if duplicate_tag:
                self.return_message_ext1 = "\nTag {} was not added to {} {} since the item already has this tag\n". \
                    format(self.tag, found_in, item )
            else:
                self.return_message_ext1 = "\nTag {} was added to {} {}\n". \
                    format(self.tag, found_in, item )
        ###
        elif self.transaction_type == 'untag something':
            # look for the item and set the tag
            found_in = 'nowhere'
            ref_id = int(self.use_this_ID_for_ref)
            if ((self.dfp is not None) and \
                        (ref_id in list(self.dfp.index.values))):
                found_in = 'project'
                if self.tag == 'clean':
                    self.dfp.loc[ref_id, 'Tag'].clear()
                else:
                    if self.tag in self.dfp.loc[ref_id, 'Tag']: \
                            self.dfp.loc[ref_id, 'Tag'].remove(self.tag)
                item = self.dfp.loc[ref_id, 'Name']
            elif ((self.dft is not None) and (ref_id in list(self.dft.index.values))):
                found_in = 'task'
                if self.tag == 'clean':
                    self.dft.loc[ref_id, 'Tag'].clear()
                else:
                    if self.tag in self.dft.loc[ref_id, 'Tag']: \
                            self.dft.loc[ref_id, 'Tag'].remove(self.tag)
                item = ref_id
            elif ((self.dfa is not None) and (ref_id in list(self.dfa.index.values))):
                found_in = 'activity'
                if self.tag == 'clean':
                    self.dfa.loc[ref_id, 'Tag'].clear()
                else:
                    if self.tag in self.dfa.loc[ref_id, 'Tag']: \
                            self.dfa.loc[ref_id, 'Tag'].remove(self.tag)
                item = ref_id
            if self.tag == 'clean':
                self.return_message_ext1 = "\nAll tags were removed from {} {}\n". \
                    format(found_in, item)
            else:
                self.return_message_ext1 = "\nTag {} was removed from {} {}\n". \
                    format(self.tag, found_in, item)
        ###

        return True

    def tagging_project(self):
        # check tag is correctly formatted - "tTAG", otherwise return false
        b1 = self.tag[0].islower() # first (t) is lower case
        b2 = self.tag[0] == 't' # first letter is t
        b3 = self.tag[1:].isupper() # the rest is upper case
        if (b1 or b2 or b3): #this is true when tag is incorrectly formatted in at least one of th eissues
            return self.had_error('tag provided does not meet the formatting ctiteria tTAG\n')

        # find the project
        if ((self.dfp is not None) and \
                    (self.item_to_tag_or_untag in list(self.dfp.Name))):
            if len(self.dfp[self.dfp['Name'] == self.item_to_tag_or_untag]) > 1 :
                self.had_error('Multiple projects named with the specified name {}\n'.\
                               format(self.item_to_tag_or_untag))
                return False
            ref = int(self.dfp.index[self.dfp['Name'] == self.item_to_tag_or_untag].values)
        else:
            self.had_error('Could not find the specified project {}\n'.\
                           format(self.item_to_tag_or_untag))
            return False

        if self.transaction_type == 'tag project':
            if self.tag not in self.dfp.loc[ref, 'Tag']:
                self.dfp.loc[ref, 'Tag'].append(self.tag)
            else:
                self.return_message_ext1 = "\nTag {} was not added to project {} since the project already has this tag\n". \
                    format(self.tag, self.item_to_tag_or_untag )                
        elif self.transaction_type == 'untag project':
            if self.tag != 'clean':
                if self.tag in self.dfp.loc[ref,'Tag']:
                    self.dfp.loc[ref, 'Tag'].remove(self.tag)
                else:
                    self.had_error('Tag {} was not found for the specied project {}.\n'.\
                                   format(self.tag, self.item_to_tag_or_untag))
                    return False
            else: # tag is clean ==> remove all
                self.dfp.loc[ref,'Tag'].clear()

        return True

    def list_tag(self):
        # first check if tag is 'alltags' which is a special word (and illigal tag as does not follow tTAG format)
        if self.tag == 'alltags': # whcih means - just return all the tags that we have
            ll = []
            for i in self.db_table.keys(): # all the db names
                if i == 'dfm':
                    continue
                ll += [x for x in self.db_table[i]['Tag'] if x != []]
            s = set([x for xs in ll for x in xs])
            self.list_resp = f'The tags that exist in all teh database are: {s}\n'
        else: 
            if self.tag == 'clean':
                self.tag = 'any-tag-at-all'
                # search for the tag in project
                df_proj = self.dfp[self.dfp['Tag'].apply(if_list_and_not_empty) == True]
                # search for the tag in project
                df_task = self.dft[self.dft['Tag'].apply(if_list_and_not_empty) == True]
                # search for the tag in project
                df_act  = self.dfa[self.dfa['Tag'].apply(if_list_and_not_empty) == True]
            else: # listing for a certain tag
                # search for the tag in project
                df_proj = self.dfp[self.dfp['Tag'].apply(if_list_find_item, args=(self.tag,)) == True]
                # search for the tag in project
                df_task = self.dft[self.dft['Tag'].apply(if_list_find_item, args=(self.tag,)) == True]
                # search for the tag in project
                df_act  = self.dfa[self.dfa['Tag'].apply(if_list_find_item, args=(self.tag,)) == True]

            # remove clean from the list response
            self.list_resp = ""
            if len(df_proj) > 0:
                str1 = self.df_to_list_resp(df_proj, 'dfp', '*Projects with tag {}*'.\
                                            format(self.tag))
                self.list_resp += str1 # first, removing the 'clean'
                self.list_resp += '\n\n'
            if len(df_task) > 0:
                str2 = self.df_to_list_resp(df_task, 'dft', '*Tasks with tag {}*'.\
                                            format(self.tag))
                self.list_resp += str2
                self.list_resp += '\n\n'
            if len(df_act) > 0:
                str3 = self.df_to_list_resp(df_act, 'dfa', '*Activities with tag {}*'.\
                                            format(self.tag))
                self.list_resp += str3
                self.list_resp += '\n\n'

        if len(self.list_resp) == 0 :
            self.error_details = 'Nothing to list since no items with tag {} found'.\
                format(self.tag)
            logger.debug(self.error_details)
            return False

        return True

    def tag_list(self):
        if len(self.items_list) <= 0: #smaller then zero ??
            return False
        else:
            for item in self.items_list:
                if item in self.dfa.index: # activity
                    self.dfa.loc[item, 'Tag'].append(self.tag)
                elif item in self.dft.index: # task
                    self.dft.loc[item, 'Tag'].append(self.tag)
                elif item in self.dfp.index:  # project
                    self.dfp.loc[item, 'Tag'].append(self.tag)
            return True

    def list_list(self):
        if ((self.items_list[0] == 'clean') or (len(self.items_list) == 0))  :
            self.had_error('list of items is empty. Cannot list it.')
            return False
        else:
            self.list_resp = ""
            for item in self.items_list:
                which_db = self.find_in_which_db(item)
                if which_db == 'nowhere':
                    self.had_error('List is bogus for item {} [1]'.format(item))
                    return False
                df = self.db_table[which_db]
                df = df.loc[item]
                if len(df) > 0:
                    self.list_resp += self.df_to_list_resp\
                        (pd.DataFrame(df).T, which_db, ' From '+defs.db_names[which_db])
                    self.list_resp += '\n\n'
                else:
                    self.had_error('List is bogus for item {} [2]'.format(item))
                    return False

        return True

    def tdelta_func(self):
        self.return_message_ext1 = '\n'
        if self.tdelta_param == 'clean':
            self.had_error('No timedelta param.')
            return False
        elif self.tdelta_param == 'off':
            self.tdelta = timedelta(days=0)
            self.return_message_ext1 += 'Timedelta set to zero\n'
        elif self.tdelta_param == 'printout':
            self.return_message_ext1 += 'Timedelta is {} (backwards)\n'.\
                format(self.tdelta)
        else: #creating timedelta
            self.tdelta = timedelta(days=float(self.tdelta_param))
            self.return_message_ext1 += 'Timedelta set to {} days (backwards).\n'.\
                format(self.tdelta_param)
        return True

    def swap(self):
        #this function swaps the Description field in the two
        self.had_error("-swap- command is not suportted at this time")
        return False
    
    def add_comment(self):
        # find the ID where it is
        which_db = self.find_in_which_db(self.use_this_ID_for_ref)
        if self.db_table[which_db] is not None: # database exists
            s = "+++ " + datetime.now().strftime("%I:%M:%S%p on %B %d, %Y") + " +++\n" +\
                self.trans_description + "\n"
            self.db_table[which_db].loc[self.use_this_ID_for_ref,'Comments'].insert(0,s)
        return True

    def set_priority(self):
        # find the ID where it is
        which_db = self.find_in_which_db(self.use_this_ID_for_ref)
        if which_db in ['dfm', 'dfp']: #can set priority only to tasks and activities
            self.had_error("tried setting priority to a megaproject or a project ({}, {})".format(self.use_this_ID_for_ref, which_db))
            return False
        if self.db_table[which_db] is not None: # database exists
            self.db_table[which_db].loc[self.use_this_ID_for_ref,'Priority'] = self.priority_to_set
        return True

    def list_html(self):
        # top part
        s = datetime.now().strftime("%I:%M:%S%p on %B %d, %Y") + '  <br>'
        total = 0
        per_db_total = {}
        for i in ['dfm', 'dfp', 'dft', 'dfa']:
            per_db_total[i] = len(self.db_table[i])
            total += per_db_total[i]
        s += f'Total number of items in the database is {total}.<br>'
        ##
        if True: # implementing list html hierarchical
            # create a dataframe to store
            # estimate the number of items
            cols=['ID', 'Type1', 'Type2', 'Type3', 'Type4', 'Name', 'State', 'ParentId', 'ParentRec', 'Description']
            rowslist = []
            # iterate over all dbs - megaproject-project-task-activity and create a line for them pd.series
            # and place in the right order in the list
            cnt = 0
            if self.dfm is not None:
                if True: #place holder to add check on if to list all or not all. default is do not print ended/closed/off items
                    ldf = self.dfm[self.dfm['State'] != 'Off']                       
                for index, row in ldf.iterrows():
                    ll = [index, 'Megaproject', '', '', '', row['Name'], row['State'], '-', '-', row['Description']] 
                    d = pd.DataFrame(dict(zip(cols, ll)), index=[cnt])
                    cnt +=1
                    rowslist.append(d)
            # now insert the projects
            if self.dfp is not None:
                lcnt = 1 
                if True: #place holder to add check on if to list all or not all. default is do not print ended/closed/off items
                    ldf = self.dfp[self.dfp['State'] != 'Ended']                       
                for index, row in ldf.iterrows():
                    #print(index, row)
                    ll = [index, '', 'Project','','', row['Name'], row['State'], '-', '-', row['Description']] 
                    d = pd.DataFrame(dict(zip(cols, ll)), index=[cnt])
                    cnt += 1                        
                    lcnt = 1 
                    for i in rowslist:
                        if i['Name'].values[0] == row['MEGAPROJECT']: # found in location lcnt
                            break
                        lcnt += 1
                    rowslist.insert(lcnt,d)
            # next - insert the tasks
            if self.dft is not None:
                if True: #place holder to add check on if to list all or not all. default is do not print ended/closed/off items
                    ldf = self.dft[self.dft['State'] != 'Closed']                       
                for index, row in ldf.iterrows():
                    #print(index, row)
                    namesub = " ".join(row['Description'].split(" ")[:4]) # take first 4 words
                    #find the project id
                    project_id = self.dfp.loc[self.dfp['Name'] == row['PROJECT']].index[0] # find which project the task belongs to
                    ll = [index, '', '', 'Task', '', namesub, row['State'], '-', '-', row['Description']] 
                    d = pd.DataFrame(dict(zip(cols, ll)), index=[cnt])                        
                    cnt += 1
                    lcnt = 1 
                    for i in rowslist:
                        if i['ID'].values[0] == project_id: # found in location lcnt
                            break
                        lcnt += 1
                    rowslist.insert(lcnt,d)
            # last - insert the activities
            if self.dfa is not None:
                if True: #place holder to add check on if to list all or not all. default is do not print ended/closed/off items
                    ldf = self.dfa[self.dfa['State'] != 'Ended']                       
                for index, row in ldf.iterrows():
                    #print(index, row)
                    namesub = " ".join(row['Description'].split(" ")[:4]) # take first 4 words
                    #find the project or task id (assume one of them is avaialble, no third option)
                    if row['TASK'] != None and row['TASK'] != '': # this is a task activity
                        lid = int(row['TASK'])
                        parent_rec = 'Task'
                    else:
                        lid = int(row['PROJECT']) # else - it is a project activity
                        parent_rec = 'Project'
                    ll = [index, '', '', '','Activity', namesub, row['State'], lid, parent_rec, row['Description']] 
                    d = pd.DataFrame(dict(zip(cols, ll)), index=[cnt])
                    cnt += 1                        
                    lcnt = 1
                    for i in rowslist:
                        if i['ID'].values[0] == lid: # found in location lcnt
                            break
                        lcnt += 1
                    rowslist.insert(lcnt,d)
            # building final dataframe
            dd = pd.concat(rowslist)
            dd.reset_index(inplace=True) # reindexes 0 to len(dd)
            dd.drop('index', axis=1,inplace=True) # removes the old index (now a column named 'index')
            s1 = s
            s1 += dd.to_html(#formatters={'Comments': print_a_list}, 
                            justify='left')
            #coloring
            s11 = self.add_color_to_hierarchical_html(s1)
            file = open(defs.mgtd_local_path + r'/{}/list_html_{}_hier.html'.format(defs.dev_or_prod, defs.dev_or_prod),"w")
            file.write(s11)
            file.close()            
        # preparing collapsable
        if True:
            scolap = defs.head
            scolap += f'<body>\n<h3>\n{s}\n</h3>\n\n'
            start = 0
            last = 0
            mp_name = rowslist[start]['Name'].values[0]
            for i in range(1,len(rowslist)):
                # assume the first one is a megaproject, so starting from 1
                if rowslist[i]['Type1'].values[0] != 'Megaproject':
                    continue
                else:
                    last = i
                    scolap += f'<button type="button" class="collapsible">{mp_name} [{last-start-1}]</button>\n<div class="content">'
                    if start == last: #megaproject with no projects in it
                        dd = pd.DataFrame(rowslist[start])
                    else:
                        dd = pd.concat(rowslist[start:last])
                    dd.reset_index(inplace=True) # reindexes 0 to len(dd)
                    dd.drop('index', axis=1,inplace=True) # removes the old index (now a column named 'index')
                    sc = dd.to_html(#formatters={'Comments': print_a_list}, 
                            justify='left')
                    #coloring
                    sc1 = self.add_color_to_hierarchical_html(sc)
                    scolap += sc1
                    scolap += '</div>\n'
                    start = i
                    mp_name = rowslist[i]['Name'].values[0] # for the next megaproject
            # after the for loop, still need to add the last megaproject
            last = len(rowslist)
            scolap += f'<button type="button" class="collapsible">{mp_name} [{last-start-1}]</button>\n<div class="content">'
            dd = pd.concat(rowslist[start:last])
            dd.reset_index(inplace=True) # reindexes 0 to len(dd)
            dd.drop('index', axis=1,inplace=True) # removes the old index (now a column named 'index')
            sc = dd.to_html(#formatters={'Comments': print_a_list}, 
                    justify='left')
            #coloring
            sc1 = self.add_color_to_hierarchical_html(sc)
            scolap += sc1
            scolap += '</div>\n'
            start = i
                    
            scolap += defs.script
            scolap += '</body>'
            file = open(defs.mgtd_local_path + r'/{}/list_html_{}_hier_collaps.html'.format(defs.dev_or_prod, defs.dev_or_prod),"w")
            file.write(scolap)
            file.close()            
        

        #preparing regular full file# 
        if True:
            s2 = s
            for db in ['dfm', 'dfp', 'dft', 'dfa'] :
                s2 += '<br> {} with {} items <br>'.format(db, per_db_total[db])
                #s1 += '\n {} \n'.format(db)
                df = self.db_table[db]
                if df is None:
                    continue
                #df.to_html(r'C:/mgtd.local/{}/{}.html'.format(defs.dev_or_prod, db))
                s2 += df.to_html(#formatters={'Comments': print_a_list}, 
                            justify='left')
                #s1 += df.style.to_html(justipy='left')
                # fix comments pages
                s2l = s2.splitlines()
                for i in range(0,len(s2l)): # this is a line of comments --> so go and break it
                    if s2l[i].find('<td>[+++') > 0 :
                        #print(s2l[i])
                        s2l[i] = s2l[i].replace('\n]','<br>]')
                        s2l[i] = s2l[i].replace('+++\\n','+++<br>')
                        s2l[i] = s2l[i].replace('\\n, +++','<br>+++')
                        s2l[i] = s2l[i].replace('\&lt;br\&gt;','\<br> ')
                s2 = "\n".join(s2l)
            file = open(defs.mgtd_local_path + r'/{}/list_html_{}.html'.format(defs.dev_or_prod, defs.dev_or_prod),"w")
            file.write(s2)
            file.close()            

        return True



    def add_color_to_hierarchical_html(self, s):
        # colors:1
        # MEGAPROJECT #B31E00 #FF5500
        # PROJECT #4D9900 #8CFF19
        # TASK #B3B300 #FFFF33 
        # ACTIVITY #0066CC #66B3FF
        # states definitions (all transitions are legel)
        # OPEN:    On Started Open
        # CLOSED:  Off Ended
        # DORMANT: Dormant
        # HALTED:  OnHold 
        match_open = ['<td>On</td>', '<td>Started</td>', '<td>Open</td>']
        match_closed = ['<td>Off</td>', '<td>Ended</td>', '<td>Closed</td>']
        match_dormant = ['<td>Dormant</td>']
        match_halted = ['<td>OnHold</td>']
        scolors = {
            'OPEN'    : '#D5F5E3',
            'CLOSED'  : '#5D6D7E',
            'DORMANT' : '#76448A',
            'HALTED'  : '#A569BD'
        }
        hcolors = { 
            'MEGAPROJECT' : { 0 : '#B31E00', 1 : '#FF5500'} ,
            'PROJECT'     : { 0 : '#4D9900', 1 : '#8CFF19'} ,
            'TASK'        : { 0 : '#B3B300', 1 : '#FFFF33'} ,        
            'ACTIVITY'    : { 0 : '#0066CC', 1 : '#66B3FF'} 
        }
        Ms = 0 # megaproject state
        Ps = 0 # project state
        Ts = 0 # task state
        As = 0 # activity state
        ls = s.splitlines()
        last_type = 'None'
        block = 0
        for l in range(0,len(ls)):
            # add color to the state column
            if any(x in ls[l] for x in match_open):
                ls[l] = ls[l].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(scolors['OPEN']))
            if any(x in ls[l] for x in match_closed):
                ls[l] = ls[l].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(scolors['CLOSED']))
            if any(x in ls[l] for x in match_dormant):
                ls[l] = ls[l].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(scolors['DORMANT']))
            if any(x in ls[l] for x in match_halted):
                ls[l] = ls[l].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(scolors['HALTED']))
            # take care of coloring megaproject/project/task/activity
            if block > 0 : #we want to skip this line - to not miscolor something
                block -= 1
                continue
            if (ls[l].find('<td>Megaproject</td>')) > -1 : # found megaproject
                Ms = (Ms+1)%2 # flip color selector
                last_type = 'MEGAPROJECT'
                ls[l] = ls[l].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['MEGAPROJECT'][Ms]))
                ls[l+1] = ls[l+1].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['MEGAPROJECT'][Ms]))
                ls[l+2] = ls[l+2].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['MEGAPROJECT'][Ms]))
                ls[l+3] = ls[l+3].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['MEGAPROJECT'][Ms]))
                ls[l+4] = ls[l+4].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['MEGAPROJECT'][Ms]))
            if (ls[l].find('<td>Project</td>')) > -1 : # found project
                Ps = (Ps+1)%2 # flip color selector
                last_type = 'PROJECT'
                ls[l] = ls[l].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['PROJECT'][Ps]))
                ls[l-1] = ls[l-1].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['MEGAPROJECT'][Ms]))
                ls[l+1] = ls[l+1].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['PROJECT'][Ps]))
                ls[l+2] = ls[l+2].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['PROJECT'][Ps]))
                ls[l+3] = ls[l+3].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['PROJECT'][Ps]))
            if (ls[l].find('<td>Task</td>')) > -1 : # found task
                Ts = (Ts+1)%2 # flip color selector
                last_type = 'TASK'
                ls[l] = ls[l].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['TASK'][Ts]))
                ls[l+1] = ls[l+1].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['TASK'][Ts]))
                ls[l-1] = ls[l-1].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['PROJECT'][Ps]))
                ls[l-2] = ls[l-2].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['MEGAPROJECT'][Ms]))
            if (ls[l].find('<td>Activity</td>')) > -1 : # found activity
                As = (As+1)%2 # flip color selector
                block = 4 # do not process next 4 lines
                if last_type == 'TASK' or last_type == 'ACTIVITY-TASK':
                    ls[l] = ls[l].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['ACTIVITY'][As]))
                    ls[l-1] = ls[l-1].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['TASK'][Ts]))
                    ls[l-2] = ls[l-2].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['PROJECT'][Ps]))
                    ls[l-3] = ls[l-3].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['MEGAPROJECT'][Ms]))
                    last_type = 'ACTIVITY-TASK'
                else:
                    ls[l] = ls[l].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['ACTIVITY'][As]))
                    ls[l-1] = ls[l-1].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['PROJECT'][Ps]))
                    ls[l-2] = ls[l-2].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['PROJECT'][Ps]))
                    ls[l-3] = ls[l-3].replace('<td>','<td ' + 'bgcolor="{}"\>'.format(hcolors['MEGAPROJECT'][Ms]))
                    last_type = 'ACTIVITY-PROJECT'

        s = "\n".join(ls)
        return s
    
    def edit_item_field(self):
        # find where the id is
        which_db = self.find_in_which_db(self.use_this_ID_for_ref)
        if which_db == 'nowhere': #item not founf
            return self.had_error('ID supplied is not found\n')
        # check that the column name is really editable
        if (which_db in ['dfm'] and self.edit_column_name not in defs.dfm_editable_columns) or \
            (which_db in ['dfp', 'dft', 'dfa'] and self.edit_column_name not in defs.dfp_dft_dfa_editable_columns): # column name does not fit
            return self.had_error('column name supplied does not match the record type editable columns for the ID given')
        old_val = self.db_table[which_db].loc[self.use_this_ID_for_ref, self.edit_column_name]
        self.db_table[which_db].loc[self.use_this_ID_for_ref, self.edit_column_name]= self.trans_description # replace the value
        self.success_response = 'replaced column {} from {} to the supplied new value'.format(self.edit_column_name, old_val)
        return True

    def import_file(self):
        print('in import. not implemented\n')


