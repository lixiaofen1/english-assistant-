import time
from datetime import datetime, timedelta
import heapq
import word


class EbbinghausScheduler:
    def __init__(self):
        self.review_intervals = [
            (1, "分钟"),  # 初次记忆后1分钟
            (10, "分钟"),  # 10分钟后
            (1, "小时"),  # 1小时后
            (2, "小时"),  # 2小时后
            (6, "小时"),  # 6小时后
            (1, "天"),  # 1天后
            (2, "天"),  # 2天后
            (6, "天"),  # 6天后
            (14, "天"),  # 14天后
            (30, "天")  # 30天后
        ]
        self.schedule = []
        self.word_list = word.word_n
        self.start_time = datetime.now()
        self.word = None

    def add_words(self, words):
        """添加单词到复习队列"""
        for idx, word in enumerate(words):
            # 为每个单词创建复习计划
            review_times = []
            current_time = self.start_time
            for interval, unit in self.review_intervals:
                # 计算每个复习时间点
                if unit == "分钟":
                    current_time += timedelta(minutes=interval)
                elif unit == "小时":
                    current_time += timedelta(hours=interval)
                elif unit == "天":
                    current_time += timedelta(days=interval)
                review_times.append(current_time)

            # 将单词和复习计划加入优先队列
            heapq.heappush(self.schedule, (review_times[0], idx, word, review_times))
            self.word_list.append((word, review_times))

    def run_scheduler(self):
        """运行复习调度器"""
        print(f"复习开始时间：{self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 40)

        while self.schedule:
            # 获取下一个最近的复习任务
            review_time, idx, word, all_times = heapq.heappop(self.schedule)
            current_time = datetime.now()

            # 计算等待时间（精确到秒）
            wait_seconds = max(0, (review_time - current_time).total_seconds())
            if wait_seconds > 0:
                print(f"等待 {wait_seconds:.0f} 秒至 {review_time.strftime('%H:%M:%S')}")
                time.sleep(wait_seconds)

            # 执行复习
            print(f"\n【复习时间】{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"单词：{word}")
            self.word = word
            print(f"复习进度：{self.word_list[idx][1].index(review_time) + 1}/{len(self.review_intervals)} 次")
            print(
                f"下次复习：{all_times[self.word_list[idx][1].index(review_time) + 1].strftime('%Y-%m-%d %H:%M:%S')}" if
                self.word_list[idx][1].index(review_time) + 1 < len(self.word_list[idx][1]) else "复习完成！")

            # 如果还有后续复习，重新加入调度队列
            next_review_index = self.word_list[idx][1].index(review_time) + 1
            if next_review_index < len(self.word_list[idx][1]):
                heapq.heappush(self.schedule,
                               (self.word_list[idx][1][next_review_index],
                                idx,
                                word,
                                self.word_list[idx][1]))

        print("\n所有单词复习计划已完成！")


#使用示例
if __name__ == "__main__":
    # 初始化单词列表（可替换为文件读取）
    words = [
        "Abandon", "Zephyr", "Ephemeral", "Serendipity",
        "Luminescent", "Petrichor", "Euphoria", "Melancholy"
    ]

    # 创建调度器并添加单词
    scheduler = EbbinghausScheduler()
    scheduler.add_words(words)

    # 运行复习调度
    try:
        scheduler.run_scheduler()
    except KeyboardInterrupt:
        print("\n复习计划已手动终止")