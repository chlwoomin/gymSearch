CREATE TABLE `Trainer` (
	`id`	BIGINT	NOT NULL,
	`sport_id`	BIGINT	NOT NULL,
	`gym_id`	BIGINT	NOT NULL,
	`sex`	VARCHAR(10)	NOT NULL	COMMENT '남/여',
	`experience_years`	SMALLINT(3)	NOT NULL	COMMENT '년 단위'
);

CREATE TABLE `Review` (
	`id`	BIGINT	NOT NULL,
	`gym_id`	BIGINT	NOT NULL,
	`score`	TINYINT(1)	NOT NULL	COMMENT '0~5',
	`comment`	TEXT	NULL	COMMENT '점수만 달기 가능'
);

CREATE TABLE `Detail_Region` (
	`id`	BIGINT	NOT NULL,
	`region_id`	BIGINT	NOT NULL,
	`detail_region_name`	VARCHAR(30)	NOT NULL
);

CREATE TABLE `Gym` (
	`id`	BIGINT	NOT NULL,
	`detail_region_id`	BIGINT	NOT NULL,
	`gym_name`	VARCHAR(20)	NOT NULL,
	`price`	INT(5)	NOT NULL,
	`open_time`	TIME	NOT NULL,
	`close_time`	TIME	NOT NULL,
	`remaining_membership`	INT(4)	NOT NULL,
	`latitude`	DECIMAL(10, 7)	NOT NULL,
	`longitude`	DECIMAL(10, 7)	NOT NULL,
	`averageRating`	DECIMAL(2,1)	NOT NULL	DEFAULT 0.0	COMMENT '리뷰가 없을 때 0점',
	`review_count`	INT(5)	NOT NULL	DEFAULT 0,
	`open_days`	TINYINT(1)	NOT NULL	COMMENT '월~일을 7bit로 저장',
	`address`	VARCHAR(50)	NOT NULL
);

CREATE TABLE `Class` (
	`id`	BIGINT	NOT NULL,
	`trainer_id`	BIGINT	NOT NULL,
	`class_name`	VARCHAR(15)	NULL,
	`start_time`	TIME	NOT NULL,
	`finsh_time`	TIME	NOT NULL,
	`capacity`	SMALLINT(2)	NOT NULL	DEFAULT 1,
	`booked`	SMALLINT(2)	NOT NULL	DEFAULT 0,
	`start_date`	DATE	NULL	COMMENT '언제든 가능한 경우 NULL',
	`end_date`	DATE	NULL	COMMENT '언제든 가능한 경우 NULL',
	`class_days`	TINYINT(1)	NOT NULL
);

CREATE TABLE `gym_sport` (
	`gym_id`	BIGINT	NOT NULL,
	`sport_id`	BIGINT	NOT NULL
);

CREATE TABLE `Sport` (
	`id`	BIGINT	NOT NULL,
	`sport`	VARCHAR(10)	NOT NULL
);

CREATE TABLE `Region` (
	`id`	BIGINT	NOT NULL,
	`region_name`	VARCHAR(10)	NOT NULL
);

ALTER TABLE `Trainer` ADD CONSTRAINT `PK_TRAINER` PRIMARY KEY (
	`id`
);

ALTER TABLE `Review` ADD CONSTRAINT `PK_REVIEW` PRIMARY KEY (
	`id`
);

ALTER TABLE `Detail_Region` ADD CONSTRAINT `PK_DETAIL_REGION` PRIMARY KEY (
	`id`
);

ALTER TABLE `Gym` ADD CONSTRAINT `PK_GYM` PRIMARY KEY (
	`id`
);

ALTER TABLE `Class` ADD CONSTRAINT `PK_CLASS` PRIMARY KEY (
	`id`
);

ALTER TABLE `gym_sport` ADD CONSTRAINT `PK_GYM_SPORT` PRIMARY KEY (
	`gym_id`,
	`sport_id`
);

ALTER TABLE `Sport` ADD CONSTRAINT `PK_SPORT` PRIMARY KEY (
	`id`
);

ALTER TABLE `Region` ADD CONSTRAINT `PK_REGION` PRIMARY KEY (
	`id`
);

ALTER TABLE `Trainer` ADD CONSTRAINT `FK_Sport_TO_Trainer_1` FOREIGN KEY (
	`sport_id`
)
REFERENCES `Sport` (
	`id`
);

ALTER TABLE `Trainer` ADD CONSTRAINT `FK_Gym_TO_Trainer_1` FOREIGN KEY (
	`gym_id`
)
REFERENCES `Gym` (
	`id`
);

ALTER TABLE `Review` ADD CONSTRAINT `FK_Gym_TO_Review_1` FOREIGN KEY (
	`gym_id`
)
REFERENCES `Gym` (
	`id`
);

ALTER TABLE `Detail_Region` ADD CONSTRAINT `FK_Region_TO_Detail_Region_1` FOREIGN KEY (
	`region_id`
)
REFERENCES `Region` (
	`id`
);

ALTER TABLE `Gym` ADD CONSTRAINT `FK_Region_TO_Gym_1` FOREIGN KEY (
	`detail_region_id`
)
REFERENCES `Detail_Region` (
	`id`
);

ALTER TABLE `Class` ADD CONSTRAINT `FK_Trainer_TO_Class_1` FOREIGN KEY (
	`trainer_id`
)
REFERENCES `Trainer` (
	`id`
);

ALTER TABLE `gym_sport` ADD CONSTRAINT `FK_Gym_TO_gym_sport_1` FOREIGN KEY (
	`gym_id`
)
REFERENCES `Gym` (
	`id`
);

ALTER TABLE `gym_sport` ADD CONSTRAINT `FK_Sport_TO_gym_sport_1` FOREIGN KEY (
	`sport_id`
)
REFERENCES `Sport` (
	`id`
);

