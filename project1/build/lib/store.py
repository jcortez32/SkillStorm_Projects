#where we handle business logic! We do not want business logic in our endpoints.
from pydantic import TypeAdapter
from sqlalchemy import select, text

#companies consist of symbol, name, sector and press_release_id 

""" returns all companies """
def list_companies():
    # stmt creates the sql query
    stmt = select(TicketRecord).order_by(TicketRecord.id)