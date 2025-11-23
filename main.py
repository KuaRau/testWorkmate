import csv
from collections import defaultdict
from tabulate import tabulate
import argparse

def give_report(file_list):
    perf_by_pos = defaultdict(list)

    for file_path in file_list:
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        position = row['position']
                        performance = float(row['performance'])
                        perf_by_pos[position].append(performance)
                    except (KeyError, ValueError) as e:
                        print(f" Ошибка: {e}")

        except FileNotFoundError:
            print(f"Ошибка, файл {file_path} не найден")
            continue
        except Exception as e:
            print(f"Ошибка с файлом {file_path}: {e}")
            continue

    average_perf = {}
    for position, performances in perf_by_pos.items():
        if performances:
            average_perf[position] = sum(performances) / len(performances)

    sorted_performance = sorted(average_perf.items(), key=lambda item: item[1], reverse=True)

    return sorted_performance

def main():
    parser = argparse.ArgumentParser(description='Анализ эффективности работы разработчиков.')
    parser.add_argument('--files', nargs='+', required=True, help='Список CSV файлов для обработки.')
    parser.add_argument('--report', type=str, required=True, help='Название отчета для формирования.')

    args = parser.parse_args()

    if args.report == 'performance':
        report_data = give_report(args.files)
        if report_data:
            headers = ["position", "performance"]

            formatted_data = [[pos, f"{perf:.2f}"] for pos, perf in report_data]
            print(tabulate(formatted_data, headers=headers, showindex="always"))
    else:
        print(f"Отчет с названием '{args.report}' не поддерживается.")



if __name__ == "__main__":
    main()