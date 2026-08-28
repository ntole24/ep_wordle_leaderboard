import pymysql
import os

class db:
    
    def __init__(self):
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

    def database_init(self):
        database_init = '''
            drop database if exists defaultdb;
            create database defaultdb;
        '''

        self.cursor = self.mysql.cursor()
        self.cursor.execute(database_init)
        self.mysql.commit()

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
            PRIMARY KEY (`score_id`),
            UNIQUE INDEX `score_id_UNIQUE` (`score_id` ASC) VISIBLE,
            INDEX `player_id_idx` (`player_id` ASC) VISIBLE,
            CONSTRAINT `player_id`
                FOREIGN KEY (`player_id`)
                REFERENCES `defaultdb`.`players` (`player_id`)
                ON DELETE CASCADE
                ON UPDATE NO ACTION);
        '''

        self.cursor.execute(create_scores)
        self.mysql.commit()

    def create_player(self, discord_id, name):
        create_player_query = """
            INSERT INTO defaultdb.players (
            discord_id, name
            ) 
            VALUES (%s, %s)
        """

        self.cursor.execute(create_player_query, (discord_id, name))
        self.mysql.commit()

        print("Success")

        return
    
    def read_all_players(self):
        read_all_players_query = """
            SELECT * FROM defaultdb.players
        """

        self.cursor.execute(read_all_players_query)

        result = self.cursor.fetchall()

        if result:
            return result
        else:
            print("No players wtaf")
            return -1
    
    def read_player_from_id(self, discord_id):
        read_player_query = """
            SELECT * FROM defaultdb.players WHERE discord_id = %s
        """

        self.cursor.execute(read_player_query, discord_id)

        result = self.cursor.fetchone()

        if result:
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

        # Delete the player
        delete_player_query = """
            DELETE FROM defaultdb.players
            WHERE player_id = %s
        """

        self.cursor.execute(delete_player_query, player_id)
        self.mysql.commit()

        # Delete that player's scores

        return
    
    # discord_id - string
    # Guesses - int
    # date - Date
    def create_score(self, discord_id, guesses, date):
        print("Creating a score!")
        buffer = self.read_player_from_id(discord_id)
        player_id = buffer['player_id'] 

        create_score_query = """
            INSERT INTO defaultdb.scores (
            player_id, guesses, date
            ) 
            VALUES (%s, %s, %s)
        """

        self.cursor.execute(create_score_query, (player_id, guesses, date))
        self.mysql.commit()



        return
    
    def read_scores(self):
        read_scores_query = """
            SELECT * FROM defaultdb.scores
        """

        self.cursor.execute(read_scores_query)

        result = self.cursor.fetchall()

        if result:
            return result
        else:
            print("No scores wtaf")
            return -1

    def read_scores_from_discord_id(self, discord_id):
        """ buffer = self.read_player_from_id(discord_id)
        player_id = buffer['player_id'] """

        player_id = "1" # REMOVE THIS LATER!!!

        read_player_query = """
            SELECT * FROM defaultdb.scores WHERE player_id = %s
        """

        self.cursor.execute(read_player_query, player_id)

        result = self.cursor.fetchall()

        if result:
            return result
        else:
            print("Person doesn't exist oohhh spooky")
            return -1
        
    def read_player_stats(self, orderType):
        asc_or_desc = "ASC"

        if orderType == "Total_Games":
            asc_or_desc = "DESC"

        player_total_query = f"""
            SELECT s.player_id as Player_ID, p.name as Name, SUM(s.guesses) as Total_Guesses, ROUND(AVG(s.guesses * 1.0), 2) as Average_Guesses, COUNT(p.player_id) as Total_Games
            FROM defaultdb.scores s
            JOIN defaultdb.players p on s.player_id = p.player_id
            GROUP BY s.player_id, p.name
            ORDER BY {orderType} {asc_or _desc};
        """

        self.cursor.execute(player_total_query)

        result = self.cursor.fetchall()

        if result:
            return result
        else:
            print("No scores???")
            return -1
        
    def get_score_from_id_and_date(self, discord_id, date):
        score_from_id_and_date_query = """
            SELECT *
            FROM defaultdb.scores s
            JOIN defaultdb.players p on s.player_id = p.player_id
            WHERE p.discord_id = %s AND s.date = %s 
        """

        self.cursor.execute(score_from_id_and_date_query, (discord_id, str(date)))
        
        result = self.cursor.fetchall()

        if result:
            return result
        else:
            print("No score???")
            return -1

    def get_total_games(self):
        total_games_query = """
            SELECT p.name, COUNT(p.player_id) as Total_Games
            FROM defaultdb.scores s
            JOIN defaultdb.players p on s.player_id = p.player_id
            GROUP BY p.player_id;
        """

        self.cursor.execute(total_games_query)
                
        result = self.cursor.fetchall()

        if result:
            return result
        else:
            print("No score???")
            return -1