import time
import random
import threading
import queue

class Task:
    def __init__(self, task_id, complexity):
        self.task_id = task_id
        self.complexity = complexity

class Worker(threading.Thread):
    def __init__(self, worker_id, task_queue):
        threading.Thread.__init__(self)
        self.worker_id = worker_id
        self.task_queue = task_queue
        self.is_running = True

    def run(self):
        while self.is_running:
            try:
                task = self.task_queue.get(timeout=1)  # Wait for a task
                print(f"Worker {self.worker_id} processing task {task.task_id} with complexity {task.complexity}")
                time.sleep(task.complexity)  # Simulates task processing
                self.task_queue.task_done()
            except queue.Empty:
                continue

    def stop(self):
        self.is_running = False

class Coordinator:
    def __init__(self, num_workers):
        self.task_queue = queue.Queue()
        self.workers = [Worker(i, self.task_queue) for i in range(num_workers)]
        for worker in self.workers:
            worker.start()

    def assign_tasks(self, tasks):
        for task in tasks:
            print(f"Coordinator assigning task {task.task_id} with complexity {task.complexity}")
            self.task_queue.put(task)

    def wait_for_completion(self):
        self.task_queue.join()
        print("All tasks have been processed.")

    def stop_workers(self):
        for worker in self.workers:
            worker.stop()
        for worker in self.workers:
            worker.join()

def create_tasks(num_tasks):
    tasks = []
    for i in range(num_tasks):
        complexity = random.randint(1, 5)  # Random complexity between 1 and 5
        tasks.append(Task(i, complexity))
    return tasks

def main():
    num_workers = 5
    num_tasks = 20

    print("Creating tasks...")
    tasks = create_tasks(num_tasks)

    print("Starting coordinator and workers...")
    coordinator = Coordinator(num_workers)

    print("Assigning tasks to workers...")
    coordinator.assign_tasks(tasks)

    print("Waiting for all tasks to complete...")
    coordinator.wait_for_completion()

    print("Stopping workers...")
    coordinator.stop_workers()
    print("Distributed system simulation complete.")

if __name__ == "__main__":
    main()
