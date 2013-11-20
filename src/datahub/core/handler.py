import hashlib

from core.db import manager
from core.db.connection import *

from datahub import DataHub
from datahub.constants import *

'''
@author: anant bhardwaj
@date: Oct 9, 2013

DataHub Handler
'''

def construct_query_result(res):
  table = DHTable(rows=[
      DHRow(
          cells=[DHCell(value=bytes(val)) for val in t]
      ) for t in res['tuples']
  ])

  schema = DHSchema(fields=[
      DHField(
          name=res['column_names'][i],
          type=DHType.Binary
      ) for i in range(0, len(res['column_names']))
  ])

  query_result = DHQueryResult(
      status=res['status'],
      row_count=res['row_count'],
      data=DHData(
          table=table, schema=schema
      )
  )

  return query_result


class DataHubHandler:
  def __init__(self):
    self.sessions={}
    pass

  def get_version(self):
    return VERSION

  def connect(self, dh_con_params):  
    try:
      con = Connection(
          user=dh_con_params.user,
          password=hashlib.sha1(dh_con_params.password).hexdigest(),
          db_name=dh_con_params.user)

      dh_con = DHConnection(user=dh_con_params.user)
      return dh_con
    except Exception, e:
      raise DHException(message=str(e))
  
  def create_repo(self, dh_con, repo):
    try:
      res = manager.create_repo(username=dh_con.user, repo=repo)
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))

  def list_repos(self, dh_con):
    try:
      res = manager.list_repos(username=dh_con.user)
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))

  def delete_repo(self, dh_con, repo):
    try:
      res = manager.delete_repo(username=dh_con.user, repo=repo)
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))

  def list_tables(self, dh_con, repo):
    try:
      res = manager.list_tables(username=dh_con.user, repo=repo)
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))

  def desc_table(self, dh_con, table):
    try:
      res = manager.desc_table(username=dh_con.user, table=table)
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))

  def execute_sql(self, dh_con, query, query_params=None):
    try:
      res = manager.execute_sql(
          username=dh_con.user, query=query, params=query_params)
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))

  def load(self, dh_con, url):
    try:
      query = 'SELECT * from %s' % (url)
      res = manager.execute_sql(username=dh_con.user, query=query)
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))