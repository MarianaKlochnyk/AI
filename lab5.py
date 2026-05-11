import random
import json
import os

# --- КОНФІГУРАЦІЯ ТА ДАНІ ---
subjects = ["Math", "Ukrainian", "English", "PE", "Music", "Art"]

# Вчителі за спеціалізацією
teachers = {
    "Math": "T1",
    "Ukrainian": "T1",
    "English": "T2",
    "PE": "T3",
    "Music": "T4",
    "Art": "T2"
}

# Класні керівники для кожного класу
main_teachers = {
    "A": "T1",
    "B": "T2"
}

# Спеціалізовані приміщення
special_rooms = {
    "PE": "Gym",
    "Music": "MusicRoom"
}

classes = ["A", "B"]
days = 5
lessons_per_day = 5

# Параметри ГА
POP_SIZE = 20
GENERATIONS = 100
MUTATION_RATE = 0.15

# --- ФУНКЦІЇ РОБОТИ З ДАНИМИ ---
def save_data(filename="school_data.json"):
    data = {
        "subjects": subjects,
        "teachers": teachers,
        "classes": classes,
        "main_teachers": main_teachers,
        "special_rooms": special_rooms
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def create_random_lesson():
    subject = random.choice(subjects)
    teacher = teachers[subject]
    room = special_rooms.get(subject, f"Room_{subject}")
    return subject, teacher, room

def create_random_schedule():
    schedule = []
    for c in classes:
        class_schedule = []
        for d in range(days):
            day_schedule = []
            for l in range(lessons_per_day):
                day_schedule.append(create_random_lesson())
            class_schedule.append(day_schedule)
        schedule.append(class_schedule)
    return schedule

# --- ГЕНЕТИЧНИЙ АЛГОРИТМ ---
def fitness(schedule):
    penalty = 0
    for c in range(len(classes)):
        teacher_time = set()
        room_time = set()
        teacher_count = {}

        for d in range(days):
            day = schedule[c][d]
            started = False
            gap = False

            for l in range(lessons_per_day):
                subject, teacher, room = day[l]

                # Перевірка на "вікна" (якщо в моделі є None, але тут ми заповнюємо все)
                if subject is not None:
                    started = True
                    if gap: penalty += 10
                else:
                    if started: gap = True

                # Конфлікт вчителя (один вчитель у двох класах одночасно)
                key_t = (teacher, d, l)
                if key_t in teacher_time:
                    penalty += 15
                teacher_time.add(key_t)

                # Конфлікт кабінету (особливо Gym та MusicRoom)
                key_r = (room, d, l)
                if key_r in room_time:
                    penalty += 15
                room_time.add(key_r)

                teacher_count[teacher] = teacher_count.get(teacher, 0) + 1

        # Перевірка умови класного керівника (мінімум 50% уроків)
        main_teacher = main_teachers[classes[c]]
        total_lessons = days * lessons_per_day
        if teacher_count.get(main_teacher, 0) < total_lessons * 0.5:
            penalty += 50  # Високий штраф за невиконання головної умови завдання

    return penalty

def crossover(p1, p2):
    child = []
    for c in range(len(classes)):
        point = random.randint(1, days - 1)
        child_class = p1[c][:point] + p2[c][point:]
        child.append(child_class)
    return child

def mutate(schedule):
    for c in range(len(classes)):
        for d in range(days):
            if random.random() < MUTATION_RATE:
                l1, l2 = random.sample(range(lessons_per_day), 2)
                schedule[c][d][l1], schedule[c][d][l2] = \
                    schedule[c][d][l2], schedule[c][d][l1]
    return schedule

def genetic_algorithm():
    population = [create_random_schedule() for _ in range(POP_SIZE)]

    for gen in range(GENERATIONS):
        population = sorted(population, key=fitness)
        best_fit = fitness(population[0])

        if gen % 10 == 0:
            print(f"Покоління {gen}: Штраф = {best_fit}")

        if best_fit == 0:
            break

        new_pop = population[:5] # Елітизм
        while len(new_pop) < POP_SIZE:
            p1, p2 = random.sample(population[:10], 2)
            child = mutate(crossover(p1, p2))
            new_pop.append(child)
        population = new_pop

    return sorted(population, key=fitness)[0]

# --- ВИВІД ТА ЗВІТНІСТЬ ---
def print_schedule_with_report(schedule):
    print("\n" + "█"*50)
    print("ОПТИМІЗОВАНИЙ РОЗКЛАД ЗАНЯТЬ")
    print("█"*50)

    for c in range(len(classes)):
        class_name = classes[c]
        main_teacher = main_teachers[class_name]
        
        print(f"\nКЛАС: {class_name} | Класний керівник: {main_teacher}")
        print("-" * 45)
        print(f"{'Урок':<6} | {'Понеділок':<12} | {'Вівторок':<12} | {'Середа':<12} | {'Четвер':<12} | {'П’ятниця':<12}")
        print("-" * 45)

        # Для красивого виводу по рядках (уроки 1-5)
        teacher_load = 0
        total_lessons = 0

        for l in range(lessons_per_day):
            row = [f"{l+1}"]
            for d in range(days):
                subject, teacher, room = schedule[c][d][l]
                row.append(f"{subject} ({teacher})")
                
                total_lessons += 1
                if teacher == main_teacher:
                    teacher_load += 1
            print(" | ".join(f"{item:<12}" for item in row))

        # Підсумок умови
        percentage = (teacher_load / total_lessons) * 100
        is_ok = teacher_load >= (total_lessons * 0.5)

        print("-" * 45)
        print(f"ЗВІТ: Керівник {main_teacher} веде {teacher_load} з {total_lessons} уроків.")
        print(f"Навантаження: {percentage:.1f}% | Умова >= 50%: {'✅ ВИКОНАНО' if is_ok else '❌ НЕ ВИКОНАНО'}")
        print("-" * 45)

if __name__ == "__main__":
    save_data()
    best_schedule = genetic_algorithm()
    print_schedule_with_report(best_schedule)