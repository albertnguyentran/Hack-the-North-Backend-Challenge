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

## Tables

**Table 1: Skills**

| id (integer, auto-increment) | user_id (integer, foreign key) | skill (string) | rating (integer) |
| --------------------------- | ------------------------------ | -------------- | ---------------- |
| 1                           | 1                              | swift         | 4                |
| 2                           | 1                              | OpenCV        | 1                |
| ...                           | ...                           | ...        | ...              |

**Table 2: Users**

| id (integer, auto-increment) | name (string)      | company (string)         | email (string, unique)   | phone (string)  |
| ---------------------------- | ------------------ | ------------------------ | ------------------------ | --------------- |
| 1                            | Breanna Dillon     | Jacksson Ltd             | lorettabrown@example.net | +1-924-116-7963 |
| 2                            | Kimberly Wilkinson | Moon, Mendoza and Carter | frederickkly@example.org | (186)579-0542   |
| ...                          | ...                | ...                      | ...                      | ...             |

## Design Decisions

* Seperated the skills of each user into a skills table with the same user_id
* Identified user by user_id for the mutation endpoint
* The Users by Skill Range endpoint returns the user(s) themselves and not just their name and frequency of skills

## Demo

**1. Database Setup:**

https://github.com/albertnguyentran/Hack-the-North-Backend-Challenge/assets/79335098/7138a848-4d41-4503-8245-ba5e8440ad4a

**2. All Users Endpoint:**

```graphql
query {
  allUsers {
    id
    name
    company
    email
    phone
    skills {
      skill
      rating
    }
  }
}
```

https://github.com/albertnguyentran/Hack-the-North-Backend-Challenge/assets/79335098/870e997c-f33c-4f8b-84e4-0446e60e38e5

**3. User By ID Endpoint:**

```graphql
query {
  userById(id: 1) {
    id
    name
    company
    email
    phone
    skills {
      skill
      rating
    }
  }
}
```

https://github.com/albertnguyentran/Hack-the-North-Backend-Challenge/assets/79335098/1006969f-36b3-4011-bea3-6745d592f62f

**4. Update User Endpoint:**

```graphql
mutation {
  updateUser(inputData: {
    id: 2,
    name: "Updated Name",
    skills: [
      { skill: "New Skill 1", rating: 5 },
      { skill: "New Skill 2", rating: 3 }
    ]
  }) {
    user {
      id
      name
      skills {
        skill
        rating
      }
    }
  }
}
```

https://github.com/albertnguyentran/Hack-the-North-Backend-Challenge/assets/79335098/19335e30-75c9-4256-b424-af2e65e6ff53

**5. Users By Skill Range Endpoint:**

```graphql
query {
  usersWithSkillsRange(minSkills:2, maxSkills: 5) {
    id
    name
    company
    email
    skills {
      skill
      rating
    }
  }
}

```

https://github.com/albertnguyentran/Hack-the-North-Backend-Challenge/assets/79335098/2c749798-eaab-478c-a051-a64e58ff1487


## Next Steps and Future Considerations

1. Unit testing (working on it rn)
2. Given data about the users location, write an endpoint that determines how much reimbursement they are eligible for
3. Given data about the users workshop preferences, determine scheduling to avoid the least amount of conflictions



