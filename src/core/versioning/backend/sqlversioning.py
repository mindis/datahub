from config import settings
import psycopg2
import logging
import string
import random

log = logging.getLogger('dh')
log.setLevel(logging.INFO)



CREATE_VERSION_SQL = "insert into versions (name, repo, user_id) values (%s,%s,%s) RETURNING v_id"
CREATE_VERSION_PARENT = "insert into version_parent (child_id, parent_id) values (%s,%s)"
CREATE_VERSIONED_TABLE = "insert into versioned_table (real_name, display_name, v_id) values (%s,%s,%s)"
FREEZE_TABLES = "update versioned_table set copy_on_write = true where v_id = %s"


class SQLVersioning:
  
  def __init__(self):
    self.connection = psycopg2.connect(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT'],
        database=settings.DATABASES['default']['NAME'])

    
    
  def create_version(self, user, repo, v_name, parent_v_id):
    cur = self.connection.cursor()
    id = None
    try:
      cur.execute(CREATE_VERSION_SQL,(v_name,repo,user))
      r = True
      id = cur.fetchone()[0]
      log.info("Id %s" % id)
    except Exception, e:
      r = False
      log.error(e)
    if r and parent_v_id:
      try:
        cur.execute(CREATE_VERSION_PARENT,(id, parent_v_id))        
      except Exception, e:
        r = False
        log.error(e)      
    if r:
      self.connection.commit()
    cur.close()
    return id
  
  def get_v_id(self,repo,v_name):
    raise Exception("TODO get_v_id")
  
  def find_active_table(self, version, display_table_name):
    raise Exception("TODO find_active_table")
  
  def get_list_tables(self, v_id):
    log.error("TODO get_list_tables")
    return []
                      
  def gen_string(self,base='', n=6):
    return "%s_%s" % (base,''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n)))

  
  def add_table(self, repo, user, v_id, table_name, create_sql):
    cur = self.connection.cursor()
    try:
      rn = self.gen_string(table_name)
      cur.execute(CREATE_VERSIONED_TABLE,(rn, table_name, v_id))
      log.info("todo add deleted and create")
      self.connection.commit()
    except Exception, e:
      rn = None
      log.error(e)      
    cur.close()
    return rn
  
  
  def build_table_query(self, table_tail):
    raise Exception("TODO")
  
  def get_rs(self,sql):
    raise Exception("TODO")
  

    
  
  def freeze_tables(self, v_id):
    cur = self.connection.cursor()
    try:
      cur.execute(FREEZE_TABLES,(v_id,))
      self.connection.commit()
    except Exception, e:
      log.error(e)      
    cur.close()

  def clone_table(self,table_real_name, new_name=None):
    #Create table name
    #CREATE TABLE [x] as 'qry' with no data
    #return table_real_name
    raise Exception("TODO")
    
  def get_query_trace(self, v_id1, v_id2):
    raise Exception("TODO")
  
  def update_user_head(self, user, repo, v_id, v_name):
    raise Exception("TODO")
  

  
  def commit(self, query_list, v_id):
    #update query log
    #insert into active table of v
    raise Exception("TODO")