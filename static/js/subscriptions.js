document.addEventListener("DOMContentLoaded", function () {
    var stripePublicKey = document.getElementById("id_stripe_public_key").textContent;
    var stripe = Stripe(stripePublicKey);

    document.querySelectorAll(".subscribe-button").forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            var planId = event.target.dataset.planId;

            fetch(`/subscriptions/subscribe/${planId}/`, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
            .then(response => response.json())
            .then(data => {
                return stripe.redirectToCheckout({ sessionId: data.sessionId });
            })
            .catch(error => {
                console.error("Error:", error);
            });
        });
    });
});