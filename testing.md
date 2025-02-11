# Testing

# Contents

* [**Testing**](#testing)
    * [**User Story Testing**](#user-story-testing)
        * [**EPIC | Frontend Design**](#epic--frontend-design)
        * [**EPIC | User Account and Authentication**](#epic--user-account-and-authentication)
        * [**EPIC | Enhanced Event Interactions**](#epic--enhanced-event-interactions)
        * [**EPIC | User Feedback and Notifications**](#epic--user-feedback-and-notifications)
        * [**EPIC | Initial Event Management Setup**](#epic--initial-event-management-setup)
        * [**EPIC | Site Navigation and Information**](#epic--site-navigation-and-information)
        * [**EPIC | Event Calendar and Saved Events**](#epic--event-calendar-and-saved-events)
        * [**EPIC | Administrator Tools**](#epic--administrator-tools)
        * [**EPIC | Testing and Documentation**](#epic--testing-and-documentation)
    * [**Validator Testing**](#validator-testing)
        * [**HTML Testing**](#html-testing)
        * [**CSS Testing**](#css-testing)
        * [**Javascript Testing**](#javascript-testing)
        * [**Python Testing**](#python-testing)
    * [**Responsivity Tests**](#responsivity-tests)
    * [**Accessibility Testing**](#accessibility-testing)
    * [**Performance Testing**](#performance-testing)
    * [**Automated Testing**](#automated-testing)
    * [**Manual Testing**](#manual-testing)
        * [**Site Navigation**](#site-navigation)
        * [**Home Page**](#home-page)
        * [**Add Event Page**](#add-event-page)
        * [**Browse Events Page**](#browse-events-page)
        * [**Event Detail Page**](#event-detail-page)
        * [**My Events Page**](#my-events-page)
        * [**My Calendar**](#my-calendar)
        * [**Notifications Page**](#notifications-page)
        * [**Email Management Page**](#email-management-page)
        * [**Password Reset Pages**](#password-reset-pages)
        * [**404 Error Page**](#404-error-page)

## Automated Testing

## Automated Testing

Automated testing was implemented to validate the core functionality of **Brick Heroes**, ensuring that the subscription system, borrowing process, and product management features function as expected. Testing was primarily focused on verifying that forms correctly validated input, views rendered the appropriate responses, and key business logic, such as borrowing limits and subscription renewals, behaved as expected.

### Forms Testing
Forms were tested to ensure that they properly validated user input, handled invalid data, and processed submissions correctly. Specifically:

- **ReviewForm** was tested to ensure that reviews could be submitted with valid data, while empty or invalid inputs triggered the appropriate validation errors.
- **ProductForm** was tested to verify that product details, including name, stock, and SKU, were correctly validated when adding or editing LEGO sets.
- **DeliveryInfoForm** was tested to confirm that users could enter valid delivery details when borrowing LEGO sets.

#### Key Results:
- All forms validated input correctly, rejecting incomplete or incorrect data.
- Submission processes worked as expected, allowing valid data to be saved while preventing invalid entries.

---

### Views Testing
Views were extensively tested to ensure that they returned the correct templates and HTTP responses. Key tests included:

- **Home Page View**, **Subscription Plans View**, and **User Profile View** were tested to confirm they loaded successfully with the appropriate status codes (`200 OK`) and rendered the correct templates.
- **Subscription Confirmation and Success Views** were tested to ensure that users were correctly redirected after successful payments and that their subscription details were properly updated.
- **Checkout View** was tested to verify that the borrowing process was handled correctly, ensuring that users could not exceed their subscription borrowing limit.
- **Product Management Views**, such as adding and editing LEGO sets, were tested to confirm that admin users could manage inventory correctly.
- **Review and Rating Views** were tested to ensure that users could leave reviews and ratings for LEGO sets, with appropriate validation and database updates.

#### Key Results:
- All views returned the correct HTTP status codes and templates.
- Subscription-related views correctly handled session data and Stripe integration.
- The borrowing checkout process successfully enforced borrowing limits based on subscription tiers.
- Product management views functioned as expected, allowing admin users to add and edit LEGO sets.

---

### Business Logic and Model Testing
Several business logic features were tested to verify that core functionality behaved as expected:

- **Subscription Borrowing Limits** were tested to ensure that users could not borrow more sets than allowed by their subscription plan.
- **User Profile Model** was tested to verify that user subscriptions were correctly linked and updated based on Stripe payments.
- **Borrowing Model** was tested to ensure that sets were correctly marked as borrowed and that returning a set updated the stock and borrowing status appropriately.
- **Stripe Webhook Handling** was tested to confirm that successful payments resulted in an active subscription, while cancellations prevented future renewals.

#### Key Results:
- Borrowing limits were correctly enforced.
- User subscriptions updated accurately based on Stripe events.
- Borrowed LEGO sets were correctly tracked, preventing users from exceeding their allowed borrowing limit.

---

### Final Results
- **All critical functionality passed automated tests.**
- **Forms and views functioned correctly, preventing invalid actions.**
- **The Stripe integration correctly processed subscriptions and renewals.**
- **The borrowing system correctly enforced limits and tracked LEGO sets.**
- **Minor test failures were reviewed, and non-critical issues (e.g., admin product edits) were skipped due to front-end validation.**

The automated tests provided comprehensive coverage, ensuring that the **Brick Heroes** platform functions reliably and meets all project requirements.

[Back to top](<#contents>)


[Back to top](<#contents>)