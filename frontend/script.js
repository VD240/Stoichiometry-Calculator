const API_URL = "http://127.0.0.1:8000";

// Common function to send data to FastAPI
async function sendRequest(endpoint, data) {
    const response = await fetch(`${API_URL}${endpoint}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.detail || "Something went wrong");
    }

    return result;
}


// 1. Balance chemical equation
async function balanceReaction() {
    const equation = document.getElementById("equation").value;
    const output = document.getElementById("balance-result");

    try {
        const result = await sendRequest("/balance", {
            equation: equation
        });

        output.textContent =
            "Balanced Equation: " + result.balanced_equation;

    } catch (error) {
        output.textContent = "Error: " + error.message;
    }
}


// 2. Calculate molar mass
async function calculateMolarMass() {
    const formula = document.getElementById("formula").value;
    const output = document.getElementById("mass-result");

    try {
        const result = await sendRequest("/molar-mass", {
            formula: formula
        });

        output.textContent =
            `Molar Mass: ${result.molar_mass} ${result.unit}`;

    } catch (error) {
        output.textContent = "Error: " + error.message;
    }
}


// 3. Find limiting reagent
async function calculateLimitingReagent() {
    const equation = document.getElementById("limiting-equation").value;
    const molesText = document.getElementById("limiting-moles").value;
    const output = document.getElementById("limiting-result");

    try {
        const available_moles = JSON.parse(molesText);

        const result = await sendRequest("/limiting-reagent", {
            equation: equation,
            available_moles: available_moles
        });

        output.textContent =
            "Limiting Reagent: " + result.limiting_reagent;

    } catch (error) {
        output.textContent = "Error: " + error.message;
    }
}


// 4. Calculate theoretical yield
async function calculateTheoreticalYield() {
    const equation = document.getElementById("yield-equation").value;
    const molesText = document.getElementById("yield-moles").value;
    const product = document.getElementById("product-formula").value;
    const output = document.getElementById("yield-result");

    try {
        const available_moles = JSON.parse(molesText);

        const result = await sendRequest("/theoretical-yield", {
            equation: equation,
            available_moles: available_moles,
            product_formula: product
        });

        output.textContent =
            `Theoretical Yield: ${result.moles} mol | ${result.mass_g} g`;

    } catch (error) {
        output.textContent = "Error: " + error.message;
    }
}