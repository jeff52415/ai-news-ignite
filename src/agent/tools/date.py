import datetime
from langchain_core.tools import tool

@tool(name_or_callable="get_current_date",)
def get_current_date():
  """
  This tool is used to get the current date in YYYY-MM-DD format.
  Don't require any input.
  Returns the current date in YYYY-MM-DD format.
  """
  return datetime.date.today().strftime("%Y-%m-%d")