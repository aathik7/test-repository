from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float,
        required=True,
        help="this field cannot be blank!"
        )
    parser.add_argument('store_id', 
        type=int,
        required=True,
        help="store id field cannot be blank!"
        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found!'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message':"Item already exists '{}'".format(name)}, 400
        
        data = Item.parser.parse_args()
        
        item = ItemModel(name, **data)  #data['price'], data['store_id']
        
        try:
            item.save_to_db()  #in above line it item is the model object
        except:
            return {"message":"An error occured while inserting"}, 500

        return item.json(), 201
    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'message':'Item Deleted'}

   #@jwt_required
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}