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
        backfill_surveys: bool = False,
        db_path: str = "m_bird.db"
    ):
        return await trigger_sync_tool(
            full_sync=full_sync,
            sync_messages=sync_messages,
            messages_days=messages_days,
            lookback_minutes=lookback_minutes,
            year=year,
            month=month,
            backfill_surveys=backfill_surveys,
            db_path=db_path,
        )
