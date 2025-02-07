document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".subscribe-button").forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            var planId = event.target.dataset.planId;

            // Redirect user to Django's subscribe URL (which then redirects to Stripe)
            window.location.href = `/subscriptions/subscribe/${planId}/`;
        });
    });
});