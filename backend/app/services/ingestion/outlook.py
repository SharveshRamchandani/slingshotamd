from app.services.ingestion import BaseConnector

class OutlookConnector(BaseConnector):
    def __init__(self, credentials):
        self.credentials = credentials
        
    async def fetch_data(self, user_id: int):
        # Implementation to call Outlook Graph API
        return []
