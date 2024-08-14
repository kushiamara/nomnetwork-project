
-- Initialize Database
DROP DATABASE IF EXISTS nomnetwork;
CREATE DATABASE IF NOT EXISTS nomnetwork;
USE nomnetwork;




-- Tables
CREATE TABLE IF NOT EXISTS Users (
 userId INTEGER PRIMARY KEY AUTO_INCREMENT,
 username VARCHAR(255) UNIQUE NOT NULL,
 firstName VARCHAR(255) NOT NULL,
 lastName VARCHAR(255) NOT NULL,
 email VARCHAR(255) UNIQUE NOT NULL,
 streetAddress VARCHAR(255),
 city VARCHAR(50),
 state VARCHAR(25),
 zipcode CHAR(5),
 dob DATE,
 createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
 updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
                   ON UPDATE CURRENT_TIMESTAMP
);




CREATE TABLE IF NOT EXISTS Followers (
 followerId INTEGER, -- fans viewing a user's posts
 followeeId INTEGER, -- the user being followed
 timeFollowed DATETIME DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (followerId, followeeId),
 FOREIGN KEY (followerId) REFERENCES Users(userId) ON UPDATE CASCADE ON DELETE CASCADE,
 FOREIGN KEY (followeeId) REFERENCES Users(userId) ON UPDATE CASCADE ON DELETE CASCADE
);




CREATE TABLE IF NOT EXISTS Restaurants (
 restId INTEGER PRIMARY KEY AUTO_INCREMENT,
 restName VARCHAR(255) NOT NULL,
 bio TEXT,
 streetAddress VARCHAR(100),
 city VARCHAR(25),
 state VARCHAR(50),
 zipcode CHAR(5),
 websiteLink VARCHAR(255),
 cName VARCHAR(100),
 cEmail VARCHAR(255),
 cPhoneNumber VARCHAR(10),
 photo VARCHAR(2000),
 createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
 updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
                   ON UPDATE CURRENT_TIMESTAMP
);




CREATE TABLE IF NOT EXISTS RestaurantProfileViews (
 restId INTEGER,
 viewerId INTEGER,
 timeViewed DATETIME DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY(restId, viewerId, timeViewed),
 FOREIGN KEY(restId) REFERENCES Restaurants(restId) ON UPDATE CASCADE ON DELETE CASCADE,
 FOREIGN KEY (viewerId) REFERENCES Users(userId) ON UPDATE CASCADE
);




CREATE TABLE IF NOT EXISTS Hours (
 restId INTEGER,
 dayOfWeek VARCHAR(15),
 openTime TIME,
 closeTime TIME,
 lastUpdated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY(restId, dayOfWeek),
 FOREIGN KEY (restId) REFERENCES Restaurants(restId) ON UPDATE CASCADE ON DELETE CASCADE
);




CREATE TABLE IF NOT EXISTS MenuItems (
 itemName VARCHAR(100),
 restId INTEGER,
 price DECIMAL(7,2),
 calories INTEGER,
 photo VARCHAR(2000),
 createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
 lastUpdated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY(itemName, restId),
 FOREIGN KEY(restId) REFERENCES Restaurants(restId) ON UPDATE CASCADE ON DELETE CASCADE
);




CREATE TABLE IF NOT EXISTS Reviews (
 reviewId INTEGER PRIMARY KEY AUTO_INCREMENT,
 rating DECIMAL(2, 1) UNSIGNED NOT NULL,
 text TEXT,
 authorId INTEGER,
 restId INTEGER,
 timePosted DATETIME DEFAULT CURRENT_TIMESTAMP,
 updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
                   ON UPDATE CURRENT_TIMESTAMP,
 FOREIGN KEY (authorId) REFERENCES Users(userId) ON UPDATE CASCADE ON DELETE SET NULL,
 FOREIGN KEY (restId) REFERENCES Restaurants(restId) ON UPDATE CASCADE
);




CREATE TABLE IF NOT EXISTS ReviewPhotos (
 photoId INTEGER PRIMARY KEY AUTO_INCREMENT,
 reviewId INTEGER NOT NULL,
 photo VARCHAR(2000),
 FOREIGN KEY (reviewId) REFERENCES Reviews(reviewId) ON UPDATE CASCADE ON DELETE CASCADE
);




CREATE TABLE IF NOT EXISTS ReviewViews (
 reviewId INTEGER NOT NULL,
 viewerId INTEGER,
 timeViewed DATETIME DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (reviewId, viewerId, timeViewed),
 FOREIGN KEY (reviewId) REFERENCES Reviews(reviewId) ON UPDATE CASCADE ON DELETE CASCADE,
 FOREIGN KEY (viewerId) REFERENCES Users(userId) ON UPDATE CASCADE
);




CREATE TABLE IF NOT EXISTS Comments (
 commentId INTEGER PRIMARY KEY AUTO_INCREMENT,
 text VARCHAR(255) NOT NULL,
 reviewId INTEGER NOT NULL,
 commenterId INTEGER ,
 timePosted DATETIME DEFAULT CURRENT_TIMESTAMP,
 updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
                   ON UPDATE CURRENT_TIMESTAMP,
 FOREIGN KEY (reviewId) REFERENCES Reviews(reviewId) ON UPDATE CASCADE ON DELETE CASCADE,
 FOREIGN KEY (commenterId) REFERENCES Users(userId) ON UPDATE CASCADE ON DELETE SET NULL
);




CREATE TABLE IF NOT EXISTS Tags (
 tagId INTEGER AUTO_INCREMENT PRIMARY KEY,
 tagName VARCHAR(255) UNIQUE NOT NULL,
 createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
);




CREATE TABLE IF NOT EXISTS ReviewTags (
 tagId INTEGER NOT NULL,
 reviewId INTEGER NOT NULL,
 PRIMARY KEY (tagId, reviewId),
 FOREIGN KEY (tagId) REFERENCES Tags(tagId) ON UPDATE CASCADE ON DELETE CASCADE,
 FOREIGN KEY (reviewId) REFERENCES  Reviews(reviewId) ON UPDATE CASCADE ON DELETE CASCADE
);




CREATE TABLE IF NOT EXISTS RestaurantTags (
 tagId INTEGER,
 restId INTEGER,
 createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (tagId, restId),
 FOREIGN KEY (tagId) REFERENCES Tags(tagId) ON UPDATE CASCADE ON DELETE CASCADE,
 FOREIGN KEY (restId) REFERENCES Restaurants(restID) ON UPDATE CASCADE ON DELETE CASCADE
);




CREATE TABLE IF NOT EXISTS Promotions (
 name VARCHAR(255),
 description TEXT,
 restId INTEGER,
 active BOOL NOT NULL DEFAULT TRUE,
 createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
 lastUpdated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY (restId, name),
 FOREIGN KEY (restId) REFERENCES Restaurants(restID) ON UPDATE CASCADE ON DELETE CASCADE
);


-- Inserting Sample Data
INSERT INTO Users (username, firstName, lastName, email, streetAddress, city, state, zipcode, dob)
VALUES ('henryButler','Henry', 'Butler', 'henry@butler.com', '123 Park Dr', 'Brooklyn', 'NY', '11238', '2004-05-03'),
   ('janeDoe', 'Jane', 'Doe', 'janedoe@gmail.com', '7 Main St', 'Denver', 'CO', '72643', '1987-06-12'),
   ('thePresident', 'Joe', 'Biden', 'joeBiden@whitehouse.gov', '1800 Pennsylvania Ave', 'Washington', 'DC', '37188', '1942-11-20');


INSERT INTO Followers (followerId, followeeId) VALUES (1, 3), (2,3), (3, 1), (1,2);


INSERT INTO Restaurants (restName, bio, streetAddress, city, state, zipcode, websiteLink, cEmail, cName, cPhoneNumber, photo)
VALUES ('Piccolo Forno','The Piccolo Forno, nestled in Boston’s North End, brings a slice of Italy to the heart of the city. Since our founding, we’ve been serving authentic Italian dishes crafted from cherished family recipes and the finest ingredients. Our menu features hand-rolled pastas, wood-fired pizzas, and classic Italian entrees, all in a cozy, rustic setting. Whether you are here for a romantic dinner or a family celebration, our warm, attentive staff ensures a memorable dining experience. At Piccolo Forno, we celebrate the sweet life with every meal. Buon appetito!',
   '355 Hanover St', 'Boston', 'MA', '02113', 'piccolo-forno.com', 'marco@piccoloforno.com', 'Marco Fontenot', '4126220111', 'https://images.app.goo.gl/dGnrLsfxA3h7sKGi8'),
   ('Lolita Back Bay','A Mexican outlaw meets Mexican royalty within dimly lit rooms brimming with gothic sophistication, setting the mood at Lolita Cocina & Tequila Bar in Boston’s Back Bay and Fort Point neighborhoods. Spanish-inspired décor brings the vision to life with signature design elements including hand-painted wall murals, vintage wrought iron and Mexican calaveras; all of which embody Lolita’s rebellious spirit.'
   ,'271 Dartmouth St', 'Boston', 'MA', '02116', 'lolitamexican.com', 'lolitamanagement@gmail.com', 'Victor Rodrigues', '6173695609', 'https://images.app.goo.gl/2rc2faoHJg3yxFkC6'),
   ('Trattoria Il Panino','Ample, traditional Italian meals in intimate indoor and spacious outdoor spaces.'
   ,'280 Hanover St', 'Boston', 'MA', '02113', 'trattoriailpanino.com', 'carlos@trattoria.com', 'Carlos Pasta', '6177201336', 'https://images.app.goo.gl/tkmUrWmi5nicyhfS9');


INSERT INTO RestaurantProfileViews (restID, viewerID) VALUES (2, 3), (1,2), (3, 2);


INSERT INTO Hours (restID, dayOfWeek, openTime, closeTime)
VALUES (1,'Monday', '10:00:00', '22:30:00'), (1,'Tuesday', '10:00:00', '22:30:00'),(1,'Thursday', '10:00:00', '22:30:00'),(1,'Friday', '10:00:00', '23:30:00'),(1,'Saturday', '10:00:00', '23:30:00'),(1,'Sunday', '12:00:00', '22:00:00'),
   (2,'Saturday', '11:00:00', '23:45:00'), (2,'Sunday', '09:00:00', '23:45:00');


INSERT INTO MenuItems (itemName, restID, price, calories, photo)
VALUES ('Margherita Pizza',1, 16.00, 800, 'https://images.app.goo.gl/GNh3CAewYvQ8rRKcA'),
      ('Cheese and Spinach Ravioli', 1, 25.00, 700, 'https://images.app.goo.gl/tXbRRqD7kznx5id59'),
      ('Penne Alla Vodka', 1, 22.00, 675, 'https://images.app.goo.gl/bkZ6cFBGZEiiGRUh9'),
      ('Steak Quesadillas', 2, 34, 480, 'https://images.app.goo.gl/NECD4rauM5pKiPp6A');


INSERT INTO Reviews (rating, text, authorId, restId)
VALUES (4.2, 'great food! really nice atmosphere and service.', 2, 1),
     (5, 'Best meal I ever had', 3, 2),
     (2.3, 'Pretty mid tbh', 2, 3);


INSERT INTO ReviewPhotos (reviewId, photo)
VALUES (2, 'https://www.google.com/imgres?q=biden%20falling%20down%20stairs&imgurl=https%3A%2F%2Fs.abcnews.com%2Fimages%2FPolitics%2Fbiden-stumble-03-ht-jt-210319_1616181267869_hpMain_2_16x9_1600.jpg&imgrefurl=https%3A%2F%2Fabcnews.go.com%2FPolitics%2Fbiden-fine-tripping-times-jogging-steps-air-force%2Fstory%3Fid%3D76561006&docid=J2IeWSq45PD2cM&tbnid=JcA4mBYU2knQBM&vet=12ahUKEwi82ueEpuaHAxWBl4kEHUp0OXIQM3oECBgQAA..i&w=1600&h=900&hcb=2&ved=2ahUKEwi82ueEpuaHAxWBl4kEHUp0OXIQM3oECBgQAA'),
      (1, 'https://www.google.com/url?sa=i&url=https%3A%2F%2Forders.co%2Fblog%2Fitalian-restaurant-design%2F&psig=AOvVaw3Gb1nN_BE_JpZfXvJcemC8&ust=1723237754104000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCLDagYen5ocDFQAAAAAdAAAAABAE');


INSERT INTO ReviewViews (reviewId, viewerId) VALUES (2, 1), (2, 2), (3, 3);


INSERT INTO Comments (text, reviewID, commenterID)
VALUES ('Very helpful Joe, thank you.', 2, 1), ('How dare you', 3, 3);


INSERT INTO Tags (tagName) VALUES ('Vegetarian'), ('Vegan'), ('Gluten-Free'), ('Italian'), ('Chinese'), ('Mexican'), ('Casual');


INSERT INTO ReviewTags (tagId, reviewId) VALUES (1, 1), (6, 2), (7, 2);


INSERT INTO RestaurantTags (tagId, restId) VALUES (1,1), (2,1), (4,1), (7,1), (6,2), (4,3), (1,3);


INSERT INTO Promotions (description, active,  name, restID)
VALUES ('Limited offer! Get two food items for the price of 1!', TRUE, 'Buy 2 for price of 1', 1),
      ('Come enjoy appetizers for under $5!', TRUE, 'Happy Hour', 2);

