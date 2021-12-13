class MergeDataset:
    """Проверяет строки из in_file. Если строки нет в source_file, то добавляет.
    Записывает всё в файл out_file"""
    def __init__(self):
        self.in_file = "in.dat"
        self.source_file = "source.dat"
        self.out_file = "out.dat"
        self.new_count = 0

    def run(self):
        in_data = []
        f = open(self.in_file, "r", encoding="UTF-8")
        while True:
            line = f.readline()
            in_data.append(line)
            if not line:
                break
        f.close()

        source_data = []
        f = open(self.source_file, "r", encoding="UTF-8")
        while True:
            line = f.readline()
            source_data.append(line)
            if not line:
                break
        f.close()

        for i in range(len(in_data)):
            if in_data[i] not in source_data:
                source_data.append(in_data[i])
                self.new_count += 1

        f = open(self.out_file, "w", encoding="UTF-8")
        for i in range(len(source_data)):
            f.write(source_data[i])
        f.close()

        print(f"Новых записей: {self.new_count}")


if __name__ == "__main__":
    MergeDataset().run()
