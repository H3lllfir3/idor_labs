give me a simple fastapi app with  this endopoints:
1. login and logout endpoint the authentication is session based. and the default user creadential is username: "alex" and password: "alex1234"
2. index page shows some blog post, also anonymouse user can see this posts. it just a static html page.
3. profile endpoint to show user data, this endpoint uses id to show user profile data it consist of this 
field id,username,email,phone,address the database should be fake and the default user has this data: {
        "id": 1,
        "username": "alex", 
        "email": "alex@email.com",
        "phone": "001-427-216-6063x8915",
        "address": "18647 Travis Unions\nNguyenhaven, ND 55081"
    } but for other user use fake library to generate randomly data like this {
        "id": 2,
        "username": fake.user().split(" ")[0], 
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": fake.address()
    }
also give me html template for each endpoint