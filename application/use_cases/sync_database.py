from infrastructure.api.sync import trigger_sync_tool

class SyncDatabaseUseCase:
    async def execute(
        self, 
        full_sync: bool = False, 
        sync_messages: bool = False, 
        messages_days: int = None, 
        lookback_minutes: int = 60,
        year: int = None,
        month: int = None,
        db_path: str = "m_bird.db"
    ):
        # We need to monkeypatch the get_db_path logic or pass the db_path to trigger_sync_tool
        # For now, let's assume the sync module will connect to the right DB.
        # Ideally, we should adapt `sync.py` to accept the `db_path` parameter, but let's see.
        return await trigger_sync_tool(
            full_sync=full_sync,
            sync_messages=sync_messages,
            messages_days=messages_days,
            lookback_minutes=lookback_minutes,
            year=year,
            month=month
        )
