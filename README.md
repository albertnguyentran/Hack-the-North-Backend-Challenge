# Hack the North Backend Challenge

## Overview

This project sets up the database and the four endpoints using Flask, GraphQL and SQLite as per the requirements. I chose this stack because I have the least amount of experience with it as opposed to the other options, so I want to show the team I can learn quickly and build something new :)

## Structure

1. Database:
    1. setupDatabase.py - creates the tables (users, skills)
    2. insertData.py - inserts the data from the JSON file into the tables
    3. database.py - creates an instance of the database
    4. models.py - define models for each table

2. Endpoints (main.py):
    1. Queries:
        1. All users
        2. User By ID
        3. Users by Skill Range
    2. Mutations:
        1. Update User By ID
    
## Design Decisions

* Seperated the skills of each user into a skills table with the same user_id
* Identified user by user_id for the mutation endpoint
* The Users by Skill Range endpoint returns the user(s) themselves and not just their name and frequency of skills

## Demo

**Database Demo:**

https://github.com/albertnguyentran/Hack-the-North-Backend-Challenge/assets/79335098/7138a848-4d41-4503-8245-ba5e8440ad4a

**All Users Endpoint:**

https://github.com/albertnguyentran/Hack-the-North-Backend-Challenge/assets/79335098/870e997c-f33c-4f8b-84e4-0446e60e38e5

**User By ID Endpoint:**

https://github.com/albertnguyentran/Hack-the-North-Backend-Challenge/assets/79335098/1006969f-36b3-4011-bea3-6745d592f62f

**Users By Skill Range Endpoint:**

https://github.com/albertnguyentran/Hack-the-North-Backend-Challenge/assets/79335098/2c749798-eaab-478c-a051-a64e58ff1487


## Next Steps and Future Considerations

1. Unit testing (working on it rn)
2. Given data about the users location, write an endpoint that determines how much reimbursement they are eligible for
3. Given data about the users workshop preferences, determine scheduling to avoid the least amount of conflictions



