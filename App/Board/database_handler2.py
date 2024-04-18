import mysql.connector

# hierbij wordt de classe aangemaakt
class DbHandler:
    def __init__(self):
        self.error_message = ""
        try:
            self.mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="scrum"
            )
            self.mycursor = self.mydb.cursor()
        except mysql.connector.Error as err:
            self.error_message = "Database connection error: {}".format(err)

    def read_names(self):
        try:
            self.mycursor.execute("SELECT userID, username, password, RightID FROM users")
            return self.mycursor.fetchall()
        except mysql.connector.Error as err:
            self.error_message = "Error fetching user data: {}".format(err)
            return []
        

    def get_tickets_data(self):
        try:
            self.mycursor.execute("""SELECT users.username, rights.rightname, tickets.title, tickets.description, tickets.hours, status.statusname FROM UserTicket 
                                  INNER JOIN users on userticket.userID = users.userID 
                                  INNER JOIN rights on users.rightID = rights.rightID
                                  INNER JOIN tickets on userticket.ticketID = tickets.ticketID
                                  INNER JOIN status on tickets.statusID = status.statusID""")
            return self.mycursor.fetchall()
        except mysql.connector.Error as err:
            self.error_message = "ERROR fetching information for tickets data failed: {}".format(err)

    # Creates a user and returns its id if successful
    def add_user(self, username, password, rightID):
        try:
            sql = "INSERT INTO users(username, password, rightID) VALUES (%s,%s,%s)"
            val = (username, password, rightID)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            return self.mycursor.lastrowid
        except mysql.connector.Error as err:
            self.error_message = "Error adding user: {}".format(err)

    # Creates a ticket and returns its id if successful
    def add_ticket(self, Title, Description, Hours, statusID):
        try: 
            ticket_sql = "INSERT INTO tickets(title, description, hours, statusID) VALUES (%s,%s,%s,%s)"
            ticket_val = (Title, Description, Hours, statusID)
            self.mycursor.execute(ticket_sql, ticket_val)
            self.mydb.commit()
            return self.mycursor.lastrowid
        except mysql.connector.Error as err:
            self.error_message = "Error adding ticket: {}".format(err) 
    
    def add_user_to_ticket(self, UserID, TicketID):
        try:
            user_ticket_sql = "INSERT INTO Userticket(UserID, TicketID) VALUES (%s, %s)"
            user_ticket_val = (UserID, TicketID)
            self.mycursor.execute(user_ticket_sql, user_ticket_val)
            self.mydb.commit()
        except mysql.connector.Error as err:
            self.error_message = "Error adding user to ticket: {}".format(err) 

    def update_ticket_status(self, TicketID, StatusID):
        try:
            sql = "UPDATE tickets SET statusID = %s WHERE ticketID = %s" 
            val = (StatusID, TicketID)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
        except mysql.connector.Error as err:
            self.error_message = f"Error updating ticket status: {err}"
    
    def update_ticket_title(self, TicketID, Title):
        try:
            sql = "UPDATE tickets SET title = %s WHERE ticketID = %s"
            val = (TicketID, Title)
            self.mycursor.execute(sql,val)
            self.mydb.commit()
        except mysql.connector.Error as err:
            self.error_message = f"Error updating ticket title: {err}"


    def update_ticket_description(self, TicketID, Description):
        try:
            sql = "UPDATE tickets SET description = %s WHERE TicketID = %s"
            val = (TicketID, Description)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
        except mysql.connector.Error as err:
            self.error_message = f"Error updating ticket description: {err}"


    def remove_ticket(self, TicketID):
        try: 

            sql_userticket = "DELETE FROM userticket WHERE TicketID = %s"
            val_userticket = (TicketID,)
            self.mycursor.execute(sql_userticket,val_userticket)

            sql_ticket = "DELETE FROM tickets WHERE TicketID = %s"
            val_ticket = (TicketID,)
            self.mycursor.execute(sql_ticket,val_ticket)
            self.mydb.commit()
        except mysql.connector.Error as err:
            self.error_message = f"Error removing ticket: {err}"
            self.mydb.rollback() # alle wijzigingen terughalen, zodat je de database niet vernietigd

    def remove_user_from_ticket(self, UserID, TicketID):
        try: 
            sql = "DELETE FROM userticket WHERE TicketID = %s AND UserID = %s"
            val = (TicketID, UserID)
            self.mycursor.execute(sql,val)
            self.mydb.commit()
        except mysql.connector.Error as err:
            self.error_message = f"Error removing user from ticket: {err}"
    
    
    def update_user_rights(self, UserID, RightID):
        try: 
            sql = "UPDATE users SET RightID = %s WHERE userID = %s"
            val = (RightID, UserID)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
        except mysql.connector.Error as err:
            self.error_message = f"Error updating user rights: {err}"

    def update_user_username(self, UserID, Username):
        try:
            sql = "UPDATE users SET Username = %s WHERE userID = %s"
            val = (Username, UserID)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
        except mysql.connector.Error as err:
            self.error_message = f"Error updating username: {err}"

    def update_user_password(self, UserID, Password):
        try:
            sql = "UPDATE users SET password = %s WHERE userID = %s"
            val = (Password, UserID)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
        except mysql.connector.Error as err:
            self.error_message = f"Error updating password: {err}"

    def remove_user(self, UserID):
        try:
            sql_userticket = "DELETE FROM userticket WHERE UserID = %s"
            val_userticket = (UserID,)
            self.mycursor.execute(sql_userticket, val_userticket)

            sql_users = "DELETE FROM users WHERE UserID = %s"
            val_users = (UserID,)
            self.mycursor.execute(sql_users, val_users)

            self.mydb.commit()
        except mysql.connector.Error as err:
            self.error_message = f"Error removing user: {err}"

    def update_ticket_hours(self, TicketID, Hours):
        try:
            sql = "UPDATE tickets SET Hours = %s WHERE TicketID = %s"
            val = (Hours, TicketID)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
        except mysql.connector.Error as err:
            self.error_message = f"Error updating hours: {err}"


    def check_username_password(self, Username, Password):
        try:
            Username = Username.lower()
            sql = "SELECT Password FROM users WHERE Username = %s"
            val = (Username, )
            self.mycursor.execute(sql, val)
            result = self.mycursor.fetchone() # een rij

            if result:
                stored_password = result[0]

                if stored_password == Password:
                    return True
                else:
                    return False
            else:
                return False
        except mysql.connector.Error as err:
            self.error_message = f"Error checking username_password: {err}"



        # Maak een instantie van de DbHandler
db_handler = DbHandler()


# toevoegen nieuwe user 
# hier moet je dingen kunnen invoegen die uit de gebruikers formulier komen ("Username", "password", "rights")
# db_handler.add_user("newusername", "newpassword123", 1)  # Voeg nieuwe gebruiker toe

# toevoegen nieuw ticket
#hier moet je dingen kunnen invoegen die uit het tickets formulier komen ("title", "description", "hours", "status")
#db_handler.add_ticket("testen applicatie", "wij gaan de applicatie testen", 1, 3)


# updaten ticket status
# vul hier de (ticketID en de statusID) in dus als je bijvoorbeeld wilt wijzigen van 'backlog' naar 'ready'
# db_handler.update_ticket_status(4,2)

# updaten van user status
# vul hier de (UserID en de RightID) in dus als je bijvoorbeeld wilt wijzigen van 1='Geen rechten' naar 6='Alle tickets editen en verwijderen'
# db_handler.update_user_rights(2,6)


# toevoegen van user to a ticket
# vul hier de (UserID en de TicketID) in dus als je bijvoorbeeld thijs wilt toevoegen aan het ticket 'code schrijven flask' vul in (2,2)
#db_handler.add_user_to_ticket(2,3)


# update de ticket titel
# vul hier de (title en de TicketID) in dus als je bijvoorbeeld de titel overleg naar overleggen wilt veranderen van TicketID1 vul je in("overleggen",1)
# db_handler.update_ticket_title("overleggen",1)

# update de ticket description
# db_handler.update_ticket_description("code schrijven flask over database", 2)


# verwijder je ticket
# vul je 2 in dan verwijder je alle tickets met een ticketID=2 uit zowel de tickets tabel als de userticket tabel
# db_handler.remove_ticket(2)

# verwijder een user gekoppeld aan een ticket
# (UserID, TicketID)
#db_handler.remove_user_from_ticket(2,3)

# Haal de namen op en druk de eerste drie af
names = db_handler.read_names()
for user in names[:3]:
    print("UserID:", user[0], "Username:", user[1], "Password", user[2], "rightID", user[3])



# # haal data op die nodig is voor op de tickets
# tickets_data = db_handler.get_tickets_data()
# for ticket_data in tickets_data:
#     print("Username:", ticket_data[0], "Right Name:", ticket_data[1], "Ticket Title:", ticket_data[2], "Description:", ticket_data[3], "Hours:", ticket_data[4], "Status:", ticket_data[5])










