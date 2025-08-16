from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from zoneinfo import ZoneInfo
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from os import getenv

jobstores = {
    "mongo": MongoDBJobStore(
        host=getenv('MDB_URI_STRING')
    ),
    "default": SQLAlchemyJobStore(url="sqlite:///jobs.sqlite"),
}

executors = {
    "default": ThreadPoolExecutor(20),
    "processpool": ProcessPoolExecutor(5),
}

job_defaults = {
    "coalesce": False,
    "max_instances": 3,
}

scheduler = BackgroundScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone=ZoneInfo("UTC"),
)

if __name__ == '__main__':
    from datetime import datetime, timedelta
    import time
    def my_job(text):
        print(f"[JOB] {text} @ {time.strftime('%X')}")
    run_time = datetime.now(ZoneInfo("UTC")) + timedelta(seconds=5)
    scheduler.add_job(my_job, trigger="date", run_date=run_time, args=['Test job'],id="one_minute_job")
    # scheduler.start()
    time.sleep(5)
