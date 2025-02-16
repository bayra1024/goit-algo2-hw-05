import json
import timeit
from datasketch import HyperLogLog

# Ініціалізація HyperLogLog
hll = HyperLogLog(p=14)
d_set = set()

set_count = 0
hll_count = 0


def calc_with_set(jdata):
    for line in jdata:
        try:
            jline = json.loads(line)

            addr = jline["remote_addr"]
            d_set.add(addr)
        except:
            print(f"Incorrect line: '{jline}'")


def calc_with_hll(jdata):
    for line in jdata:
        try:
            jline = json.loads(line)

            addr = jline["remote_addr"]
            hll.update(addr.encode("utf-8"))
        except:
            print(f"Incorrect line: '{jline}'")


with open("lms-stage-access.log", "r") as file:
    jdata = file.readlines()

hll_time = timeit.timeit(
    "calc_with_hll(jdata)",
    setup="from __main__ import calc_with_hll , jdata",
    number=1,
)

# calc_with_hll(jdata)
set_time = timeit.timeit(
    "calc_with_set(jdata)",
    setup="from __main__ import calc_with_set , jdata",
    number=1,
)


# Оцінка кількості унікальних елементів
print(
    "Результати порівняння:\n"
    + "                       Точний підрахунок        HyperLogLog\n"
    + f"Унікальні елементи              {len(d_set)}          {hll.count()}\n"
    + f"Час виконання (сек.)   {set_time}  {hll_time}"
)
# print(f"Оцінена кількість унікальних елементів hll: {hll.count()}")

# print(f"Оцінена кількість унікальних елементів set: {len(d_set)}")
