from ..extensions import db
import datetime

class HotdealModel(db.Model):

    serialize_rules = ["scrape_at"]
    _now = datetime.datetime.now()

    id = db.Column(db.VARCHAR(30), primary_key=True)
    title = db.Column(db.TEXT)
    first_price = db.Column(db.DOUBLE)
    last_price = db.Column(db.DOUBLE)
    currency_type = db.Column(db.VARCHAR(30))
    store_link = db.Column(db.TEXT)
    source_link = db.Column(db.TEXT)
    scrape_at = db.Column(db.DATETIME, default=_now)
    is_done = db.Column(db.BOOLEAN)
    is_blind = db.Column(db.BOOLEAN)