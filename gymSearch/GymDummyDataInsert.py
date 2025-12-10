import random
import pymysql
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("ko_KR")

# ===================== DB 연결 =====================
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="gym",
    charset="utf8mb4"
)
cur = conn.cursor()

# ===================== Region =====================
regions = [
    "서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종",
    "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"
]

cur.executemany(
    "INSERT INTO Region (id, region_name) VALUES (%s, %s)",
    [(i+1, name) for i, name in enumerate(regions)]
)
print("Region OK")

# ===================== Detail_Region =====================

import json
with open("region_detail.json", "r", encoding="utf-8") as f:
    region_detail_map = json.load(f)
detail_regions = []
detail_id = 1
for region_id, region_name in enumerate(regions, start=1):
    for detail_name in region_detail_map[region_name]:
        detail_regions.append((detail_id, region_id, detail_name))
        detail_id += 1

cur.executemany(
    "INSERT INTO Detail_Region (id, region_id, detail_region_name) VALUES (%s,%s,%s)",
    detail_regions
)
print("Detail_Region OK")

# ===================== Sport =====================
sports_list = [
    "헬스", "요가", "필라테스", "크로스핏", "줌바", "수영",
    "복싱", "클라이밍", "테니스", "골프"
]

cur.executemany(
    "INSERT INTO Sport (id, sport) VALUES (%s, %s)",
    [(i+1, s) for i, s in enumerate(sports_list)]
)
print("Sport OK")

# ===================== Gym 6000개 =====================
gym_data = []

gym_types = ["헬스", "요가", "필라테스", "크로스핏", "짐"]
gym_brands = ["바디플랜","헬스존","피트니스24","파워짐","스포짐"]

gym_id = 1
for region_name in regions:
    detail_names = region_detail_map[region_name]
    for _ in range(random.randint(1000, 2000)):  # 지역당 헬스장 수
        detail_name = random.choice(detail_names)
        price = random.choice([30000, 40000, 50000, 60000])
        open_t = f"{random.randint(5,8)}:00:00"
        close_t = f"{random.randint(20,23)}:00:00"
        capacity = random.randint(30, 200)
        lat = round(random.uniform(33.1, 38.6), 7)
        lon = round(random.uniform(125.1, 131.9), 7)
        open_days = random.randint(0, 127)  # 7bit 월~일

        # 실제 같은 헬스장 이름 생성: [상세지역 + 유형 + 브랜드]
        gym_name = f"{detail_name} {random.choice(gym_types)} {random.choice(gym_brands)}"

        address = f"{region_name} {detail_name}"

        detail_region_id = next(
            (i+1 for i, t in enumerate(detail_regions) if t[2] == detail_name),
            None
        )
        gym_data.append((
            gym_id,
            detail_region_id,  # detail_region_id
            gym_name,
            price,
            open_t,
            close_t,
            capacity,
            lat,
            lon,
            0.0,  # averageRating
            0,    # review_count
            open_days,
            address
        ))

        gym_id += 1

cur.executemany("""
INSERT INTO Gym (
    id, detail_region_id, gym_name, price, open_time, close_time,
    remaining_membership, latitude, longitude,
    averageRating, review_count, open_days, address
) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
""", gym_data)
print("Gym OK")

# ===================== gym_sport =====================
gym_count = len(gym_data)
gym_sport_data = []
for gym_id in range(1, gym_count + 1):
    sport_ids = random.sample(range(1, len(sports_list) + 1), random.randint(1, 3))
    for sid in sport_ids:
        gym_sport_data.append((gym_id, sid))

cur.executemany(
    "INSERT INTO gym_sport (gym_id, sport_id) VALUES (%s, %s)",
    gym_sport_data
)
print("gym_sport OK")

# ===================== Trainer =====================
trainer_data = []
trainer_id = 1
for gym_id in range(1, gym_count + 1):
    for _ in range(random.randint(2, 7)):
        sex = random.choice(["남", "여"])
        sport_id = random.randint(1, len(sports_list))
        exp = random.randint(1, 30)
        trainer_data.append((trainer_id, sport_id, gym_id, sex, exp))
        trainer_id += 1

cur.executemany("""
INSERT INTO Trainer (id, sport_id, gym_id, sex, experience_years)
VALUES (%s,%s,%s,%s,%s)
""", trainer_data)
print("Trainer OK")

# ===================== Class =====================

class_data = []
class_id = 1

for t_id, _, gym_id, _, _ in trainer_data:
    for _ in range(random.randint(1, 5)):  # 트레이너당 1~5개 수업
        # 수업 시간
        start_hour = random.randint(6, 20)
        start = datetime.now().replace(hour=start_hour, minute=0, second=0, microsecond=0)
        end = start + timedelta(hours=1)

        # 수업 이름
        class_name = f"{random.choice(sports_list)} 클래스 {random.randint(1000,9999)}"

        # 수업 최대 인원
        capacity = random.randint(1, 20)

        # 현재 예약 인원 (0~capacity)
        booked = random.randint(0, capacity)

        # 기간형 클래스 (랜덤으로 None 또는 실제 날짜)
        if random.random() < 0.7:  # 70%는 기간 지정
            start_date = start.date() + timedelta(days=random.randint(0, 7))
            end_date = start_date + timedelta(days=random.randint(7, 30))
        else:
            start_date = None
            end_date = None

        # 수업 요일 (월~일 7bit)
        class_days = random.randint(1, 127)

        class_data.append((
            class_id, t_id, class_name, start.time(), end.time(),
            capacity, booked, start_date, end_date, class_days
        ))
        class_id += 1

cur.executemany("""
INSERT INTO Class (
    id, trainer_id, class_name, start_time, finsh_time,
    capacity, booked, start_date, end_date, class_days
) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
""", class_data)

print("Class OK")

# ===================== Review =====================
review_data = []
review_id = 1
for gym_id in range(1, gym_count + 1):
    for _ in range(random.randint(1, 30)):
        score = random.randint(1, 5)
        cmt = fake.sentence() if random.random() < 0.5 else None
        review_data.append((review_id, gym_id, score, cmt))
        review_id += 1

cur.executemany("""
INSERT INTO Review (id, gym_id, score, comment)
VALUES (%s, %s, %s, %s)
""", review_data)
print("Review OK")

conn.commit()
cur.close()
conn.close()

print("🎉 모든 더미데이터 생성 완료!")
