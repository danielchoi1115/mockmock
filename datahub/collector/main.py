import logging
import subtasks


if __name__ == "__main__":

    logging.basicConfig(
        filename='error.log',
        encoding='utf-8',
        level=logging.WARNING,
        format='%(asctime)s:%(levelname)s:%(pathname)s:%(funcName)s:%(lineno)d:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    # subtasks.run_edgar()
    # subtasks.run_all(fake_run=True)
    # subtasks.run_naver(fake_run=True)
    
    
