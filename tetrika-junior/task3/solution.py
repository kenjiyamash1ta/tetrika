def appearance(intervals: dict[str, list[int]]) -> int:
    def process_intervals(times, lesson_start, lesson_end):
        # Формируем интервалы
        intervals = [(times[i], times[i+1]) for i in range(0, len(times), 2)]
        intervals.sort()
        # Объединяем пересекающиеся интервалы
        merged = []
        for start, end in intervals:
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))
        # Обрезаем интервалы по границам урока
        result = []
        for start, end in merged:
            new_start = max(start, lesson_start)
            new_end = min(end, lesson_end)
            if new_start < new_end:
                result.append((new_start, new_end))
        return result

    lesson_start, lesson_end = intervals['lesson']
    pupil_processed = process_intervals(intervals['pupil'],
                                        lesson_start,
                                        lesson_end)
    tutor_processed = process_intervals(intervals['tutor'],
                                        lesson_start,
                                        lesson_end)

    # Находим пересечения интервалов pupil и tutor
    common_time = 0
    i = j = 0
    while i < len(pupil_processed) and j < len(tutor_processed):
        pupil_start, pupil_end = pupil_processed[i]
        tutor_start, tutor_end = tutor_processed[j]
        start = max(pupil_start, tutor_start)
        end = min(pupil_end, tutor_end)
        if start < end:
            common_time += end - start
        if pupil_end < tutor_end:
            i += 1
        else:
            j += 1
    return common_time
