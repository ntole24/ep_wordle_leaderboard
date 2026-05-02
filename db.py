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
        self.mysql.commit()

        create_scores = '''
            CREATE TABLE `defaultdb`.`scores` (
            `score_id` INT NOT NULL AUTO_INCREMENT,
            `player_id` INT NOT NULL,
            `guesses` INT NOT NULL,
            `date` DATE NOT NULL,
            PRIMARY KEY (`score_id`));
        '''

        self.cursor.execute(create_scores)
        self.mysql.commit()

    def create_player(self, discord_id, name):
        create_player_query = """
        INSERT INTO defaultdb.players (
	    discord_id, name
        ) 
        VALUES ('%s', '%s')"""

        self.cursor.execute(create_player_query % (discord_id, name))
        self.mysql.commit()

        print("Success")

        return
    
    def read_player_from_id(self, discord_id):
        read_player_query = """
            SELECT * FROM defaultdb.players WHERE discord_id = %s
        """

        self.cursor.execute(read_player_query % discord_id)
        self.mysql.commit()

        result = self.cursor.fetchone()

        if result:
            print("Result: ", result)
            print(result['player_id'])
            return result
        else:
            print("Person doesn't exist oohhh spooky")
            return -1
    
    def update_player_name(self, discord_id, name):
        row = self.read_player_from_id(discord_id)
        player_id = row['player_id']

        update_player_query = """
            UPDATE defaultdb.players p
            SET p.name = %s
            WHERE p.player_id = %s
        """

        self.cursor.execute(update_player_query, (name, player_id))
        self.mysql.commit()

        return
    
    def delete_player(self, discord_id):
        row = self.read_player_from_id(discord_id)
        player_id = row['player_id']

        delete_player_query = """
            DELETE FROM defaultdb.players
            WHERE player_id = %s
        """

        self.cursor.execute(delete_player_query, player_id)
        self.mysql.commit()

        return

    