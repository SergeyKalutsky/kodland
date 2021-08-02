from kodland_db import db

cart_data = db.cart.get_all()
order_data = db.orders.get_all()

id_ = order_data[-1].id + 1 if order_data else 1
for row in cart_data:
    item = {'id': id_, 'item_id': row.item_id, 'amount': row.amount}
    db.orders.put(item)

for row in cart_data:
    db.cart.delete('item_id', row.item_id)