const form = document.getElementById("houseForm");
const price = document.getElementById("price");
const message = document.getElementById("resultMessage");
const error = document.getElementById("error");
const button = document.getElementById("predictButton");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    // Collect property details
    const house = {
        area: Number(document.getElementById("area").value),
        bedrooms: Number(document.getElementById("bedrooms").value),
        bathrooms: Number(document.getElementById("bathrooms").value),
        floors: Number(document.getElementById("floors").value),
        age: Number(document.getElementById("age").value),
        location: Number(document.getElementById("location").value)
    };

    // Validate the input values
    if (
        !Number.isFinite(house.area) ||
        house.area < 100 ||
        house.area > 100000 ||
        !Number.isInteger(house.bedrooms) ||
        house.bedrooms < 1 ||
        house.bedrooms > 20 ||
        !Number.isInteger(house.bathrooms) ||
        house.bathrooms < 1 ||
        house.bathrooms > 20 ||
        !Number.isInteger(house.floors) ||
        house.floors < 1 ||
        house.floors > 10 ||
        !Number.isInteger(house.age) ||
        house.age < 0 ||
        house.age > 200 ||
        ![1, 2, 3].includes(house.location)
    ) {
        error.textContent = "Please enter valid property details.";
        return;
    }

    // Show loading status
    button.disabled = true;
    button.querySelector("span").textContent = "Analyzing Property...";
    price.textContent = "Calculating...";
    message.textContent = "Our machine learning model is processing your details.";
    error.textContent = "";

    try {
        // Send data to Flask backend
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(house)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Prediction failed.");
        }

        const predictedPrice = Number(data.predicted_price);

        if (!Number.isFinite(predictedPrice)) {
            throw new Error("The server returned an invalid prediction.");
        }

        // Display formatted prediction
        price.textContent = predictedPrice.toLocaleString("en-IN", {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0
        });

        message.textContent =
            "Estimated value based on the property details you provided.";

    } catch (err) {
        price.textContent = "₹ —";
        message.textContent = "We couldn't complete the valuation.";
        error.textContent = err.message ||
            "Please check your connection and try again.";
    } finally {
        button.disabled = false;
        button.querySelector("span").textContent =
            "Estimate Property Value";
    }
});
