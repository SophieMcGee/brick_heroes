document.addEventListener("DOMContentLoaded", function () {
    var stripePublicKey = document.getElementById("id_stripe_public_key").textContent;
    var clientSecret = document.getElementById("id_client_secret").textContent;
    var stripe = Stripe(stripePublicKey);
    var elements = stripe.elements();
    
    var card = elements.create("card", {
        style: {
            base: {
                fontSize: "16px",
                color: "#000",
                "::placeholder": { color: "#888" },
            },
            invalid: { color: "#dc3545" },
        },
    });

    card.mount("#card-element");

    var form = document.getElementById("payment-form");
    var cardErrors = document.getElementById("card-errors");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        stripe.confirmCardPayment(clientSecret, {
            payment_method: { card: card },
        }).then(function (result) {
            if (result.error) {
                cardErrors.textContent = result.error.message;
            } else {
                form.submit();
            }
        });
    });
});
