from concurrent.futures import ThreadPoolExecutor

# Create a ThreadPoolExecutor with 4 worker threads
executor = ThreadPoolExecutor(max_workers=4)
# from concurrent.futures import ThreadPoolExecutor

# class CustomThreadPoolExecutor(ThreadPoolExecutor):
#     def get_queue(self):
#         with self._work_queue.queue.mutex:
#             return list(self._work_queue.queue)


# executor = CustomThreadPoolExecutor(max_workers=4)

     
