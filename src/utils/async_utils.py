import threading


def async_start_job(target, args):
    print(f"async_count_lang_percentage_and_save_to_file -> start. Target: {target}. "
          f"Args: {args}")

    print("Before calling thread")
    t = threading.Thread(target=target, args=args, kwargs={})
    t.start()
    print("After calling thread")
