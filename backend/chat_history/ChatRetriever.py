from flask import Flask, jsonify

from mongodb.ChatStore import ChatStore


class ChatRetriever:
  
    def __init__(
        self, collection: ChatStore.Collection
    ) -> None:
        self.__collection = collection

    def register_routes(self, app: Flask) -> None:
        @app.route('/chathistory', methods=['GET'])
        def get_chat_history():
            try:
                chats_cursor = self.__collection.get_all_documents()

                chats = list(chats_cursor)
                chats = sorted(chats, key=lambda x: x['key'])
                responses =[]
                for chat in chats:
                    responses.append({
                        "content" : chat["question"],
                        "isUser" : True
                    })
                    responses.append({
                        "content" : chat["response"],
                        "isUser": False
                    })

                # Extract key for each document
                
                return jsonify({"history": responses}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            
