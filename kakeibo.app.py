class KakeiboAnalyzer:

    def __init__(self):
        self.date_data = {}
        self.category_data = {}
        self.month_data = {}

    def parse_line(self, line):
        date, category, amount = line.strip().split(",")
        return date, category, int(amount)

    def create_stat(self):
        return {"sum": 0, "count": 0}

    def load(self, filename):
        try:
            with open(filename, encoding="utf-8") as f:
                for line in f:
                    try:
                        date, category, amount = self.parse_line(line)
                    except ValueError:
                        continue

                    month = date[:7]

                    # 日付別
                    if date not in self.date_data:
                        self.date_data[date] = self.create_stat()
                    self.date_data[date]["sum"] += amount
                    self.date_data[date]["count"] += 1

                    # カテゴリ別
                    if category not in self.category_data:
                        self.category_data[category] = self.create_stat()
                    self.category_data[category]["sum"] += amount
                    self.category_data[category]["count"] += 1

                    # 月別
                    if month not in self.month_data:
                        self.month_data[month] = self.create_stat()
                    self.month_data[month]["sum"] += amount
                    self.month_data[month]["count"] += 1

        except FileNotFoundError:
            print("ファイルが存在しません")
            return False

        return True

    def calc_stats(self, base_data):
        return {
            name: {
                "sum": v["sum"],
                "count": v["count"],
                "avg": v["sum"] / v["count"] if v["count"] else 0
            }
            for name, v in base_data.items()
        }

    def get_stats(self):
        return self.calc_stats(self.date_data)

    def get_category_stats(self):
        return self.calc_stats(self.category_data)

    def get_month_stats(self):
        return self.calc_stats(self.month_data)

    def get_top_category(self):
        if not self.category_data:
            return None, None

        top_category_name = max(
            self.category_data,
            key=lambda k: self.category_data[k]["sum"]
        )
        return top_category_name, self.category_data[top_category_name]

    def print_ranking(self, stats, title, key="sum", reverse=True):
        print("\n" + "=" * 40)
        print(title)
        print("=" * 40)

        sort_data = sorted(
            stats.items(),
            key=lambda x: x[1][key],
            reverse=reverse
        )

        for i, (name, v) in enumerate(sort_data, 1):
            print(
                f"{i:>2}位 {name:<10} | 合計:{v['sum']:>8}円 | 平均:{v['avg']:>8.1f}円"
            )


# ===== ここから実行処理 =====

filename = input("ファイル名を入力してください: ")

analyzer = KakeiboAnalyzer()

if not analyzer.load(filename):
    exit()

while True:
    print("\n====== 家計簿分析ツール ======")
    print("1: カテゴリ別（合計）")
    print("2: カテゴリ別（平均）")
    print("3: 月別（合計）")
    print("4: 月別（平均）")
    print("5: 日付別（合計）")
    print("6: 日付別（平均）")
    print("7: 一番使ったカテゴリ")
    print("0: 終了")

    choice = input("選択してください: ")

    if choice == "1":
        analyzer.print_ranking(
            analyzer.get_category_stats(),
            "カテゴリ別（合計）"
        )
    elif choice == "2":
        analyzer.print_ranking(
            analyzer.get_category_stats(),
            "カテゴリ別（平均）",
            key="avg"
        )
    elif choice == "3":
        analyzer.print_ranking(
            analyzer.get_month_stats(),
            "月別（合計）"
        )
    elif choice == "4":
        analyzer.print_ranking(
            analyzer.get_month_stats(),
            "月別（平均）",
            key="avg"
        )
    elif choice == "5":
        analyzer.print_ranking(
            analyzer.get_stats(),
            "日付別（合計）"
        )
    elif choice == "6":
        analyzer.print_ranking(
            analyzer.get_stats(),
            "日付別（平均）",
            key="avg"
        )
    elif choice == "7":
        name, data = analyzer.get_top_category()
        if name and data:
            print(f"\n一番使ったカテゴリ: {name}（{data['sum']}円）")
        else:
            print("データがありません")
    elif choice == "0":
        print("終了します")
        break
    else:
        print("無効な入力です")
        break
    else:
        print("無効な入力です")