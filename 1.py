import time
seconds = int(input("Введіть кількість секунд: "))
print("Таймер запущено!")

for i in range(seconds, 0, -1):
    print(i)
    time.sleep(1)

print("Час вийшов!")