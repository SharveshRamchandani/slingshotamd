from app.services.ingestion import BaseConnector

class GmailConnector(BaseConnector):
    def __init__(self, credentials):
        self.credentials = credentials
    
    async def fetch_data(self, user_id: int):
        # Implementation to call Gmail API
        # Return list of emails that look like tasks/announcements
        return []
