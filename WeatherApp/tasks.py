from celery import shared_task

@shared_task
def sum_numbers(a, b):
    result = a + b
    print(f'The sum of {a} and {b} is {result}')
    return result