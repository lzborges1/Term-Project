# Term-Project
This repository is for our team term project

# Team Names:
Lila Borges and Ashley Battiata

# Project Proposal
## The Big Idea: What is the main idea of your project? What topics will you explore and what will you accomplish? Describe your minimum viable product (MVP) and your stretch goal. 

For this project we would like to develop a website that provides real time traffic analysis, specifically heavy traffic indicators on Interstate 95 (I-95). The heavy traffic indicators will include average vehicle speed, traffic volume, traffic density, accidents and roadwork, and peak traffic periods. Upon accessing the website, the user will be presented with a map showing the current traffic condition on I-95. The web application will not allow the user to input their current location and final location. This site will only be used for users who know their commute requires them to use Interstate I-95.  

We will be exploring the following topics: real-time data handling where we will learn how to handle and process real-time traffic data, APi integration, web development with python where we will be using frameworks like Flask and Django to build the web application and data visualization.  

The minimal viable product is a simple and intuitive interface that displays the current traffic condition on I-95. The interface will include basic data processing to identify heavy traffic indicators such as average speed and traffic density. Lastly it will use a backend server set up using Flask to handle web requests and serve the front-end content.  

The stretch goal will include adding one to two more interstates. If we can do this, we can design the website to allow for user customization meaning they can save their favorite routes or receive alerts. Ideally, we can integrate with other data sources to provide more comprehensive traffic reports such as weather conditions, construction work and special events. Lastly, it would have enhanced data visualizations and interactive maps that allow users to zoom in on specific section of the interstate. 

## Learning Objectives: Since this is a team project, you may want to articulate both shared and individual learning goals. 

Given that this project is a collaborative effort between Ashley and myself, we wanted to delve into a subject that hits close to home for both of us. Our primary focus revolves around the evaluation of traffic dynamics on Interstate-95, which conveniently runs through our own localities. This allows us to explore the nuances of traffic flow within our respective hometowns. Some common learning goals are to see what the cause of traffic flow may be, what times traffic may be the heaviest, and to also build a web application for users to see how bad traffic may be if they live near I-95. Most of our goals align in trying to make geographical applications easier to use. We’ve noticed that current I-95 interface applications show current heavy traffic but as the user you’d have to decide if you want to take it. Our vision is to enhance the experience of navigating heavy traffic by crafting a web application that caters to the specific needs of commuters who heavily rely on I-95 for their daily work commutes and trips back home.  

## Implementation Plan: This part may be somewhat ambiguous initially. You might have identified a library or a framework that you believe would be helpful for your project at this early stage. If you're uncertain about executing your project plan, provide a rough plan describing how you'll investigate this information further. 

The first part of the project involves researching APIs or government data feeds that provide real time traffic information for I-95. Then we must select a python web framework, we are thinking of using Flask or Django. This is the Planning phase. Moving forward to the development of the application. On the backend we must create the code for the API integration, implement functions to process the received data into a format fitted for identifying heavy traffic indicators. If we decide to provide personalized user experiences on the website, we will need to code a database integration. Then we need to do the front-end development. Create HTML pages to define the structure of our web UI. After we develop, we need to test our application.  

## Project Schedule: You have 6 weeks (roughly) to finish the project. Draft a general timeline for your project. Depending on your project, you might be able to provide a detailed schedule or only an overview. Preparation of a longer project is also accompanied by present uncertainty, and this schedule will likely require revisions as the project progresses. 

Creating a web application will be a learning experience for both me and Lila. We explained our project topic and objectives to ChatGPT by feeding it our response to question one then we asked it to make our Project Schedule. We are unfamiliar with some of the aspects of this project, therefore it was difficult to go in depth. ChatGPT was great assistance.  

**Week 1: Backend Development and API Integration **

Day 1: Project Initialization  

Set up the project structure. 

Initialize the Flask app and create a repository on GitHub. 

Day 2: API Research 

Identify and evaluate APIs for real-time traffic data. 

Register for API keys and understand rate limits and data schemas. 

Day 3: API Integration 

Write Python scripts to connect to the traffic APIs. 

Develop functions to fetch real-time data such as average speed, traffic volume, and incidents. 

Day 4: Data Processing 

Implement backend logic to process API data and identify heavy traffic indicators. 

Begin writing backend routes to serve processed data to the frontend. 

Day 5: Backend Functional Testing 

Test API integration and data processing logic. 

Ensure the backend can serve data correctly to the frontend. 

**Week 2: Frontend Development and Data Visualization **

Day 1: Frontend Setup 

Create the basic frontend structure using HTML/CSS. 

Set up a template engine with Flask. 

Day 2: UI Design 

Design the layout of the web application, focusing on the map and traffic indicator displays. 

Start implementing the design using chosen frontend technologies. 

Day 3: Map Integration 

Integrate a map API (like Google Maps) into the frontend. 

Ensure that the map can display real-time traffic data. 

Day 4: Data Visualization 

Implement visualization of traffic data on the map. 

Develop UI components to represent different traffic indicators. 

Day 5: Frontend Functional Testing 

Test the interactivity of the map and the display of real-time data. 

Ensure the UI is responsive and works on multiple devices and screen sizes. 

**Week 3: Intermediate Features and User Experience **

Day 1: User Interface Enhancement 

Refine the user interface based on the MVP requirements. 

Implement additional UI features like a legend for traffic indicators. 

Day 2: Intermediate Backend Features 

Develop and test intermediate features such as route-specific traffic conditions. 

Expand backend capabilities to handle additional interstates if time allows. 

Day 3: User Experience Improvements 

Conduct evaluations of the interface. 

Iterate on the UI/UX to ensure a seamless user journey. 

Day 4: Performance Optimization 

Optimize backend performance for faster API response times. 

Ensure frontend performance is optimized for real-time data updates. 

Day 5: Soft User Testing 

Conduct informal user testing sessions to gather feedback. 

Begin incorporating user feedback into the development process. 

**Week 4: Additional Features and Stretch Goals **

Day 1: Stretch Goal Assessment

Review progress towards MVP and assess the viability of stretch goals. 

Prioritize stretch goal features based on remaining time and resources. 

Day 2-3: Additional Features Development 

Start implementing additional features such as saving favorite routes (if MVP is complete). 

Ensure backend can handle new features without affecting performance. 

Day 4: Integration Testing 

Conduct integration tests for any new features added. 

Validate that all parts of the system work together harmoniously. 

Day 5: User Experience Refinement 

Refine user experience elements based on testing and feedback. 

Finalize the UI/UX in preparation for final testing and deployment. 

## Collaboration Plan: How will you collaborate with your teammates on this project? Will you divide tasks and then incorporate them separately? Will you undertake a comprehensive pair program? Explain how you'll ensure effective team collaboration. This may also entail information on any software development methodologies you anticipate using (e.g. agile development). Be sure to clarify why you've picked this specific organizational structure. 

Ashley and I plan to meet-up weekly to work on the project as well as work on our code. We plan to work on finding the data individually but working on the actual code together to make sure we’re on the same page. In the beginning we’ll need to meet up more to solidify our plan as well as make sure we start off on the same foot to make the process of completing this project easier. I think once we start to get the hang of things, we might meet up less since we’ll know what we each need to do. For now, we plan on working on the project together but over time we’ll be able to split up the work once we’ve settled into what we want to do. We’ll have effective team collaboration by communicating with one another on a regular basis (so texting and emailing). We’ve already established a good foundation with communication between one another.  

## Risks and Limitations: What do you believe is the most significant threat to this project's success? 

We definitely have some risks, mostly related to real-time data. Our application's core functionality depends on real-time data, so if our website has frequent downtime, if our data source is unreliable, or if our website provides inaccurate information. It could be due to changes in the API or if there was a discontinuation with the service. There could also be legal and privacy concerns as the website could lead to legal challenges. We also don’t have a lot of time for this project so the complexity of it will not be as advanced as other applications. Retaining our customers and ensuring our application runs smoothly is another possible risk or limitation. 

## Additional Course Content: What topics do you believe will be beneficial to your project? 

The topics we believe would be beneficial API’s, Functions, Web Design, Dictionaries. 