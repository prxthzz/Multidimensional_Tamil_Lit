import time
import uuid
import threading
from typing import Dict, List, Any, Callable, Optional

class BackgroundJobQueue:
    """Production Job Manager for long-running asynchronous operations."""
    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()

    def submit_job(self, name: str, target_fn: Callable, *args, **kwargs) -> str:
        job_id = f"JOB-{uuid.uuid4().hex[:8].upper()}"
        with self.lock:
            self.jobs[job_id] = {
                "id": job_id,
                "name": name,
                "status": "QUEUED",
                "progress": 0,
                "result": None,
                "error": None,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "completed_at": None,
            }

        def worker():
            with self.lock:
                self.jobs[job_id]["status"] = "RUNNING"
                self.jobs[job_id]["progress"] = 10
            try:
                res = target_fn(*args, **kwargs)
                with self.lock:
                    self.jobs[job_id]["status"] = "COMPLETED"
                    self.jobs[job_id]["progress"] = 100
                    self.jobs[job_id]["result"] = res
                    self.jobs[job_id]["completed_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            except Exception as e:
                with self.lock:
                    self.jobs[job_id]["status"] = "FAILED"
                    self.jobs[job_id]["error"] = str(e)
                    self.jobs[job_id]["completed_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        return job_id

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            return self.jobs.get(job_id)

    def list_jobs(self) -> List[Dict[str, Any]]:
        with self.lock:
            return list(self.jobs.values())

job_queue_instance = BackgroundJobQueue()
