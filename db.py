import pymysql
import os

class db:
    
    def __init__(self):
        database_init = '''
            drop database if exists defaultdb;
            create database defaultdb;
        '''
        self.mysql = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            port=int(os.getenv('DB_PORT')),
            password=os.getenv('DB_PASSWORD'),
            client_flag=(
                pymysql.constants.CLIENT.MULTI_STATEMENTS |
                pymysql.constants.CLIENT.LOCAL_FILES    
            ),
            cursorclass=pymysql.cursors.DictCursor,
            local_infile=True 
        )

        self.cursor = self.mysql.cursor()
        self.cursor.execute(database_init)
        self.mysql.commit()

        print("successful!!!")

    def tables_init(self):
        create_players = '''
            CREATE TABLE `defaultdb`.`players` (
            `player_id` INT NOT NULL AUTO_INCREMENT,
            `discord_id` VARCHAR(100) NOT NULL,
            `name` VARCHAR(100) NOT NULL,
            PRIMARY KEY (`player_id`),
            UNIQUE INDEX `player_id_UNIQUE` (`player_id` ASC) VISIBLE,
            UNIQUE INDEX `discord_id_UNIQUE` (`discord_id` ASC) VISIBLE);
        '''

        self.cursor.execute(create_players)

        create_scores = '''
            CREATE TABLE `defaultdb`.`scores` (
            `score_id` INT NOT NULL AUTO_INCREMENT,
            `player_id` INT NOT NULL,
            `guesses` INT NOT NULL,
            `date` DATE NOT NULL,
            PRIMARY KEY (`score_id`));
        '''

        self.cursor.execute(create_scores)

        print("successful2!!!")

    def create_player(self, discord_id, name):
        query = """
        INSERT INTO defaultdb.players (
	    discord_id, name
        ) 
        VALUES ('%s', '%s')"""
        
        return
    
    def read_player(self):
        return
    
    def update_player(self):
        return
    
    def delete_player(self):
        return

    