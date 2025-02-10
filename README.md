# **_Brick Heroes - Project Portfolio 5_**

Welcome to Brick Heroes, a vibrant, comic-book-inspired subscription service designed for LEGO enthusiasts of all ages! This innovative platform offers users the ability to borrow LEGO sets instead of purchasing them, making high-quality LEGO building more affordable, accessible, and sustainable.

Traditional LEGO collections can be expensive and take up space over time. With Brick Heroes, users can subscribe to a monthly plan, choose sets they want to build, borrow them for as long as they need, and return them to borrow new ones. This cycle allows for continuous creativity while reducing costs and waste.

The live site is available to view via this link: <a href="https://brick-heroes-52ffabb94b76.herokuapp.com/" target="_blank" rel="noopener">Brick Heroes</a>

![Responsive View](docs/readme_images/responsive-view.jpg)

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

The Brick Heroes website is designed to provide a comprehensive platform for users to explore and purchase Lego sets through a subscription-based model. The primary goal is to create an engaging, user-friendly space that empowers builders of all ages to access a wide variety of Lego sets affordably, while also promoting sustainability through the reuse of sets. The site integrates borrowing functionality and e-commerce subscription management, ensuring a seamless experience for users.

Additionally, Brick Heroes aims to foster a creative community of Lego enthusiasts by offering features such as a Facebook page where customers can share building tips, share creations, and the ability to leave reviews and feedback on borrowed sets. The website's design reflects a vibrant, comic-book-inspired theme to make the browsing and interaction experience fun and memorable.


**Key objectives:**
1. **Subscription Management**
  - Enable users to view, select, and manage subscription plans, including monthly options, with clear pricing and benefits.
  - Provide flexible management tools for upgrading, downgrading, or cancelling subscriptions.

2. **Borrowing and Returning Sets**
  - Offer a seamless borrowing system where users can browse and filter sets by theme, difficulty, and availability.
  - Allow users to borrow sets and return them easily, with clear stock availability.

3. **Creative Engagement**
  - Foster community interaction through features like user reviews and ratings.
  - Create a social media platform for users to share tips, reviews, and Lego news.

5. **Accessibility and Usability**
  - Ensure the site is fully responsive and accessible, providing a smooth experience across devices, including mobile, tablet, and desktop.
  - Use an intuitive design and navigation structure to simplify browsing and borrowing for all users.

6. **Sustainability Focus**
  - Promote eco-friendly practices by encouraging the reuse of Lego sets, reducing waste, and minimising the environmental impact of toy consumption.

7. **Administrator Tools**
  - Provide a robust admin interface for managing Lego sets, monitoring user activity, and moderating reviews.
  - Include tools to track subscriptions, reviews and borrowing.

8. **Notifications and Feedback**
  - Keep users informed with timely notifications such as subscription renewals.
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
      - Implementing e-commerce functionality for subscriptions and potential future ecommerce options.

This iterative structure ensured steady progress while maintaining the flexibility to pivot when necessary.

2. **User Stories**

User stories were at the heart of the development process, capturing features and functionality from the perspective of different user types (e.g., subscribers, admins, and visitors).

  - Each user story was written to reflect specific user goals, helping to focus on delivering value.
  - Prioritisation followed the MoSCoW framework:
      - Must Have: Core functionality like account registration, borrowing Lego sets, and subscription management.
      - Should Have: Features enhancing usability, such as filtering Lego sets by theme or difficulty.
      - Could Have: Community features like buying gift cards and sets, a blog for sharing Lego creations or commenting on blog posts.
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
  - Should Have: User reviews and ratings for Lego sets, notifications.
  -	Could Have: A gallery for users to share their builds, blog area, purchasing of sets and giftcards.
  - Won’t Have: Features planned for future phases, like multi-language support or advanced analytics for users.

This approach ensured that critical functionality was delivered first while leaving room for enhancements later in the project lifecycle.


# User Experience (UX)

## Client Background and Goals

The Brick Heroes platform is designed to provide a seamless and engaging space for Lego enthusiasts to access a subscription-based service for borrowing Lego sets. As the developer and someone passionate about creativity and sustainability, I recognised the need for a platform that simplifies access to high-quality Lego sets while promoting reuse and reducing waste. The goals for this website include:

* **Catering to a wide user base:** – The platform is designed for a diverse audience, from casual hobbyists to avid builders and parents looking for fun, cost-effective activities for their children.
* **Ease of use and accessiblity** – A clean, intuitive interface ensures users can browse Lego sets, manage subscriptions, and complete transactions effortlessly on any device.
* **Fostering creativity and community** – The platform promotes user engagement by providing tools to review and rate sets, with links to a newsletter and social media.
* **Clear pathways for action** – Strategically placed calls-to-action (CTAs) guide users to subscribe, borrow, purchase, ensuring a smooth user journey.
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
    - Individuals searching for creative gift options, such as subscriptions.

* **4.	Sustainability-conscious users::**
    - Individuals who value eco-friendly alternatives to toy consumption and appreciate the platform's focus on reuse and sharing.

* **5.	Community-oriented Lego fans:**
    - Builders who enjoy sharing their creations, leaving reviews, and engaging with news about Lego themes and techniques.

[Back to top](#contents)

## User Stories

**User Stories Summary**

Below is a table summarising the milestones/epics for the Brick Heroes platform. Each milestone represents a key area of focus during the development process and includes user stories designed to achieve specific goals. Doe to time constaints and the fact this is a project that is submitted as part of my course, these will be fully developed as my coding knowledge and abilities develop. As explained above, areas within these user stories will focus on must have, should have and could have, with some developments saved for future implementation that are not essential to the core objectives of the app.

| **Milestone**                     | **Summary**                                                                                          |
|------------------------------------|------------------------------------------------------------------------------------------------------|
| **Frontend Design**                | Focuses on visual and functional aspects of the site, including the favicon, layout consistency, subscription pricing details, and responsiveness across devices. |
| **User Account and Authentication** | Handles core user management features such as account registration, login/logout, email verification, password reset, and profile updates. |
| **Subscription Management**        | Implements subscription workflows, including selecting, upgrading, downgrading, and canceling plans, as well as sending renewal reminders. |
| **Borrowing and Returning Lego Sets** | Manages the core functionality of borrowing and returning Lego sets, including waitlists for unavailable sets and filtering options for browsing. |
| **E-Commerce Features**            | Provides e-commerce functionality for purchasing Lego sets and gift cards, as well as redeeming gift cards during checkout. |
| **Blog and Community Interaction**  | Encourages engagement by allowing users to read blog posts, share Lego creations in a gallery, and participate in community-driven features. |
| **Administrator Tools**            | Focuses on administrative functionality, such as managing Lego sets, moderating user reviews, and viewing subscription and order analytics. |
| **Notifications and Feedback**      | Ensures users receive confirmation emails for actions such as subscriptions, purchases, and borrowing to provide clear communication and feedback. |
| **Testing and Documentation**      | Covers writing and running automated tests for key features and creating comprehensive user and developer documentation, including deployment instructions. |

[Back to top](#contents)

Each user story within the milestones is categorised and tracked through the GitHub Project Board, ensuring iterative development and task completion. Below is a breakdown of user stories associated with each milestone.

## **Detailed User Stories**

### **Frontend Design**

<details><summary><b>User Story: View the site favicon</b></summary>

* **Issue**: As a user, I can see a recognisable favicon in the browser tab so that I can easily identify Brick Heroes when multiple tabs are open.

#### **Acceptance Criteria:**
- A favicon related to the site's branding is displayed in all browsers.
- The favicon is clear and visible across different devices.

* **Label**: Could Have  
* **Milestone**: Frontend Design  
</details><hr>

<details><summary><b>User Story: See a consistent theme across the site</b></summary>

* **Issue**: As a user, I can experience a consistent comic-book-inspired design across all pages so that I enjoy a cohesive and fun browsing experience.

#### **Acceptance Criteria:**
- Header, footer, and colour schemes are consistent.
- The comic-book theme is applied through bold fonts, colourful highlights, and speech-bubble-style buttons.
- All pages are responsive and adapt to different devices.

* **Label**: Must Have  
* **Milestone**: Frontend Design  
</details><hr>

<details><summary><b>User Story: View subscription pricing details</b></summary>

* **Issue**: As a user, I can view subscription plans with clear pricing and features so that I can make an informed decision.

#### **Acceptance Criteria:**
- The homepage includes a pricing table with subscription tiers.
- Each tier displays the price, borrowing limits, and unique benefits.
- A clear call-to-action button for each plan is available.

* **Label**: Must Have  
* **Milestone**: Frontend Design  
</details><hr>

### **User Account and Authentication**

<details><summary><b>User Story: Register an account</b></summary>

* **Issue**: As a new user, I can create an account so that I can start borrowing sets and managing subscriptions.

#### **Acceptance Criteria:**
- The registration form includes fields for name, email, and password.
- A success message confirms the account creation.
- Users are redirected to their dashboard after signing up.

* **Label**: Must Have  
* **Milestone**: User Account and Authentication  
</details><hr>

<details><summary><b>User Story: Receive email verification</b></summary>

* **Issue**: As a user, I can verify my email address so that I can activate my account securely.

#### **Acceptance Criteria:**
- After registration, a verification email is sent automatically.
- Clicking the link activates the user account.
- A notification displays if the email is successfully verified.

* **Label**: Must Have  
* **Milestone**: User Account and Authentication  
</details><hr>

<details><summary><b>User Story: Log in to my account</b></summary>

* **Issue**: As a user, I can log in to my account so that I can manage my subscriptions and borrow sets.

#### **Acceptance Criteria:**
- Login form with email and password fields.
- Incorrect login attempts display an error message.
- Successful login redirects to the dashboard.

* **Label**: Must Have  
* **Milestone**: User Account and Authentication  
</details><hr>

<details><summary><b>User Story: Reset my password</b></summary>

* **Issue**: As a user, I can reset my password if I forget it so that I can regain access to my account.

#### **Acceptance Criteria:**
- A password reset link is sent to the user's email.
- Users can securely create a new password.

* **Label**: Must Have  
* **Milestone**: User Account and Authentication  
</details><hr>

<details><summary><b>User Story: Update my profile</b></summary>

* **Issue**: As a user, I can update my account details so that my information stays current.

#### **Acceptance Criteria:**
- Editable fields for name, email, and password.
- Changes are saved and confirmed.

* **Label**: Should Have  
* **Milestone**: User Account and Authentication  
</details><hr>

### **Subscription Management**

<details><summary><b>User Story: Select a subscription plan</b></summary>

* **Issue**: As a user, I can choose a subscription plan so that I can start borrowing Lego sets.

#### **Acceptance Criteria:**
- Subscription options are listed during registration or on the homepage.
- Users can pick a monthly or annual plan.
- Payment processing confirms the selected plan.

* **Label**: Must Have  
* **Milestone**: Subscription Management  
</details><hr>

<details><summary><b>User Story: Upgrade or downgrade my subscription</b></summary>

* **Issue**: As a user, I can adjust my subscription plan so that I can find the one that best fits my needs.

#### **Acceptance Criteria:**
- Users can view their current plan in the account dashboard.
- Options to upgrade or downgrade are available.
- Plan changes take effect on the next billing cycle.

* **Label**: Should Have  
* **Milestone**: Subscription Management  
</details><hr>

<details><summary><b>User Story: Cancel my subscription</b></summary>

* **Issue**: As a user, I can cancel my subscription so that I am no longer charged.

#### **Acceptance Criteria:**
- A cancel button is accessible in the account dashboard.
- Users receive a confirmation email after cancellation.
- Account access remains, but borrowing privileges are suspended.

* **Label**: Should Have  
* **Milestone**: Subscription Management  
</details><hr>

<details><summary><b>User Story: Receive subscription renewal reminders</b></summary>

* **Issue**: As a user, I can get email reminders about upcoming subscription renewals so that I stay informed.

#### **Acceptance Criteria:**
- Reminder email sent 7 days before renewal.
- Email includes subscription details and a link to manage the subscription.

* **Label**: Should Have  
* **Milestone**: Subscription Management  
</details><hr>

### **Borrowing and Returning Lego Sets**

<details><summary><b>User Story: Browse available Lego sets</b></summary>

* **Issue**: As a user, I can browse all available Lego sets so that I can choose one to borrow.

#### **Acceptance Criteria:**
- Lego sets are displayed in a grid format.
- Filters allow sorting by theme, difficulty, and availability.
- Clicking a set displays detailed information.

* **Label**: Must Have  
* **Milestone**: Borrowing and Returning Lego Sets  
</details><hr>

<details><summary><b>User Story: Borrow a Lego set</b></summary>

* **Issue**: As a user, I can borrow a Lego set so that I can start building.

#### **Acceptance Criteria:**
- Users can add an available set to their "Borrowed Items."
- Borrowed sets are marked as unavailable to other users.
- A confirmation email is sent upon successful borrowing.

* **Label**: Must Have  
* **Milestone**: Borrowing and Returning Lego Sets  
</details><hr>

<details><summary><b>User Story: Return a Lego set</b></summary>

* **Issue**: As a user, I can return a borrowed set so that I can borrow a new one.

#### **Acceptance Criteria:**
- Users can mark sets as returned in their dashboard.
- The set's availability is updated in the database.
- A confirmation message appears upon successful return.

* **Label**: Must Have  
* **Milestone**: Borrowing and Returning Lego Sets  
</details><hr>

<details><summary><b>User Story: Join a waitlist for unavailable Lego sets</b></summary>

* **Issue**: As a user, I can join a waitlist for a Lego set so that I’m notified when it becomes available.

#### **Acceptance Criteria:**
- Waitlist button appears for unavailable sets.
- Notification sent when the set becomes available.

* **Label**: Could Have  
* **Milestone**: Borrowing and Returning Lego Sets  
</details><hr>

---

### **E-Commerce Features**

<details><summary><b>User Story: Purchase a Lego set</b></summary>

* **Issue**: As a user, I can buy a Lego set outright so that I can own my favourite builds.

#### **Acceptance Criteria:**
- Lego sets for sale are clearly marked.
- The checkout process includes payment confirmation.
- Purchased sets are excluded from the borrowing pool.

* **Label**: Could Have  
* **Milestone**: E-Commerce Features  
</details><hr>

<details><summary><b>User Story: Buy a gift card</b></summary>

* **Issue**: As a user, I can purchase a gift card so that I can share the Brick Heroes experience with someone else.

#### **Acceptance Criteria:**
- Gift cards have multiple denominations available.
- A confirmation email with a unique gift card code is sent.
- Gift card codes can be redeemed during checkout.

* **Label**: Could Have  
* **Milestone**: E-Commerce Features  
</details><hr>

<details><summary><b>User Story: Redeem a gift card</b></summary>

* **Issue**: As a user, I can redeem a gift card code during checkout so that I can use its value toward my purchase.

#### **Acceptance Criteria:**
- Gift card field is present in the checkout form.
- Gift card value is applied to the total.

* **Label**: Could Have  
* **Milestone**: E-Commerce Features  
</details><hr>

---

### **Blog and Community Interaction**

<details><summary><b>User Story: View blog articles</b></summary>

* **Issue**: As a user, I can read blog posts about Lego tips and news so that I stay inspired.

#### **Acceptance Criteria:**
- Blog page displays a list of posts with thumbnails and snippets.
- Clicking a post opens the full article.

* **Label**: Should Have  
* **Milestone**: Blog and Community Interaction  
</details><hr>

<details><summary><b>User Story: Submit Lego creations to the gallery</b></summary>

* **Issue**: As a user, I can share my Lego builds in a gallery so that I inspire others.

#### **Acceptance Criteria:**
- Users can upload images and captions.
- Creations are reviewed before being displayed.

* **Label**: Could Have  
* **Milestone**: Blog and Community Interaction  
</details><hr>

---

### **Administrator Tools**

<details><summary><b>User Story: Manage Lego sets</b></summary>

* **Issue**: As an admin, I can add, edit, or delete Lego sets so that the catalogue stays up to date.

#### **Acceptance Criteria:**
- Admin panel includes controls for Lego set management.
- Changes reflect immediately on the site.

* **Label**: Must Have  
* **Milestone**: Administrator Tools  
</details><hr>

<details><summary><b>User Story: Moderate reviews and comments</b></summary>

* **Issue**: As an admin, I can approve or delete user reviews and comments so that the site maintains a positive environment.

#### **Acceptance Criteria:**
- Admins see flagged or pending comments in the dashboard.
- Options to approve or delete are available.

* **Label**: Should Have  
* **Milestone**: Administrator Tools  
</details><hr>

<details><summary><b>User Story: View subscription analytics</b></summary>

* **Issue**: As an admin, I can view subscription statistics so that I understand user engagement.

#### **Acceptance Criteria:**
- Reports include active subscriptions, cancellations, and revenue.
- Filters for monthly and yearly views are available.

* **Label**: Could Have  
* **Milestone**: Administrator Tools  
</details><hr>

<details><summary><b>User Story: View order history</b></summary>

* **Issue**: As an admin, I can view user order histories so that I can resolve disputes or answer questions.

#### **Acceptance Criteria:**
- Order details are displayed in the admin panel.
- Orders can be filtered by user or date.

* **Label**: Should Have  
* **Milestone**: Administrator Tools  
</details><hr>

---

### **Notifications and Feedback**

<details><summary><b>User Story: Receive confirmation emails</b></summary>

* **Issue**: As a user, I can get confirmation emails for subscriptions, purchases, and borrowing so that I know my actions were successful.

#### **Acceptance Criteria:**
- Email includes details of the action.
- Email is sent promptly after the action.

* **Label**: Must Have  
* **Milestone**: Notifications and Feedback  
</details><hr>

---

### **Testing and Documentation**

<details><summary><b>User Story: Run automated tests</b></summary>

* **Issue**: As a developer, I can write and run automated tests so that I ensure the site works as intended.

#### **Acceptance Criteria:**
- Test scripts cover key functionalities like login, checkout, and subscriptions.
- Tests pass consistently without errors.

* **Label**: Must Have  
* **Milestone**: Testing and Documentation  
</details><hr>

<details><summary><b>User Story: Write user documentation</b></summary>

* **Issue**: As a developer, I can write documentation for the site so that users understand how to use its features.

#### **Acceptance Criteria:**
- Documentation includes step-by-step guides for subscriptions, borrowing, and purchases.
- Available as a help section on the site.

* **Label**: Must Have  
* **Milestone**: Testing and Documentation  
</details><hr>

<details><summary><b>User Story: Write deployment instructions</b></summary>

* **Issue**: As a developer, I can document deployment steps so that the site can be redeployed easily.

#### **Acceptance Criteria:**
- Instructions cover setting up the database, environment variables, and dependencies.
- Deployment is successfully replicated using the documentation.

* **Label**: Should Have  
* **Milestone**: Testing and Documentation  
</details><hr>


There are several areas within the Brick Heroes GitHub Projects that remain open and are marked as 'To Do' or 'In Progress', reserved for future development to further enhance the platform's functionality and user experience. These features are part of the platform's long-term vision to remain innovative, user-centric, and scalable, although these future developments are not essential to the main core functionality now.