import threading
import random
import time
from queue import Queue


class Table:

    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(threading.Thread):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        time.sleep(random.randint(3, 10))


class Cafe:

    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        for guest in guests:
            free_table = next(
                (table for table in self.tables if table.guest is None), None)
            if free_table:
                free_table.guest = guest
                guest.start()
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
            else:
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None
                                            for table in self.tables):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None

            if not self.queue.empty() and any(table.guest is None
                                              for table in self.tables):
                free_table = next(table for table in self.tables
                                  if table.guest is None)
                guest = self.queue.get()
                free_table.guest = guest
                guest.start()
                print(
                    f"{guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {free_table.number}"
                )


tables = [Table(number) for number in range(1, 6)]

guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman', 'Vitoria',
    'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]


guests = [Guest(name) for name in guests_names]

cafe = Cafe(*tables)

cafe.guest_arrival(*guests)

cafe.discuss_guests()







# from queue import Queue
# import time
# import threading
#
# def getter(queue):
#     while True:
#         time.sleep(5)
#         item = queue.get()
#         print(threading.current_thread(), 'взял элемент', item)
#
#
# q = Queue(maxsize=10)
# thread1 = threading.Thread(target=getter, args=(q,), daemon=True)
# thread1.start()
#
# for i in range(10):
#     time.sleep(2)
#     q.put(i)
#     print(threading.current_thread(), 'положил в очередь элемент', i)
#


# from threading import Thread, Event
# import time
#
#
# def first_worker():
#     print('Первый рабочий приступил к своей задаче')
#     event.wait()
#     print('Первый рабочий продолжил выполнять задачу')
#     time.sleep(5)
#     print('Первый рабочий закончил выполнять задачу')
#
#
#
# def second_worker():
#     print('Второй рабочий приступил к своей задаче')
#     time.sleep(10)
#     print('Второй рабочий закончил выполнять задачу')
#     event.set()
#
#
# event = Event()
# event.set()
# event.clear()
# print(event.is_set())
# thread1 = Thread(target=first_worker)
# thread2 = Thread(target=second_worker)
# thread1.start()
# thread2.start()