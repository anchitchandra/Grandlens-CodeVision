# Grandlens-CodeVision
*#Blogging web application. The website is made with the help of PYTHON FLASK MODULE were backend is done with the flask and the front end with HTML-CSS with firebase as database. 
**#OVERVIEW & highlights:**
In this web site user can create there account once you ave created an account you can post images and write about them, you can also like images uploaded by other users. The uploaded blog will be featured on the feed page of the website.
The key feature of this website is that it extracts meta-data stored in the image with the help of that you can tell weather the image is clicked by the user or downloaded from internet even edited or not. This website was made specially for photographic contests, once user uploaded there image on website the image is stored as it is without changing even a single pixel and at the same time meta-data is also extracted from the image. Each account is allowed to upload only image if the user reuploads the image the previous image will be replaced by the current one. Website also have a custom session which protects website ad it content from anonymous users only verified users to view and post on the website feed. Insted of using default session from flask using custom session helps more efficiently in keeping track of user.

**#DETAILED VIEW:**
Create Acc : Accout creation will be done by GOOGLE FIREBASE AUTH, after creating account a verifying mail will be sent to the user email, in order to login the website you have to first clear the verification process.

*Login : After login you'll be redirected to the home page of the website where you can find your uploaded image and images uploaded by other users also. You'l get three buttons on Home page
 	"HOME", "BLOG", "LOGOUT".
*BLOG page: Here you can upload your Image and write description. The data is pushed in GOOGLE FIREBASE REALTIME DATABASE.
*LOGOUT: This button will helps you to pop out from the current session of the website.
![Screenshot 2021-09-06 185544](https://user-images.githubusercontent.com/66684814/132225113-8958a293-b5a4-49ae-b6ac-612a3f2eb021.png)

![Screenshot 2021-09-06 185710](https://user-images.githubusercontent.com/66684814/132225102-b821b304-665b-4178-a706-8e8ba84fb4bd.png)
![Screenshot 2021-09-06 190007](https://user-images.githubusercontent.com/66684814/132225082-7593acaf-a6d4-4ef4-948f-5f028c988f22.png)

![Screenshot 2021-09-06 190033](https://user-images.githubusercontent.com/66684814/132225120-a6b02164-aa37-4902-a67d-55f334487081.png)
![Screenshot 2021-09-06 190104](https://user-images.githubusercontent.com/66684814/132225125-7dbfa88d-d9c2-4072-9052-3277c08c0448.png)


