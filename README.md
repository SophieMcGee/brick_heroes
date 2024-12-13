# **_Brick Heroes - Project Portfolio 5_**

INSERT INTRO AND LINK TO LIVE SITE HERE

# Contents

* [**Website Objectives**](#website-objectives)
* [**Agile Methodology**](#agile-methodology)
  * [**Key Agile Practices Utilised**](#key-agile-practices-utilised)
* [**User Experience (UX)**](#user-experience-ux)
  * [**Client Background and Goals**](#client-background-and-goals)
  * [**Target Audience**](#target-audience)
  * [**User Stories**](#user-stories-1)
* [**Market Research**](#market-research)
* [**Design**](#design)
  * [**Planning and Development**](#planning-and-development)
  * [**Colour Scheme and Typography**](#colour-scheme-and-typography)
* [**Data Model**](#data-model)
* [**General Features**](#general-features)
* [**Page-Specific Features**](#page-specific-features)
  * [**Home Page Features**](#home-page-features)
  * [**Event Management Features**](#event-management-features)
  * [**User Account Features**](#user-account-features)
  * [**404 Page**](#404-page)
  * [**Authentication**](#authentication)
  * [**Future Features**](#future-features)
* [**Technologies Used**](#technologies-used)
* [**Deployment**](#deployment)
* [**Testing**](#testing)
* [**Bugs**](#bugs)
* [**Credits**](#credits)
* [**Acknowledgements**](#acknowledgements)

# Website Objectives

The Brick Heroes website is designed to provide a comprehensive platform for users to explore, borrow, and purchase Lego sets through a subscription-based model. The primary goal is to create an engaging, user-friendly space that empowers builders of all ages to access a wide variety of Lego sets affordably, while also promoting sustainability through the reuse of sets. The site integrates borrowing functionality, e-commerce options, and subscription management, ensuring a seamless experience for users.

Additionally, Brick Heroes aims to foster a creative community of Lego enthusiasts by offering features like a blog with building tips, user galleries for sharing creations, and the ability to leave reviews and feedback on borrowed sets. The website's design reflects a vibrant, comic-book-inspired theme to make the browsing and interaction experience fun and memorable.


**Key objectives:**
1. **Subscription Management**
  - Enable users to view, select, and manage subscription plans, including monthly and annual options, with clear pricing and benefits.
  - Provide flexible management tools for upgrading, downgrading, or cancelling subscriptions.

2. **Borrowing and Returning Sets**
  - Offer a seamless borrowing system where users can browse and filter sets by theme, difficulty, and availability.
  - Allow users to track borrowed sets, return them easily, and join waitlists for unavailable items.

3. **E-Commerce Functionality**
  - Include the option for users to purchase Lego sets outright, along with other products like gift cards.
  - Provide a secure checkout process for transactions and gift card redemption.

4. **Creative Engagement**
  - Foster community interaction through features like user reviews, ratings, and a gallery for sharing builds.
  - Maintain an inspiring blog with tips, set reviews, and Lego news.

5. **Accessibility and Usability**
  - Ensure the site is fully responsive and accessible, providing a smooth experience across devices, including mobile, tablet, and desktop.
  - Use an intuitive design and navigation structure to simplify browsing and borrowing for all users.

6. **Sustainability Focus**
  - Promote eco-friendly practices by encouraging the reuse of Lego sets, reducing waste, and minimising the environmental impact of toy consumption.

7. **Administrator Tools**
  - Provide a robust admin interface for managing Lego sets, monitoring user activity, and moderating reviews and gallery submissions.
  - Include analytics tools to track subscriptions, borrowing trends, and overall site engagement.

8. **Notifications and Feedback**
  - Keep users informed with timely notifications for due dates, waitlist availability, and subscription renewals.
  - Encourage user feedback to continuously improve the service and offerings.

By focusing on these objectives, Brick Heroes aims to become the go-to platform for affordable and creative Lego set access while building a supportive and enthusiastic community of builders.

[Back to top](<#contents>)

# Agile Methodology

## Agile Methodology

Throughout the development of the Brick Heroes platform, Agile methodology was implemented to ensure the project was completed efficiently while remaining flexible to evolving requirements. This iterative approach emphasized incremental delivery, continuous improvement, and alignment with user needs, allowing the project to adapt as feedback was incorporated. Agile principles helped manage the project's scope, prioritise key features, and maintain a high standard of quality.

### Key Agile Practices Utilised:

1. **Sprint Planning and Milestones**

The development process was broken into multiple milestones, each representing a major feature or section of the site (e.g., User Authentication, Subscription Management, Borrowing and Returning Lego Sets).

  - Each milestone was treated as a sprint, with specific goals and a clear timeline for delivery.
  - Deadlines were set for each sprint but remained flexible, allowing adjustments to address high-priority features first or respond to feedback.
  - Examples of milestones included:
      - Setting up the user authentication system.
      - Developing the borrowing and returning workflows.
      - Implementing e-commerce functionality for gift cards and set purchases.

This iterative structure ensured steady progress while maintaining the flexibility to pivot when necessary.

2. **User Stories**

User stories were at the heart of the development process, capturing features and functionality from the perspective of different user types (e.g., subscribers, admins, and visitors).

  - Each user story was written to reflect specific user goals, helping to focus on delivering value.
  - Prioritisation followed the MoSCoW framework:
      - Must Have: Core functionality like account registration, borrowing Lego sets, and subscription management.
      - Should Have: Features enhancing usability, such as filtering Lego sets by theme or difficulty.
      - Could Have: Community features like sharing Lego creations or commenting on blog posts.
  - User stories provided clear acceptance criteria to guide development and testing, ensuring that each feature met user expectations.

3. **GitHub Project Board**

A dedicated GitHub Projects board was created to organise and track tasks, user stories, and features.

  - The board was divided into columns, such as:
      - Backlog: Features or tasks awaiting prioritisation.
      - In Progress: Current tasks under development.
      - Testing: Completed tasks undergoing testing and validation.
      - Done: Completed and deployed features.
  - Each user story was assigned to its relevant sprint and tracked on the board to ensure visibility into the development process.
  - For example, once the "Implement Monthly Subscription Workflow" user story was completed, it was moved from In Progress to Done.

This structure provided transparency, allowed blockers to be identified early, and ensured smooth progress through each sprint.

   [GitHub Project Board - Brick Heroes](https://github.com/users/SophieMcGee/projects/3)

4. **Regular Retrospectives**

At the end of each sprint, retrospectives were conducted to reflect on the process and identify areas for improvement.

  - Key questions included:
      - What went well?
      - What challenges were encountered?
      - What can be improved in the next sprint?
  - Retrospectives allowed for:
      - Addressing technical debt.
      - Streamlining processes to improve delivery times.
      - Enhancing collaboration and decision-making for future tasks.

These reflective sessions ensured the development process remained agile and adaptable.

5. **Continuous Integration and Testing**

To maintain a robust and reliable codebase, continuous integration principles were applied.

  - Each feature was developed and tested in isolation, ensuring it met the acceptance criteria before being integrated into the main project.
  - Testing focused on:
      - Functional testing for core features (e.g., borrowing Lego sets, subscription management).
      - Validation of edge cases (e.g., handling expired subscriptions or unavailable sets).
   - Automated tests were created for critical features to ensure they worked as intended across updates.
   - Any issues identified during testing were documented in GitHub Issues and addressed promptly, preventing regressions and maintaining site stability.

6. **Prioritisation Using MoSCoW**

The MoSCoW method was used to prioritize user stories and features systematically:

  - Must Have: User registration, borrowing and returning Lego sets, subscription payments.
  - Should Have: User reviews and ratings for Lego sets, waitlist notifications for unavailable sets.
  -	Could Have: A gallery for users to share their builds, gamified rewards for frequent borrowers.
  - Won’t Have: Features planned for future phases, like multi-language support or advanced analytics for users.

This approach ensured that critical functionality was delivered first while leaving room for enhancements later in the project lifecycle.


# User Experience (UX)

## Client Background and Goals

The Brick Heroes platform is designed to provide a seamless and engaging space for Lego enthusiasts to access a subscription-based service for borrowing and purchasing Lego sets. As the developer and someone passionate about creativity and sustainability, I recognised the need for a platform that simplifies access to high-quality Lego sets while promoting reuse and reducing waste. The goals for this website include:

* **Catering to a wide user base:** – The platform is designed for a diverse audience, from casual hobbyists to avid builders and parents looking for fun, cost-effective activities for their children.
* **Ease of use and accessiblity** – A clean, intuitive interface ensures users can browse Lego sets, manage subscriptions, and complete transactions effortlessly on any device.
* **Fostering creativity and community** – The platform promotes user engagement by providing tools to review and rate sets, share builds, and interact with other users through a blog and gallery.
* **Clear pathways for action** – Strategically placed calls-to-action (CTAs) guide users to subscribe, borrow, purchase, or participate in community activities, ensuring a smooth user journey.
* **Sustainability and value** – By encouraging borrowing and reuse, the site offers a cost-effective and environmentally friendly way to enjoy Lego sets.

[Back to top](#contents)


## Target Audience

Based on research into the Lego community and subscription services, Brick Heroes is designed to serve the following target audiences:

* **1.	Families and parents:**
    - Parents looking for affordable, fun, and educational activities for their children.
    - Families interested in borrowing rather than purchasing expensive Lego sets.

* **2.	Avid Lego enthusiasts:**
    - Builders seeking access to a variety of sets to fuel their creativity without the commitment of ownership.
    - Hobbyists looking for exclusive or themed sets that might not be available for purchase elsewhere.

* **3.	Gift Shoppers:**
    - Individuals searching for creative gift options, such as gift cards or annual subscriptions.

* **4.	Sustainability-conscious users::**
    - Individuals who value eco-friendly alternatives to toy consumption and appreciate the platform's focus on reuse and sharing.

* **5.	Community-oriented Lego fans:**
    - Builders who enjoy sharing their creations, leaving reviews, and engaging with blog content about Lego themes and techniques.

[Back to top](#contents)

## User Stories

**User Stories Summary**

Below is a table summarising the milestones/epics for the Brick Heroes platform. Each milestone represents a key area of focus during the development process and includes user stories designed to achieve specific goals.