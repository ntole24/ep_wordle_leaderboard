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
        read_all_scores_query = """
            SELECT * FROM defaultdb.scores
        """

        self.cursor.execute(read_all_scores_query)

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
        
    def read_player_stats_totalOrder(self):
        player_total_query = """
            SELECT s.player_id as Player_ID, p.name as Name, SUM(s.guesses) as Total_Guesses, ROUND(AVG(s.guesses * 1.0), 2) as Average_Guesses            FROM defaultdb.scores s
            JOIN defaultdb.players p on s.player_id = p.player_id
            GROUP BY s.player_id, p.name
            ORDER BY SUM(s.guesses) ASC;
        """

        self.cursor.execute(player_total_query)

        result = self.cursor.fetchall()

        if result:
            return result
        else:
            print("No scores???")
            return -1
        
    def read_player_stats_averageOrder(self):
        player_total_query = """
            SELECT s.player_id as Player_ID, p.name as Name, SUM(s.guesses) as Total_Guesses, ROUND(AVG(s.guesses * 1.0), 2) as Average_Guesses
            FROM defaultdb.scores s
            JOIN defaultdb.players p on s.player_id = p.player_id
            GROUP BY s.player_id, p.name
            ORDER BY AVG(s.guesses) ASC;
        """

        self.cursor.execute(player_total_query)

        result = self.cursor.fetchall()

        if result:
            return result
        else:
            print("No scores???")
            return -1

    def sample_players(self):
        query = """
            INSERT INTO defaultdb.players (discord_id, name) VALUES
            ('3847291056', 'Alice'),
            ('7193048572', 'Bob'),
            ('5820394716', 'Charlie'),
            ('9174836205', 'Diana'),
            ('2648193057', 'Ethan'),
            ('8315720496', 'Fiona'),
            ('4072958631', 'George'),
            ('6531804927', 'Hannah'),
            ('1897345062', 'Ivan');
        """

        self.cursor.execute(query)
        self.mysql.commit()
        
    def sample_scores(self):
        query = """
        INSERT INTO defaultdb.scores (player_id, guesses, date) VALUES
            (3, 4, '2024-01-15'),
            (1, 2, '2024-01-15'),
            (5, 6, '2024-01-16'),
            (2, 1, '2024-01-16'),
            (4, 3, '2024-01-17'),
            (1, 7, '2024-01-17'),
            (3, 5, '2024-01-18'),
            (5, 2, '2024-01-18'),
            (2, 4, '2024-01-19'),
            (4, 6, '2024-01-19'),
            (1, 1, '2024-01-20'),
            (3, 3, '2024-01-20'),
            (5, 7, '2024-01-21'),
            (2, 2, '2024-01-21'),
            (4, 5, '2024-01-22'),
            (1, 4, '2024-01-22'),
            (3, 6, '2024-01-23'),
            (5, 1, '2024-01-23'),
            (2, 3, '2024-01-24'),
            (4, 7, '2024-01-24'),
            (1, 2, '2024-01-25'),
            (3, 5, '2024-01-25'),
            (5, 4, '2024-01-26'),
            (2, 6, '2024-01-26'),
            (4, 1, '2024-01-27'),
            (1, 3, '2024-01-27'),
            (3, 7, '2024-01-28'),
            (5, 2, '2024-01-28'),
            (2, 5, '2024-01-29'),
            (4, 4, '2024-01-29'),
            (1, 6, '2024-02-01'),
            (3, 1, '2024-02-01'),
            (5, 3, '2024-02-02'),
            (2, 7, '2024-02-02'),
            (4, 2, '2024-02-03'),
            (1, 5, '2024-02-03'),
            (3, 4, '2024-02-04'),
            (5, 6, '2024-02-04'),
            (2, 1, '2024-02-05'),
            (4, 3, '2024-02-05'),
            (1, 7, '2024-02-06'),
            (3, 2, '2024-02-06'),
            (5, 5, '2024-02-07'),
            (2, 4, '2024-02-07'),
            (4, 6, '2024-02-08'),
            (1, 1, '2024-02-08'),
            (3, 3, '2024-02-09'),
            (5, 7, '2024-02-09'),
            (2, 2, '2024-02-10'),
            (4, 5, '2024-02-10');        
        """

        self.cursor.execute(query)
        self.mysql.commit()

        return
    
    def sample_duplicate(self, i):
        print("duplicating!!!")
        
        query = ""

        if i == 0:
            query = """ INSERT INTO defaultdb.scores (player_id, guesses, date) VALUES
                (3, 4, '2024-01-15'); """
        elif i == 1:
            query = """ INSERT INTO defaultdb.scores (player_id, guesses, date) VALUES
                (3, 4, '2024-01-15'); """
        elif i == 2:
            query = """ INSERT INTO defaultdb.scores (player_id, guesses, date) VALUES
                (3, 4, '2024-01-15'); """
        elif i == 3:
            query = """ INSERT INTO defaultdb.scores (player_id, guesses, date) VALUES
                (3, 4, '2024-01-15'); """
        elif i == 4:
            query = """ INSERT INTO defaultdb.scores (player_id, guesses, date) VALUES
                (3, 4, '2024-01-15'); """

        
        self.cursor.execute(query)
        self.mysql.commit()

        return