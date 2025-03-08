from typing import Any
from info import *
from motor import motor_asyncio
client: motor_asyncio.AsyncIOMotorClient[Any] = motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client["biisal"]


class User:
    def __init__(self):
        """
        Initialize the User class.

        This class stores and retrieves user data from the database. The
        `users` attribute is a MotorCollection instance, which is the
        interface to the MongoDB collection. The `cache` attribute is a
        dictionary that stores user data in memory. This cache is updated
        whenever the user data is retrieved from the database.

        The cache is used to speed up the process of retrieving user data.
        """
        self.users = db["users"]
        self.cache : dict[int, dict[str, Any]] = {}

    async def addUser(self, user_id: int, name: str) -> dict[str, Any] | None:
        """
        Add a user to the database.

        Args:
            user_id (int): The unique identifier for the user.
            name (str): The name of the user.

        Returns:
            dict[str, Any] | None: A dictionary representing the user if added successfully, otherwise None.
        """
        try:
            user: dict[str, Any] = {"user_id": user_id, "name": name}
            await self.users.insert_one(user)
            self.cache[user_id] = user      
            return user
        except Exception as e:
            print("Error in addUser: ", e)
            

    async def get_user(self, user_id: int) -> dict[str, Any] | None:
        """
        Retrieves a user from the database.

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            dict[str, Any] | None: A dictionary representing the user if found, otherwise None.
        """
        try:
            if user_id in self.cache:
                return self.cache[user_id]
            user = await self.users.find_one({"user_id": user_id})
            return user
        except Exception as e:
            print("Error in getUser: ", e)
            return None

    async def remove_user(self, user_id: int) -> bool:
        
        """
        Removes a user from the database.

        Args:
            user_id (int): The unique identifier for the user.

        Returns:
            bool: True if the user was removed successfully, False otherwise.
        """
        try:
            await self.users.delete_one({"user_id": user_id})
            del self.cache[user_id]
            return True
        except Exception as e:
            print("Error in removeUser: ", e)
            return False
    async def get_or_add_user(self, user_id: int, name: str) -> dict[str ,str] | None:
        """
        Retrieves a user from the database or adds the user if they do not exist.
        
        Args:
            user_id (int): The unique identifier for the user.
            name (str): The name of the user.
            
        Returns:
            dict[str, str] | None: A dictionary representing the user if found or added successfully, otherwise None.
        """
        user : dict[str ,str] | None = await self.get_user(user_id)
        if user is None :
            user = await self.addUser(user_id, name)
        return user
    
    async def get_all_users(self) -> list[dict[str, Any]]:
        """
        Retrieves a list of all users stored in the database.

        Returns:
            list[dict[str, Any]]: A list of dictionaries representing all users in the database.
        """
        try:
            users : list[dict[str, Any]] = []
            async for user in self.users.find():
                users.append(user)
            return users
        except Exception as e:
            print("Error in getAllUsers: ", e)
            return []


class ChatHistory:
    def __init__(self):
        self.history  = db["history"]

    async def add_history(self, user_id: int, history: list[dict[str, str]]) -> bool:
        """
        Add a user's chat history to the database.

        Args:
            user_id (int): The Telegram User ID.
            history (list[dict[str, str]]): A list of dictionaries with 'role' and 'content' keys
                representing the conversation history.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            recent_history = history[-50:] # increesing this will create a api error
            query = {"user_id": user_id}
            update = {"$set": {"history": recent_history}}
            await self.history.update_one(query, update, upsert=True)
            return True
        except Exception as e:
            print("Error in addHistory: ", e)
            return False


    async def get_history(self, user_id: int) -> list[dict[str, str]]:        
        """
        Retrieve the chat history for a specific user.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            list[dict[str, str]]: A list of dictionaries representing the user's chat history. 
            Each dictionary contains 'role' and 'content' keys. Returns an empty list if no history is found or an error occurs.
        """

        try:
            history : dict[str , Any] | None = await self.history.find_one({"user_id": user_id})
            return history["history"] if history else []
        except Exception as e:
            print("Error in getHistory: ", e)
            return []
    
    async def reset_history(self, user_id: int) -> bool:
        """
        Deletes all chat history of a user.

        Args:
            user_id (int): The Telegram User ID.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            await self.history.delete_one({"user_id": user_id})
            return True
        except Exception as e:
            print("Error in clearHistory: ", e)
            return False


chat_history = ChatHistory()
users = User()
