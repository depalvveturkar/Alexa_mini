from config import DEBUG_MODE

class ConversationManager:
    def __init__(self):
        """Initialize conversation state"""
        self.reset_state()
    
    def reset_state(self):
        """Reset conversation state"""
        self.state = {
            "awaiting_response": False,
            "context": None,
            "data": {}
        }
        if DEBUG_MODE:
            print("🔄 Conversation state reset")
    
    def set_state(self, context, data=None):
        """Set conversation state"""
        self.state = {
            "awaiting_response": True,
            "context": context,
            "data": data or {}
        }
        if DEBUG_MODE:
            print(f"💬 Awaiting response for: {context}")
    
    def get_state(self):
        """Get current state"""
        return self.state
    
    def is_awaiting_response(self):
        """Check if waiting for user response"""
        return self.state["awaiting_response"]
    
    def get_context(self):
        """Get current context"""
        return self.state["context"]
    
    def get_data(self, key=None):
        """Get data from state"""
        if key:
            return self.state["data"].get(key)
        return self.state["data"]