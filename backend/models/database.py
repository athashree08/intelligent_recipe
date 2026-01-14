from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB Connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/intelligent_recipe')
client = MongoClient(MONGO_URI)
db = client['intelligent_recipe']

# Collections
users_collection = db['users']
recipes_collection = db['recipes']
user_preferences_collection = db['user_preferences']

# Create indexes for better query performance
users_collection.create_index('username', unique=True)
users_collection.create_index('email', unique=True)
recipes_collection.create_index('name')
recipes_collection.create_index('cuisine')
recipes_collection.create_index('dietary_type')

def get_db():
    """Get database instance"""
    return db

def get_collection(name):
    """Get a specific collection"""
    return db[name]

# Helper functions for CRUD operations
class RecipeDB:
    @staticmethod
    def create_recipe(recipe_data):
        """Insert a new recipe"""
        result = recipes_collection.insert_one(recipe_data)
        return result.inserted_id
    
    @staticmethod
    def get_recipe_by_id(recipe_id):
        """Get recipe by ID"""
        from bson import ObjectId
        return recipes_collection.find_one({'_id': ObjectId(recipe_id)})
    
    @staticmethod
    def search_recipes(filters=None):
        """Search recipes with optional filters"""
        query = {}
        if filters:
            if filters.get('cuisine'):
                query['cuisine'] = filters['cuisine']
            if filters.get('dietary_type'):
                query['dietary_type'] = filters['dietary_type']
            if filters.get('max_cooking_time'):
                query['cooking_time'] = {'$lte': int(filters['max_cooking_time'])}
        
        return list(recipes_collection.find(query))
    
    @staticmethod
    def get_all_recipes():
        """Get all recipes"""
        return list(recipes_collection.find())

class UserDB:
    @staticmethod
    def create_user(user_data):
        """Insert a new user"""
        result = users_collection.insert_one(user_data)
        return result.inserted_id
    
    @staticmethod
    def get_user_by_username(username):
        """Get user by username"""
        return users_collection.find_one({'username': username})
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        from bson import ObjectId
        return users_collection.find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def update_user(user_id, update_data):
        """Update user data"""
        from bson import ObjectId
        return users_collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
