from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.balancer import balance_reaction
from backend.stoichiometry import calculate_molar_mass
from backend.stoichiometry import find_limiting_reagent
from backend.stoichiometry import calculate_theoretical_yield
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Reaction Balancer & Stoichiometry Calculator",
    description="Balance chemical equations and calculate stoichiometry.",
    version="1.0.0"
)
app.add_middleware(CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500",
                  "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EquationRequest(BaseModel):
    equation: str


@app.get("/")
def home():
    return {
        "message": "Reaction Balancer API is running!"
    }


@app.post("/balance")
def balance_equation(request: EquationRequest):
    try:
        result = balance_reaction(request.equation)
        return {
            "original_equation": request.equation,
            "balanced_equation": result
        }
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
class FormulaRequest(BaseModel):
    formula: str
class LimitingReagentRequest(BaseModel):
    equation:str
    available_moles:dict[str,float]
class TheoreticalYieldRequest(BaseModel):
    equation:str
    available_moles:dict[str,float]
    product_formula:str

@app.post("/molar-mass")
def molar_mass(request: FormulaRequest):
    try:
        result = calculate_molar_mass(request.formula)

        return {
            "formula": request.formula,
            "molar_mass": result,
            "unit": "g/mol"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
@app.post("/limiting-reagent")
def limiting_reagent(request: LimitingReagentRequest):
    try:
        result = find_limiting_reagent(
            request.equation,
            request.available_moles
        )

        return {
            "limiting_reagent": result
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
@app.post("/theoretical-yield")
def theoretical_yield(request: TheoreticalYieldRequest):
    try:
        result = calculate_theoretical_yield(
            request.equation,
            request.available_moles,
            request.product_formula
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )